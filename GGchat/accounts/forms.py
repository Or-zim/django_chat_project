from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Accounts
from django import forms

# forms.CharField()        # Текст
# forms.EmailField()       # Email (с валидацией)
# forms.IntegerField()     # Целое число
# forms.DecimalField()     # Десятичное число
# forms.BooleanField()     # True/False (checkbox)
# forms.DateField()        # Дата
# forms.DateTimeField()    # Дата + время
# forms.FileField()        # Файл
# forms.ImageField()       # Изображение (проверяет что это картинка)
# forms.URLField()         # URL (с валидацией)
# forms.ChoiceField()      # Выбор из списка

# attrs={
#     'placeholder': 'текст',      # Подсказка в поле
#     'class': 'my-class',         # CSS класс
#     'id': 'custom-id',           # HTML id
#     'autocomplete': 'off',       # Автозаполнение
#     'maxlength': '50',           # Максимум символов
#     'style': 'color: red;',      # Inline стили
#     'data-value': '123',         # Data атрибуты
#     'required': 'required',      # HTML5 валидация
# }


class RegisterForm(UserCreationForm):
    
    email = forms.EmailField(required=True, label='Email', help_text='Используется для входа в систему', widget=forms.EmailInput(attrs={
        'placeholder': 'your@email.com',
        'autocomplete': 'email'
    }))
    
    
    display_name = forms.CharField(required=True, label='Username', max_length=12,  help_text='Название вашей персональной ссылки на профиль', 
                                   widget=forms.TextInput(attrs={
                                       'placeholder': 'username',
                                       'autocomplete': 'off' 
                                   }))
    
    first_name = forms.CharField(required=True, label='Имя', max_length=16, help_text='Как вас будут видеть другие пользователи', 
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'имя',
                                    'autocomplete': 'given-name' 
                                })
                                )
    
    last_name = forms.CharField(required=False, label='Фамилия', max_length=16, widget=forms.TextInput(attrs={
        'placeholder': 'фамилия',
        'autocomplete': 'family-name',
    }))
    
    class Meta:
        model = Accounts
        fields = ['email', 'display_name', 'first_name', 'last_name', 'password1', 'password2']
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """нужен чтобы изменить текущие настроки полей в форме, в данном случае если, меняем настроки полей для паролей так как они объявденны в UserCreationForm"""
        self.fields['password1'].widget.attrs.update({
                'placeholder': '••••••••',
                'autocomplete': 'new-password'
        })
        
        self.fields['password2'].widget.attrs.update({
            'placeholder': '••••••••',
            'autocomplete': 'new-password'
        })
        
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        
        
        self.fields['password1'].help_text = 'Минимум 8 символов'
        self.fields['password2'].help_text = 'Повторите пароль для подтверждения'
    
    
    
    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data.get('email')
        
        if Accounts.objects.filter(username=email).exists():
            raise forms.ValidationError(
                'Пользователь с таким email уже зарегистрирован.'
            )
    
        return email.lower()
    
    def clean_display_name(self):
        """Проверка уникальности отображаемого имени"""
        display_name = self.cleaned_data.get('display_name')
        
        if Accounts.objects.filter(display_name=display_name).exists():
             raise forms.ValidationError(
            'Это отображаемое имя уже занято. Выберите другое.'
        )
        
        if len(display_name) < 3:
            raise forms.ValidationError(
            'Отображаемое имя должно содержать минимум 3 символа.'
        )

        import re
        if not re.match(r'^[\w\s\-]+$', display_name, re.UNICODE):
            raise forms.ValidationError(
            'Отображаемое имя может содержать только буквы, цифры, пробелы, дефисы и подчеркивания.'
        )
        
        return '@' + display_name
    
    
    def save(self, commit=True):
        """
        Сохранение пользователя
        """
        user = super().save(commit=False)
        
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.display_name = self.cleaned_data['display_name']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        
        return user
    
class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')