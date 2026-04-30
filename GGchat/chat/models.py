from django.db import models
from accounts.models import Accounts
class ChatRoom(models.Model):
    """комната общения"""
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']  # Сначала новые
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'
    
    
    def __str__(self):
        return self.name


class Message(models.Model):
    """сообщения"""
    room = models.ForeignKey(ChatRoom, related_name='message', on_delete=models.CASCADE)
    user = models.ForeignKey(Accounts, related_name='message', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']     # Сначала старые сообщения
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
    
    def __str__(self):
        return f'{self.user.username}: {self.content[:50]}'