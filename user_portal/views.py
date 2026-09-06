from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from main.models import Notification
from .forms import UserAccountForm, UserProfileForm
from .models import UserProfile


def _profile(user):
    return UserProfile.objects.get_or_create(user=user)[0]


@login_required
def dashboard(request):
    profile = _profile(request.user)
    today = timezone.localdate()
    event_registrations = request.user.event_registrations.select_related('event')
    workshop_registrations = request.user.workshop_registrations.select_related('workshop')
    activities = request.user.activity_participations.select_related('activity')
    memberships = request.user.memberships.select_related('membership_type')
    return render(request, 'user_portal/dashboard.html', {
        'profile': profile,
        'event_count': event_registrations.count(),
        'workshop_count': workshop_registrations.count(),
        'activity_count': activities.count(),
        'certificate_count': request.user.certificates.count(),
        'membership': memberships.order_by('-created_at').first(),
        'unread_notification_count': request.user.notifications.filter(is_read=False).count(),
        'upcoming_events': event_registrations.filter(event__date__gte=today).exclude(status='cancelled').order_by('event__date')[:5],
        'recent_activities': activities.order_by('-activity__activity_date')[:5],
    })


@login_required
def profile(request):
    return render(request, 'user_portal/profile.html', {'profile': _profile(request.user)})


@login_required
def edit_profile(request):
    profile = _profile(request.user)
    account_form = UserAccountForm(request.POST or None, instance=request.user)
    profile_form = UserProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST' and account_form.is_valid() and profile_form.is_valid():
        account_form.save()
        profile_form.save()
        messages.success(request, 'Your profile has been updated.')
        return redirect('user_profile')
    return render(request, 'user_portal/edit_profile.html', {'account_form': account_form, 'profile_form': profile_form})


@login_required
def my_events(request):
    return render(request, 'user_portal/records.html', {'portal_title': 'My Events', 'record_type': 'events', 'records': request.user.event_registrations.select_related('event')})


@login_required
def my_workshops(request):
    return render(request, 'user_portal/records.html', {'portal_title': 'My Workshops', 'record_type': 'workshops', 'records': request.user.workshop_registrations.select_related('workshop')})


@login_required
def my_activities(request):
    return render(request, 'user_portal/records.html', {'portal_title': 'My Activities', 'record_type': 'activities', 'records': request.user.activity_participations.select_related('activity', 'activity__category')})


@login_required
def attendance(request):
    records = []
    records.extend({'kind': 'Event', 'title': r.event.title, 'date': r.event.date, 'attended': r.attended} for r in request.user.event_registrations.select_related('event'))
    records.extend({'kind': 'Workshop', 'title': r.workshop.title, 'date': r.workshop.date, 'attended': r.attended} for r in request.user.workshop_registrations.select_related('workshop'))
    records.extend({'kind': 'Activity', 'title': r.activity.title, 'date': r.activity.activity_date, 'attended': r.attended} for r in request.user.activity_participations.select_related('activity'))
    return render(request, 'user_portal/attendance.html', {'records': sorted(records, key=lambda item: item['date'], reverse=True)})


@login_required
def certificates(request):
    return render(request, 'user_portal/certificates.html', {'certificates': request.user.certificates.select_related('event', 'workshop', 'activity')})


@login_required
def memberships(request):
    return render(request, 'user_portal/memberships.html', {'memberships': request.user.memberships.select_related('membership_type')})


@login_required
def notifications(request):
    return render(request, 'user_portal/notifications.html', {'notifications': request.user.notifications.all()})


@login_required
@require_POST
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save(update_fields=['is_read'])
    return redirect('user_notifications')


@login_required
def settings(request):
    return render(request, 'user_portal/settings.html', {'profile': _profile(request.user)})


@login_required
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Your password has been changed.')
        return redirect('user_settings')
    return render(request, 'user_portal/change_password.html', {'form': form})


@login_required
def volunteer_points(request):
    return redirect('user_activities')
