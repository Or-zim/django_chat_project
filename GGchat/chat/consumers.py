import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from accounts.models import Accounts
from .models import ChatRoom, Message


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Обрабатывает WebSocket соединения для чата
    
    Методы жизненного цикла:
    1. connect()    - Подключение клиента
    2. disconnect() - Отключение клиента
    3. receive()    - Получение сообщения от клиента
    4. send()       - Отправка сообщения клиенту
    """
    
    async def connect(self):
        # Проверяем авторизацию
        if not self.scope['user'].is_authenticated:
            await self.close()
            return
            
        self.room_slug = self.scope['url_route']['kwargs']['room_slug']
        self.room_group_name = f'chat_{self.room_slug}'
        
        # Подключаемся к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
    
        await self.accept()
        
        # Отправляем историю сообщений
        messages = await self.get_messages()
        await self.send(text_data=json.dumps({
            'type': 'message_history',
            'messages': messages
        }))
        
    
    async def disconnect(self, close_code):
        # Отключаемся от группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        
        # Берем пользователя из авторизации (БЕЗОПАСНО)
        user = self.scope['user']
        
        # Сохраняем сообщение
        await self.save_message(user, message)
        
        # Отправляем всем в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'display_name': user.display_name or user.first_name,
                'user_email': user.username,
                'timestamp': timezone.now().strftime('%H:%M')
            }
        )    
        
        
    async def chat_message(self, event):
        """Получаем сообщение из группы и отправляем в WebSocket"""
        
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'display_name': event['display_name'],
            'user_email': event['user_email'],
            'timestamp': event['timestamp']
        }))
        
    
    @database_sync_to_async
    def save_message(self, user, message):
        """Сохраняем сообщение в БД"""
        room = ChatRoom.objects.get(slug=self.room_slug)
        Message.objects.create(user=user, room=room, content=message)
        
    @database_sync_to_async
    def get_messages(self):
        """Получаем последние 50 сообщений"""
        try:
            room = ChatRoom.objects.get(slug=self.room_slug)
            messages = Message.objects.filter(room=room).select_related('user').order_by('-timestamp')[:50]
            
            return [{
                'display_name': msg.user.display_name or msg.user.first_name,
                'user_email': msg.user.username,
                'message': msg.content,
                'timestamp': msg.timestamp.strftime('%H:%M')
            } for msg in reversed(messages)]
        except ChatRoom.DoesNotExist:
            return []