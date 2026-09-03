from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='admin_dashboard'),
    path('users/', views.user_management, name='admin_users'),
    path('volunteers/', views.volunteer_management, name='admin_volunteers'),
    path('memberships/', views.membership_management, name='admin_memberships'),
    path('events/', views.event_management, name='admin_events'),
    path('workshops/', views.workshop_management, name='admin_workshops'),
    path('activities/', views.activity_management, name='admin_activities'),
    path('gallery/', views.gallery_management, name='admin_gallery'),
    path('news/', views.news_management, name='admin_news'),
    path('board/', views.board_management, name='admin_board'),
    path('committee/', views.committee_management, name='admin_committee'),
    path('certificates/', views.certificate_management, name='admin_certificates'),
    path('reports/', views.reports, name='admin_reports'),
    path('notifications/', views.admin_notifications, name='admin_notifications'),
    path('settings/', views.website_settings, name='admin_settings'),
    path('audit-logs/', views.audit_logs, name='admin_audit_logs'),
    path('profile/', views.admin_profile, name='admin_profile'),
    path('change-password/', views.admin_change_password, name='admin_change_password'),
    path('login/', views.admin_login, name='admin_login'),
]