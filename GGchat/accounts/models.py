from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import Q

class Accounts(AbstractUser):
    # Делаем username EmailField для хранения email
    username = models.EmailField(
        unique=True,
        verbose_name='email'
    )
    
    # Создаем display_name как ник пользователя
    display_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='display name'
    )
    
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True, null=False)
    last_online_date = models.DateTimeField(null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    user_created = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['display_name'],
                name='unique_display_name_when_not_null',
                condition=models.Q(display_name__isnull=False)
            )
        ]

    def __str__(self):
        return self.display_name or self.username.split('@')[0]
