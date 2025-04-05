from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Startup(models.Model):
    INDUSTRY_CHOICES = [
        ('tech', 'Technology'),
        ('health', 'Healthcare'),
        ('fin', 'Finance'),
        ('edu', 'Education'),
        ('other', 'Other')
    ]
    STAGE_CHOICES = [
        ('idea', 'Idea Stage'),
        ('prototype', 'Prototype'),
        ('seed', 'Seed Stage'),
        ('growth', 'Growth Stage'),
        ('established', 'Established')
    ]
    
    founder = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to='startup_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    funding_goal = models.DecimalField(max_digits=10, decimal_places=2)
    current_funding = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    industry = models.CharField(max_length=20, choices=INDUSTRY_CHOICES, default='tech')
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='idea')
    location = models.CharField(max_length=100, blank=True, default='')
    website = models.URLField(blank=True)
    pitch_deck = models.FileField(upload_to='pitch_decks/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Vacancy(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    description = models.TextField()
    skills_required = models.TextField()
    
    def __str__(self):
        return f"{self.role} at {self.startup.name}"

class Investor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    investment_focus = models.CharField(max_length=200, blank=True)
    telegram = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    resume = models.FileField(upload_to='investor_resumes/', blank=True, null=True)
    investment_range = models.CharField(max_length=100, blank=True)
    preferred_industries = models.CharField(max_length=200, blank=True)
    
    # Настройки уведомлений
    email_notifications = models.BooleanField(default=True)
    investment_alerts = models.BooleanField(default=True)
    startup_updates = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Investor: {self.user.username}"

class Investment(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_invested = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.investor.user.username} invested ${self.amount} in {self.startup.name}"

class Milestone(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.startup.name} - {self.title}"

class Document(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='startup_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.startup.name} - {self.title}"

class Update(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='updates')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.startup.name} - {self.created_at.strftime('%d.%m.%Y')}"

class TeamMember(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='team_members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['startup', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.role} at {self.startup.name}"

class Comment(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Комментарий от {self.author.username} к {self.startup.name}'

class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='chat_rooms')
    created_at = models.DateTimeField(default=timezone.now)
    participants = models.ManyToManyField(User, related_name='chat_rooms')

    def __str__(self):
        return f'Чат {self.name} для {self.startup.name}'

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f'Сообщение от {self.sender.username} в {self.room.name}'

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    link = models.URLField(blank=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Уведомление для {self.user.username}'

class Rating(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('startup', 'user')
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

class Review(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, related_name='review')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class UserVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification')
    is_verified = models.BooleanField(default=False)
    verification_documents = models.FileField(upload_to='verification_docs/', null=True, blank=True)
    verification_date = models.DateTimeField(null=True, blank=True)
    verification_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Ожидает проверки'),
            ('approved', 'Подтверждено'),
            ('rejected', 'Отклонено')
        ],
        default='pending'
    )

    class Meta:
        verbose_name = 'Верификация пользователя'
        verbose_name_plural = 'Верификации пользователей'

class Analytics(models.Model):
    startup = models.OneToOneField(Startup, on_delete=models.CASCADE, related_name='analytics')
    views_count = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)
    investor_views = models.IntegerField(default=0)
    contact_requests = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Аналитика'
        verbose_name_plural = 'Аналитика'

class StartupMetrics(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='metrics')
    date = models.DateField(auto_now_add=True)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    customers = models.IntegerField(default=0)
    active_users = models.IntegerField(default=0)
    churn_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = 'Метрики стартапа'
        verbose_name_plural = 'Метрики стартапов'
        ordering = ['-date']

class Achievement(models.Model):
    ACHIEVEMENT_TYPES = [
        ('funding', 'Достижение цели по финансированию'),
        ('users', 'Достижение по количеству пользователей'),
        ('revenue', 'Достижение по выручке'),
        ('milestone', 'Достижение вехи проекта'),
        ('rating', 'Высокий рейтинг'),
        ('verification', 'Верификация'),
        ('custom', 'Пользовательское достижение')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='achievements', null=True, blank=True)
    type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES)
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)  # Имя иконки Bootstrap
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'
        ordering = ['-created_at']

class UserActivity(models.Model):
    ACTIVITY_TYPES = [
        ('login', 'Вход в систему'),
        ('startup_view', 'Просмотр стартапа'),
        ('investment', 'Инвестиция'),
        ('comment', 'Комментарий'),
        ('rating', 'Оценка'),
        ('message', 'Сообщение'),
        ('document', 'Работа с документами')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Активность пользователя'
        verbose_name_plural = 'Активность пользователей'
        ordering = ['-timestamp']

class LeaderboardEntry(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leaderboard_entry')
    points = models.IntegerField(default=0)
    investments_count = models.IntegerField(default=0)
    successful_startups = models.IntegerField(default=0)
    achievements_count = models.IntegerField(default=0)
    rank = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Запись таблицы лидеров'
        verbose_name_plural = 'Таблица лидеров'
        ordering = ['-points']
