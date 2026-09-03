from django.shortcuts import render

def dashboard(request): return render(request, 'user_portal/dashboard.html')
def profile(request): return render(request, 'user_portal/profile.html')
def edit_profile(request): return render(request, 'user_portal/edit_profile.html')
def my_events(request): return render(request, 'user_portal/my_events.html')
def my_workshops(request): return render(request, 'user_portal/my_workshops.html')
def my_activities(request): return render(request, 'user_portal/my_activities.html')
def attendance(request): return render(request, 'user_portal/attendance.html')
def certificates(request): return render(request, 'user_portal/certificates.html')
def volunteer_points(request): return render(request, 'user_portal/volunteer_points.html')
def notifications(request): return render(request, 'user_portal/notifications.html')
def settings(request): return render(request, 'user_portal/settings.html')