from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='user_dashboard'),
    path('profile/', views.profile, name='user_profile'),
    path('edit-profile/', views.edit_profile, name='user_edit_profile'),
    path('events/', views.my_events, name='user_events'),
    path('workshops/', views.my_workshops, name='user_workshops'),
    path('activities/', views.my_activities, name='user_activities'),
    path('attendance/', views.attendance, name='user_attendance'),
    path('certificates/', views.certificates, name='user_certificates'),
    path('memberships/', views.memberships, name='user_memberships'),
    path('notifications/', views.notifications, name='user_notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='user_notification_read'),
    path('settings/', views.settings, name='user_settings'),
    path('change-password/', views.change_password, name='user_change_password'),
]
