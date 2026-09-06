from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # About
    path('about/profile/', views.org_profile, name='org_profile'),
    path('about/board/', views.board_members, name='board_members'),
    path('about/committee/', views.exec_committee, name='exec_committee'),
    
    # Activities
    path('events/', views.events_list, name='events_list'),
    path('events/upcoming/', views.events_upcoming, name='events_upcoming'),
    path('events/ongoing/', views.events_ongoing, name='events_ongoing'),
    path('events/completed/', views.events_completed, name='events_completed'),
    path('events/details/', views.event_details, name='event_details'),
    path('events/<slug:slug>/', views.event_details, name='event_detail'),
    path('events/<slug:slug>/register/', views.event_register, name='event_register'),
    
    path('workshops/', views.workshops_list, name='workshops_list'),
    path('workshops/details/', views.workshop_details, name='workshop_details'),
    path('workshops/<slug:slug>/', views.workshop_details, name='workshop_detail'),
    path('workshops/<slug:slug>/register/', views.workshop_register, name='workshop_register'),
    
    path('awareness/', views.awareness_home, name='awareness_home'),
    path('awareness/<str:category>/', views.awareness_category, name='awareness_category'),
    path('awareness/article/<slug:slug>/', views.awareness_details, name='awareness_detail'),
    
    path('volunteer/', views.volunteer_home, name='volunteer_home'),
    path('volunteer/<str:category>/', views.volunteer_category, name='volunteer_category'),
    path('volunteer/details/', views.volunteer_details, name='volunteer_details'),
    path('volunteer/activity/<slug:slug>/', views.volunteer_details, name='volunteer_detail'),
    path('volunteer/activity/<slug:slug>/join/', views.volunteer_register, name='volunteer_register'),
    
    # Archive
    path('gallery/albums/', views.gallery_albums, name='gallery_albums'),
    path('gallery/photos/', views.gallery_photos, name='gallery_photos'),
    path('gallery/videos/', views.gallery_videos, name='gallery_videos'),
    path('gallery/<slug:slug>/', views.gallery_photos, name='gallery_album'),
    
    path('news/', views.news_list, name='news_list'),
    path('news/details/', views.news_details, name='news_details'),
    path('news/media/', views.media_coverage, name='media_coverage'),
    path('news/stories/', views.success_stories, name='success_stories'),
    path('news/<slug:slug>/', views.news_details, name='news_detail'),
    
    # Membership
    path('membership/', views.membership_home, name='membership_home'),
    path('membership/student/', views.membership_student, name='membership_student'),
    path('membership/general/', views.membership_general, name='membership_general'),
    path('membership/lifetime/', views.membership_lifetime, name='membership_lifetime'),
    path('membership/register/', views.membership_register, name='membership_register'),
    
    # Contact & Auth (Frontend Only)
    path('contact/', views.contact, name='contact'),
    path('contact/faq/', views.faq, name='faq'),
    path('contact/privacy/', views.privacy_policy, name='privacy_policy'),
    path('contact/terms/', views.terms, name='terms'),
    
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('change-password/', views.change_password, name='change_password'),
    path('logout/', views.logout_view, name='logout'),
    path('certificates/verify/<uuid:code>/', views.certificate_verify, name='certificate_verify'),
]
