# chat/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message
from transliterate import translit
import re

@login_required
def chat_rooms(request):
    """Показывает список всех комнат"""
    rooms = ChatRoom.objects.all()
    return render(request, 'chat/rooms.html', {'rooms': rooms})

@login_required
def chat_room(request, room_slug):
    """Показывает комнату чата"""
    room = get_object_or_404(ChatRoom, slug=room_slug)
    messages = Message.objects.filter(room=room).order_by('timestamp')[:50]
    
    return render(request, 'chat/room.html', {
        'room': room,
        'messages': messages
    })

@login_required
def create_room(request):
    """Создает новую комнату"""
    
    if request.method == 'POST':
        name = request.POST.get('name')
        
        # ============================================
        # НОВЫЙ КОД: Создание slug с транслитерацией
        # ============================================
        
        # Транслитерация кириллицы в латиницу
        try:
            slug = translit(name, 'ru', reversed=True)
        except:
            # Если не кириллица, используем как есть
            slug = name
        
        # Приводим к нижнему регистру
        slug = slug.lower()
        
        # Заменяем пробелы и недопустимые символы на дефис
        slug = re.sub(r'[^\w\s-]', '', slug)  # Удаляем спецсимволы
        slug = re.sub(r'[\s_]+', '-', slug)   # Пробелы и _ в дефис
        slug = re.sub(r'-+', '-', slug)       # Множественные дефисы в один
        slug = slug.strip('-')                # Убираем дефисы по краям
        
        # Если slug пустой, используем ID
        if not slug:
            import uuid
            slug = str(uuid.uuid4())[:8]
        
        # ============================================
        # Создаем или получаем существующую комнату
        # ============================================
        
        room, created = ChatRoom.objects.get_or_create(
            slug=slug,
            defaults={'name': name}
        )
        
        # Если комната уже существует, но с другим именем
        if not created and room.name != name:
            # Добавляем номер к slug
            import random
            slug = f"{slug}-{random.randint(1000, 9999)}"
            room = ChatRoom.objects.create(name=name, slug=slug)
        
        return redirect('chat_room', room_slug=room.slug)
    
    return render(request, 'chat/create_room.html')