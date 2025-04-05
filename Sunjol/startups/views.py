from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Startup, Investor, Investment, Vacancy, Milestone, Document, Update, TeamMember, Comment, ChatRoom, Message, Notification, Analytics, StartupMetrics, Achievement, LeaderboardEntry, UserActivity
from startups.forms import StartupForm, VacancyForm, InvestorProfileForm, RatingForm, ReviewForm, VerificationForm, UserProfileForm
from django.contrib.auth.models import User
import os
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

def home(request):
    latest_startups = Startup.objects.all().order_by('-created_at')[:6]
    return render(request, 'startups/home.html', {'latest_startups': latest_startups})

def startup_list(request):
    startups = Startup.objects.all()
    return render(request, 'startups/startup_list.html', {'startups': startups})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'startups/register.html', {'form': form})

@login_required
def create_startup(request):
    if request.method == 'POST':
        form = StartupForm(request.POST, request.FILES)
        if form.is_valid():
            startup = form.save(commit=False)
            startup.founder = request.user
            startup.save()
            return redirect('home')
    else:
        form = StartupForm()
    return render(request, 'startups/create_startup.html', {'form': form})

@login_required
def investor_dashboard(request):
    investor, created = Investor.objects.get_or_create(user=request.user)
    if created:
        return redirect('edit_investor_profile')
    investments = Investment.objects.filter(investor=investor)
    return render(request, 'startups/investor_dashboard.html', 
                 {'investor': investor, 'investments': investments})

@login_required
def create_vacancy(request, startup_id):
    startup = get_object_or_404(Startup, id=startup_id)
    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.startup = startup
            vacancy.save()
            return redirect('startup_detail', startup_id=startup.id)
    else:
        form = VacancyForm()
    return render(request, 'startups/create_vacancy.html', {'form': form, 'startup': startup})

@login_required
def investor_profile(request):
    investor, created = Investor.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = InvestorProfileForm(request.POST, request.FILES, instance=investor)
        if form.is_valid():
            form.save()
            return redirect('investor_dashboard')
    else:
        form = InvestorProfileForm(instance=investor)
    return render(request, 'startups/investor_profile.html', {'form': form})

@login_required
def edit_investor_profile(request):
    investor, created = Investor.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = InvestorProfileForm(request.POST, request.FILES, instance=investor)
        if form.is_valid():
            form.save()
            return redirect('investor_dashboard')
    else:
        form = InvestorProfileForm(instance=investor)
    return render(request, 'startups/edit_investor_profile.html', {'form': form})

@login_required
def make_investment(request, startup_id):
    startup = get_object_or_404(Startup, id=startup_id)
    investor = get_object_or_404(Investor, user=request.user)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount:
            investment = Investment.objects.create(
                investor=investor,
                startup=startup,
                amount=amount
            )
            startup.current_funding += float(amount)
            startup.save()
            return redirect('startup_detail', startup_id=startup.id)
    
    return render(request, 'startups/make_investment.html', {'startup': startup})

@login_required
def startup_detail(request, pk):
    startup = get_object_or_404(Startup, pk=pk)
    vacancies = Vacancy.objects.filter(startup=startup)
    return render(request, 'startups/startup_detail.html', 
                 {'startup': startup, 'vacancies': vacancies})

@login_required
def manage_vacancies(request, startup_id):
    startup = get_object_or_404(Startup, id=startup_id)
    vacancies = Vacancy.objects.filter(startup=startup)
    return render(request, 'startups/manage_vacancies.html', 
                 {'startup': startup, 'vacancies': vacancies})

@login_required
def delete_vacancy(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    startup_id = vacancy.startup.id
    vacancy.delete()
    return redirect('manage_vacancies', startup_id=startup_id)

@login_required
def profile(request, username=None):
    if username:
        # Просмотр профиля другого пользователя
        user = get_object_or_404(User, username=username)
        is_own_profile = False
    else:
        # Просмотр своего профиля
        user = request.user
        is_own_profile = True
    
    try:
        investor = Investor.objects.get(user=user)
    except Investor.DoesNotExist:
        investor = None
    
    try:
        startup = Startup.objects.get(founder=user)
    except Startup.DoesNotExist:
        startup = None
    
    return render(request, 'startups/profile.html', {
        'user': user,
        'investor': investor,
        'startup': startup,
        'is_own_profile': is_own_profile
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'startups/edit_profile.html', {'form': form})

@login_required
def settings(request):
    return render(request, 'startups/settings.html')

@login_required
def update_account(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Настройки аккаунта обновлены!')
            return redirect('settings')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'startups/update_account.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'startups/change_password.html', {'form': form})

@login_required
def update_notifications(request):
    if request.method == 'POST':
        investor = get_object_or_404(Investor, user=request.user)
        investor.email_notifications = 'email_notifications' in request.POST
        investor.investment_alerts = 'investment_alerts' in request.POST
        investor.startup_updates = 'startup_updates' in request.POST
        investor.save()
        messages.success(request, 'Настройки уведомлений обновлены!')
    return redirect('settings')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Ваш аккаунт был успешно удален.')
        return redirect('home')
    return render(request, 'startups/delete_account.html')

@login_required
def startup_edit(request, pk):
    startup = get_object_or_404(Startup, pk=pk)
    
    # Проверяем, является ли пользователь владельцем стартапа
    if request.user != startup.founder:
        messages.error(request, 'У вас нет прав для редактирования этого стартапа.')
        return redirect('startup_detail', pk=pk)
    
    if request.method == 'POST':
        form = StartupForm(request.POST, request.FILES, instance=startup)
        if form.is_valid():
            # Проверяем размер загружаемого файла
            if 'pitch_deck' in request.FILES:
                pitch_deck = request.FILES['pitch_deck']
                if pitch_deck.size > 10 * 1024 * 1024:  # 10MB
                    messages.error(request, 'Размер файла не должен превышать 10MB.')
                    return render(request, 'startups/startup_edit.html', {'form': form, 'startup': startup})
                
                # Проверяем расширение файла
                allowed_extensions = ['.pdf', '.ppt', '.pptx']
                file_ext = os.path.splitext(pitch_deck.name)[1].lower()
                if file_ext not in allowed_extensions:
                    messages.error(request, 'Поддерживаются только файлы PDF, PPT и PPTX.')
                    return render(request, 'startups/startup_edit.html', {'form': form, 'startup': startup})
            
            try:
                form.save()
                messages.success(request, 'Стартап успешно обновлен!')
                return redirect('startup_detail', pk=pk)
            except Exception as e:
                messages.error(request, f'Произошла ошибка при сохранении: {str(e)}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = StartupForm(instance=startup)
    
    return render(request, 'startups/startup_edit.html', {'form': form, 'startup': startup})

@login_required
def investment_history(request):
    investor = get_object_or_404(Investor, user=request.user)
    investments = Investment.objects.filter(investor=investor).order_by('-date_invested')
    return render(request, 'startups/investment_history.html', {'investments': investments})

@login_required
def startup_dashboard(request, pk):
    startup = get_object_or_404(Startup, pk=pk, founder=request.user)
    total_investments = Investment.objects.filter(startup=startup).aggregate(Sum('amount'))['amount__sum'] or 0
    active_vacancies = Vacancy.objects.filter(startup=startup).count()
    
    context = {
        'startup': startup,
        'total_investments': total_investments,
        'active_vacancies': active_vacancies,
        'recent_investments': Investment.objects.filter(startup=startup).order_by('-date_invested')[:5],
        'recent_applications': Vacancy.objects.filter(startup=startup).order_by('-id')[:5]
    }
    return render(request, 'startups/startup_dashboard.html', context)

@login_required
def startup_analytics(request, pk):
    startup = get_object_or_404(Startup, pk=pk, founder=request.user)
    investments = Investment.objects.filter(startup=startup)
    total_invested = investments.aggregate(Sum('amount'))['amount__sum'] or 0
    funding_progress = (total_invested / startup.funding_goal) * 100 if startup.funding_goal > 0 else 0
    
    context = {
        'startup': startup,
        'investments': investments,
        'total_invested': total_invested,
        'funding_progress': funding_progress,
        'investor_count': investments.values('investor').distinct().count()
    }
    return render(request, 'startups/startup_analytics.html', context)

@login_required
def startup_team(request, pk):
    startup = get_object_or_404(Startup, pk=pk, founder=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            username = request.POST.get('username')
            role = request.POST.get('role')
            try:
                user = User.objects.get(username=username)
                TeamMember.objects.create(
                    startup=startup,
                    user=user,
                    role=role
                )
                messages.success(request, f'Пользователь {username} добавлен в команду!')
            except User.DoesNotExist:
                messages.error(request, f'Пользователь {username} не найден.')
            except Exception as e:
                messages.error(request, f'Ошибка при добавлении пользователя: {str(e)}')
        elif action == 'remove':
            member_id = request.POST.get('member_id')
            try:
                member = TeamMember.objects.get(id=member_id, startup=startup)
                member.delete()
                messages.success(request, 'Участник команды удален.')
            except TeamMember.DoesNotExist:
                messages.error(request, 'Участник команды не найден.')
            except Exception as e:
                messages.error(request, f'Ошибка при удалении участника: {str(e)}')
    
    team_members = TeamMember.objects.filter(startup=startup)
    return render(request, 'startups/startup_team.html', {
        'startup': startup,
        'team_members': team_members
    })

@login_required
def startup_milestones(request, pk):
    startup = get_object_or_404(Startup, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        if title and description and due_date:
            Milestone.objects.create(
                startup=startup,
                title=title,
                description=description,
                due_date=due_date
            )
            messages.success(request, 'Веха успешно добавлена!')
    milestones = Milestone.objects.filter(startup=startup).order_by('due_date')
    return render(request, 'startups/startup_milestones.html', {'startup': startup, 'milestones': milestones})

@login_required
def startup_documents(request, pk):
    startup = get_object_or_404(Startup, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        document = request.FILES.get('document')
        if title and document:
            Document.objects.create(
                startup=startup,
                title=title,
                file=document
            )
            messages.success(request, 'Документ успешно загружен!')
    documents = Document.objects.filter(startup=startup)
    return render(request, 'startups/startup_documents.html', {'startup': startup, 'documents': documents})

@login_required
def startup_updates(request, pk):
    startup = get_object_or_404(Startup, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Update.objects.create(
                startup=startup,
                content=content
            )
            messages.success(request, 'Обновление успешно добавлено!')
    updates = Update.objects.filter(startup=startup).order_by('-created_at')
    return render(request, 'startups/startup_updates.html', {'startup': startup, 'updates': updates})

@login_required
def investment_portfolio(request):
    investor = get_object_or_404(Investor, user=request.user)
    investments = Investment.objects.filter(investor=investor)
    
    # Группируем инвестиции по стартапам
    portfolio = {}
    for investment in investments:
        if investment.startup not in portfolio:
            portfolio[investment.startup] = {
                'total_invested': 0,
                'investments': []
            }
        portfolio[investment.startup]['total_invested'] += float(investment.amount)
        portfolio[investment.startup]['investments'].append(investment)
    
    context = {
        'investor': investor,
        'portfolio': portfolio,
        'total_invested': sum(item['total_invested'] for item in portfolio.values())
    }
    return render(request, 'startups/investment_portfolio.html', context)

@login_required
def add_comment(request, startup_id):
    if request.method == 'POST':
        startup = get_object_or_404(Startup, id=startup_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.startup = startup
            comment.author = request.user
            comment.save()
            
            # Создаем уведомление для владельца стартапа
            if startup.owner != request.user:
                Notification.objects.create(
                    user=startup.owner,
                    message=f'Новый комментарий к вашему стартапу "{startup.name}" от {request.user.username}',
                    link=f'/startup/{startup.id}/'
                )
            
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.id,
                    'content': comment.content,
                    'author': comment.author.username,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
                    'parent_id': comment.parent_id
                }
            })
    return JsonResponse({'success': False})

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in room.participants.all():
        return redirect('startup_detail', pk=room.startup.id)
    
    messages = room.messages.all().order_by('timestamp')
    return render(request, 'startups/chat_room.html', {
        'room': room,
        'messages': messages
    })

@login_required
@require_POST
def send_message(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in room.participants.all():
        return JsonResponse({'success': False})
    
    form = MessageForm(request.POST)
    if form.is_valid():
        message = form.save(commit=False)
        message.room = room
        message.sender = request.user
        message.save()
        
        # Создаем уведомления для других участников чата
        for participant in room.participants.exclude(id=request.user.id):
            Notification.objects.create(
                user=participant,
                message=f'Новое сообщение в чате "{room.name}" от {request.user.username}',
                link=f'/chat/{room.id}/'
            )
        
        return JsonResponse({
            'success': True,
            'message': {
                'id': message.id,
                'content': message.content,
                'sender': message.sender.username,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M')
            }
        })
    return JsonResponse({'success': False})

@login_required
def notifications(request):
    notifications = request.user.notifications.all()
    unread_count = notifications.filter(is_read=False).count()
    
    if request.method == 'POST':
        notifications.update(is_read=True)
        return JsonResponse({'success': True})
    
    return render(request, 'startups/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'success': True})

@login_required
def add_rating(request, startup_id):
    startup = get_object_or_404(Startup, id=startup_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.startup = startup
            rating.user = request.user
            rating.save()
            return JsonResponse({'success': True, 'rating': rating.rating})
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
def add_review(request, startup_id):
    startup = get_object_or_404(Startup, id=startup_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.startup = startup
            review.user = request.user
            review.save()
            return JsonResponse({
                'success': True,
                'review': {
                    'content': review.content,
                    'user': review.user.username,
                    'created_at': review.created_at.strftime('%Y-%m-%d %H:%M')
                }
            })
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
def submit_verification(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST, request.FILES)
        if form.is_valid():
            verification = form.save(commit=False)
            verification.user = request.user
            verification.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
def verification(request):
    verification = getattr(request.user, 'verification', None)
    return render(request, 'startups/verification.html', {'verification': verification})

@login_required
def ratings(request, startup_id):
    startup = get_object_or_404(Startup, id=startup_id)
    return render(request, 'startups/ratings.html', {'startup': startup})

@login_required
def get_messages(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in [room.startup.user, room.investor.user]:
        return JsonResponse({'error': 'У вас нет доступа к этому чату'}, status=403)
    
    messages = Message.objects.filter(room=room).order_by('timestamp')
    messages_data = [{
        'id': msg.id,
        'content': msg.content,
        'sender': msg.sender.username,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M'),
        'is_sender': msg.sender == request.user
    } for msg in messages]
    
    return JsonResponse({'messages': messages_data})

@login_required
def mark_all_notifications_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Метод не поддерживается'}, status=405)

@login_required
def startup_analytics_dashboard(request, startup_id):
    startup = get_object_or_404(Startup, id=startup_id, founder=request.user)
    analytics, created = Analytics.objects.get_or_create(startup=startup)
    metrics = StartupMetrics.objects.filter(startup=startup).order_by('-date')[:30]
    
    # Подготовка данных для графиков
    dates = [metric.date.strftime('%d.%m') for metric in metrics]
    revenues = [float(metric.revenue) for metric in metrics]
    expenses = [float(metric.expenses) for metric in metrics]
    customers = [metric.customers for metric in metrics]
    active_users = [metric.active_users for metric in metrics]
    
    context = {
        'startup': startup,
        'analytics': analytics,
        'metrics': metrics,
        'chart_data': {
            'dates': dates,
            'revenues': revenues,
            'expenses': expenses,
            'customers': customers,
            'active_users': active_users
        }
    }
    return render(request, 'startups/analytics_dashboard.html', context)

@login_required
def update_metrics(request, startup_id):
    startup = get_object_or_404(Startup, id=startup_id, founder=request.user)
    if request.method == 'POST':
        form = StartupMetricsForm(request.POST)
        if form.is_valid():
            metrics = form.save(commit=False)
            metrics.startup = startup
            metrics.save()
            
            # Проверяем достижения
            check_metrics_achievements(startup, metrics)
            
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def achievements(request):
    user_achievements = Achievement.objects.filter(user=request.user)
    leaderboard = LeaderboardEntry.objects.all()[:10]
    
    context = {
        'achievements': user_achievements,
        'leaderboard': leaderboard,
        'total_points': sum(a.points for a in user_achievements)
    }
    return render(request, 'startups/achievements.html', context)

@login_required
def activity_log(request):
    activities = UserActivity.objects.filter(user=request.user).order_by('-timestamp')[:50]
    return render(request, 'startups/activity_log.html', {'activities': activities})

def check_metrics_achievements(startup, metrics):
    """Проверяет и выдает достижения на основе метрик"""
    user = startup.founder
    
    # Достижение за выручку
    if metrics.revenue >= 1000000:
        Achievement.objects.get_or_create(
            user=user,
            startup=startup,
            type='revenue',
            defaults={
                'title': 'Миллионер',
                'description': 'Достигнута выручка в 1 миллион рублей',
                'icon': 'bi-currency-dollar',
                'points': 100
            }
        )
    
    # Достижение за пользователей
    if metrics.active_users >= 1000:
        Achievement.objects.get_or_create(
            user=user,
            startup=startup,
            type='users',
            defaults={
                'title': 'Популярный стартап',
                'description': 'Более 1000 активных пользователей',
                'icon': 'bi-people',
                'points': 50
            }
        )
    
    # Обновляем таблицу лидеров
    entry, created = LeaderboardEntry.objects.get_or_create(user=user)
    entry.points = Achievement.objects.filter(user=user).aggregate(Sum('points'))['points__sum'] or 0
    entry.save()

def track_activity(user, activity_type, description, request=None):
    """Записывает активность пользователя"""
    ip_address = None
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
    
    UserActivity.objects.create(
        user=user,
        activity_type=activity_type,
        description=description,
        ip_address=ip_address
    )
