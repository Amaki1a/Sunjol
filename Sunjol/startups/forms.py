from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Startup, Vacancy, Investor, User, Comment, Message, Rating, Review, UserVerification, StartupMetrics, Achievement
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class StartupForm(forms.ModelForm):
    class Meta:
        model = Startup
        fields = ['name', 'description', 'industry', 'stage', 'funding_goal', 'location', 'website', 'pitch_deck']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Опишите ваш стартап подробно...'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название вашего стартапа'}),
            'industry': forms.Select(attrs={'class': 'form-select'}),
            'stage': forms.Select(attrs={'class': 'form-select'}),
            'funding_goal': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': 'Сумма в рублях'
            }),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Город или регион'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://'}),
            'pitch_deck': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.ppt,.pptx',
                'help_text': 'Поддерживаемые форматы: PDF, PPT, PPTX'
            }),
        }
        help_texts = {
            'name': 'Укажите краткое и запоминающееся название вашего стартапа',
            'description': 'Опишите ваш стартап, его миссию и уникальное торговое предложение',
            'industry': 'Выберите основную отрасль, в которой работает ваш стартап',
            'stage': 'Укажите текущую стадию развития стартапа',
            'funding_goal': 'Укажите сумму, которую вы хотите привлечь',
            'location': 'Укажите город или регион, где находится ваш стартап',
            'website': 'Укажите URL вашего сайта или лендинга',
            'pitch_deck': 'Загрузите презентацию вашего стартапа (PDF, PPT или PPTX)'
        }

class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['role', 'description', 'skills_required']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'skills_required': forms.Textarea(attrs={'rows': 3}),
        }

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class InvestorProfileForm(forms.ModelForm):
    class Meta:
        model = Investor
        fields = ['bio', 'investment_focus', 'telegram', 'instagram', 'linkedin', 'twitter', 'facebook', 'resume', 'investment_range', 'preferred_industries']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'investment_focus': forms.Textarea(attrs={'rows': 2}),
            'preferred_industries': forms.Textarea(attrs={'rows': 2})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишите ваш комментарий...'
            }),
            'parent': forms.HiddenInput()
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Введите сообщение...'
            })
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)])
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишите ваш отзыв...',
                'rows': 4
            })
        }

class VerificationForm(forms.ModelForm):
    class Meta:
        model = UserVerification
        fields = ['verification_documents']
        widgets = {
            'verification_documents': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            })
        }

class StartupMetricsForm(forms.ModelForm):
    class Meta:
        model = StartupMetrics
        fields = ['revenue', 'expenses', 'customers', 'active_users', 'churn_rate']
        widgets = {
            'revenue': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Выручка'
            }),
            'expenses': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Расходы'
            }),
            'customers': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество клиентов'
            }),
            'active_users': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Активные пользователи'
            }),
            'churn_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Отток клиентов (%)'
            })
        }

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['type', 'title', 'description', 'icon', 'points']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название достижения'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание достижения'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя иконки Bootstrap'
            }),
            'points': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество очков'
            })
        }

class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }