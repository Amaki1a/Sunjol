from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('startups/', views.startup_list, name='startup_list'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='startups/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('create-startup/', views.create_startup, name='create_startup'),
    path('investor-dashboard/', views.investor_dashboard, name='investor_dashboard'),
    path('create-vacancy/<int:startup_id>/', views.create_vacancy, name='create_vacancy'),
    path('edit-investor-profile/', views.edit_investor_profile, name='edit_investor_profile'),
    path('investor-profile/', views.investor_profile, name='investor_profile'),
    path('make-investment/<int:startup_id>/', views.make_investment, name='make_investment'),
    
    # Профиль пользователя
    path('accounts/profile/', views.profile, name='accounts_profile'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    
    # Стартапы
    path('startup/<int:pk>/', views.startup_detail, name='startup_detail'),
    path('startup/<int:pk>/edit/', views.startup_edit, name='startup_edit'),
    path('startup/<int:pk>/dashboard/', views.startup_dashboard, name='startup_dashboard'),
    path('startup/<int:pk>/analytics/', views.startup_analytics, name='startup_analytics'),
    path('startup/<int:pk>/team/', views.startup_team, name='startup_team'),
    path('startup/<int:pk>/milestones/', views.startup_milestones, name='startup_milestones'),
    path('startup/<int:pk>/documents/', views.startup_documents, name='startup_documents'),
    path('startup/<int:pk>/updates/', views.startup_updates, name='startup_updates'),
    path('startup/<int:startup_id>/vacancy/create/', views.create_vacancy, name='create_vacancy'),
    path('startup/<int:startup_id>/vacancies/', views.manage_vacancies, name='manage_vacancies'),
    path('vacancy/<int:vacancy_id>/delete/', views.delete_vacancy, name='delete_vacancy'),
    path('investments/history/', views.investment_history, name='investment_history'),
    path('investments/portfolio/', views.investment_portfolio, name='investment_portfolio'),
    
    # Комментарии
    path('startup/<int:startup_id>/comment/', views.add_comment, name='add_comment'),
    
    # Чат
    path('chat/<int:room_id>/', views.chat_room, name='chat_room'),
    path('chat/<int:room_id>/send/', views.send_message, name='send_message'),
    path('chat/<int:room_id>/messages/', views.get_messages, name='get_messages'),
    
    # Уведомления
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    
    # Рейтинги и отзывы
    path('startup/<int:startup_id>/rating/', views.add_rating, name='add_rating'),
    path('startup/<int:startup_id>/review/', views.add_review, name='add_review'),
    path('verification/submit/', views.submit_verification, name='submit_verification'),
    path('verification/', views.verification, name='verification'),
    path('startup/<int:startup_id>/ratings/', views.ratings, name='ratings'),
    
    # Аналитика и статистика
    path('startup/<int:startup_id>/analytics/', views.startup_analytics_dashboard, name='startup_analytics'),
    path('startup/<int:startup_id>/metrics/update/', views.update_metrics, name='update_metrics'),
    path('achievements/', views.achievements, name='achievements'),
    path('activity/', views.activity_log, name='activity_log'),
    
    # Настройки
    path('settings/', views.settings, name='settings'),
    path('settings/update-account/', views.update_account, name='update_account'),
    path('settings/update-notifications/', views.update_notifications, name='update_notifications'),
    path('settings/delete-account/', views.delete_account, name='delete_account'),
]