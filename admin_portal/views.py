from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from .forms import (ActivityForm, ActivityParticipantForm, AwarenessForm, BoardMemberForm,
                    CertificateForm, CommitteeMemberForm, EventForm, EventRegistrationForm,
                    GalleryAlbumForm, MembershipForm, NewsForm, NotificationForm,
                    WorkshopForm, WorkshopRegistrationForm)
from main.models import (AuditLog, AwarenessArticle, BoardMember, Certificate, Event, EventRegistration,
                         ExecutiveCommitteeMember, GalleryAlbum, Membership, News, Notification,
                         SiteSettings, VolunteerActivity, VolunteerActivityParticipant, Workshop,
                         WorkshopRegistration)

staff_required = user_passes_test(lambda user: user.is_staff, login_url='admin_login')

CRUD = {
    'event': (Event, EventForm, 'admin_events'), 'workshop': (Workshop, WorkshopForm, 'admin_workshops'),
    'activity': (VolunteerActivity, ActivityForm, 'admin_activities'), 'awareness': (AwarenessArticle, AwarenessForm, 'admin_awareness'),
    'news': (News, NewsForm, 'admin_news'), 'gallery': (GalleryAlbum, GalleryAlbumForm, 'admin_gallery'),
    'board': (BoardMember, BoardMemberForm, 'admin_board'), 'committee': (ExecutiveCommitteeMember, CommitteeMemberForm, 'admin_committee'),
    'membership': (Membership, MembershipForm, 'admin_memberships'), 'certificate': (Certificate, CertificateForm, 'admin_certificates'),
    'notification': (Notification, NotificationForm, 'admin_notifications'),
    'event-registration': (EventRegistration, EventRegistrationForm, 'admin_event_registrations'),
    'workshop-registration': (WorkshopRegistration, WorkshopRegistrationForm, 'admin_workshop_registrations'),
    'participant': (VolunteerActivityParticipant, ActivityParticipantForm, 'admin_volunteers'),
}

def _crud_config(entity):
    if entity not in CRUD: raise PermissionDenied
    return CRUD[entity]

def _require_model_permission(user, model, action):
    permission = f'{model._meta.app_label}.{action}_{model._meta.model_name}'
    if not (user.is_superuser or user.has_perm(permission)): raise PermissionDenied


def _list(request, title, kind, queryset, admin_url, search_fields=(), status_field=None, entity=None):
    query = request.GET.get('q', '').strip()
    if query and search_fields:
        search = Q()
        for field in search_fields:
            search |= Q(**{f'{field}__icontains': query})
        queryset = queryset.filter(search)
    selected_status = request.GET.get('status', '').strip()
    if selected_status and status_field:
        queryset = queryset.filter(**{status_field: selected_status})
    return render(request, 'admin_portal/management_list.html', {
        'admin_title': title, 'kind': kind, 'page_obj': Paginator(queryset, 20).get_page(request.GET.get('page')),
        'query': query, 'selected_status': selected_status, 'admin_url': admin_url, 'entity': entity,
        'create_url': reverse('admin_crud_create', args=[entity]) if entity else '',
    })


@staff_required
def dashboard(request):
    return render(request, 'admin_portal/dashboard.html', {
        'user_count': User.objects.count(),
        'volunteer_count': User.objects.filter(activity_participations__isnull=False).distinct().count(),
        'membership_count': Membership.objects.count(),
        'pending_membership_count': Membership.objects.filter(status=Membership.Status.PENDING).count(),
        'upcoming_event_count': Event.objects.filter(status=Event.Status.UPCOMING, active=True).count(),
        'workshop_count': Workshop.objects.filter(active=True).count(),
        'activity_count': VolunteerActivity.objects.filter(active=True).count(),
        'pending_registration_count': EventRegistration.objects.filter(status=EventRegistration.Status.PENDING).count() + WorkshopRegistration.objects.filter(status=WorkshopRegistration.Status.PENDING).count(),
        'certificate_count': Certificate.objects.count(),
        'recent_users': User.objects.order_by('-date_joined')[:8],
    })


@staff_required
def user_management(request): return _list(request, 'Users', 'users', User.objects.order_by('-date_joined'), reverse('admin:auth_user_changelist'), ('username', 'email', 'first_name', 'last_name'))
@staff_required
def volunteer_management(request): return _list(request, 'Volunteer Participation', 'participants', VolunteerActivityParticipant.objects.select_related('user', 'activity').order_by('-created_at'), reverse('admin:main_volunteeractivityparticipant_changelist'), ('user__username', 'user__email', 'activity__title'), 'status', 'participant')
@staff_required
def membership_management(request): return _list(request, 'Membership Applications', 'memberships', Membership.objects.select_related('user', 'membership_type').order_by('-created_at'), reverse('admin:main_membership_changelist'), ('user__username', 'user__email', 'membership_id', 'membership_type__name'), 'status', 'membership')
@staff_required
def event_management(request): return _list(request, 'Events', 'events', Event.objects.order_by('-date'), reverse('admin:main_event_changelist'), ('title', 'venue'), 'status', 'event')
@staff_required
def workshop_management(request): return _list(request, 'Workshops', 'workshops', Workshop.objects.order_by('-date'), reverse('admin:main_workshop_changelist'), ('title', 'venue', 'speaker'), 'status', 'workshop')
@staff_required
def activity_management(request): return _list(request, 'Volunteer Activities', 'activities', VolunteerActivity.objects.select_related('category').order_by('-activity_date'), reverse('admin:main_volunteeractivity_changelist'), ('title', 'location', 'category__name'), 'status', 'activity')
@staff_required
def awareness_management(request): return _list(request, 'Awareness Articles', 'awareness', AwarenessArticle.objects.select_related('category').order_by('-published_date'), reverse('admin:main_awarenessarticle_changelist'), ('title', 'category__name'), entity='awareness')
@staff_required
def gallery_management(request): return _list(request, 'Gallery Albums', 'gallery', GalleryAlbum.objects.order_by('-created_at'), reverse('admin:main_galleryalbum_changelist'), ('title', 'description'), entity='gallery')
@staff_required
def news_management(request): return _list(request, 'News', 'news', News.objects.select_related('category').order_by('-published_date'), reverse('admin:main_news_changelist'), ('title', 'category__name'), entity='news')
@staff_required
def board_management(request): return _list(request, 'Board Members', 'people', BoardMember.objects.all(), reverse('admin:main_boardmember_changelist'), ('name', 'designation'), entity='board')
@staff_required
def committee_management(request): return _list(request, 'Executive Committee', 'people', ExecutiveCommitteeMember.objects.all(), reverse('admin:main_executivecommitteemember_changelist'), ('name', 'designation'), entity='committee')
@staff_required
def certificate_management(request): return _list(request, 'Certificates', 'certificates', Certificate.objects.select_related('user').order_by('-issue_date'), reverse('admin:main_certificate_changelist'), ('title', 'certificate_number', 'user__username'), entity='certificate')
@staff_required
def event_registrations(request): return _list(request, 'Event Registrations', 'event_registrations', EventRegistration.objects.select_related('user', 'event').order_by('-created_at'), reverse('admin:main_eventregistration_changelist'), ('user__username', 'event__title'), 'status', 'event-registration')
@staff_required
def workshop_registrations(request): return _list(request, 'Workshop Registrations', 'workshop_registrations', WorkshopRegistration.objects.select_related('user', 'workshop').order_by('-created_at'), reverse('admin:main_workshopregistration_changelist'), ('user__username', 'workshop__title'), 'status', 'workshop-registration')
@staff_required
def reports(request): return _list(request, 'Audit Logs', 'audit_logs', AuditLog.objects.select_related('user').all(), reverse('admin:main_auditlog_changelist'), ('action', 'detail', 'user__username'))
@staff_required
def admin_notifications(request): return _list(request, 'Notifications', 'notifications', Notification.objects.select_related('user').all(), reverse('admin:main_notification_changelist'), ('title', 'message', 'user__username'), entity='notification')
@staff_required
def website_settings(request): return _list(request, 'Website Settings', 'settings', SiteSettings.objects.order_by('pk'), reverse('admin:main_sitesettings_changelist'), ('site_name', 'email'))
@staff_required
def audit_logs(request): return reports(request)

@staff_required
def crud_create(request, entity):
    model, form_class, list_url = _crud_config(entity); _require_model_permission(request.user, model, 'add')
    form = form_class(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(); AuditLog.objects.create(user=request.user, action=f'Created {model._meta.verbose_name}', detail=str(obj))
        messages.success(request, f'{model._meta.verbose_name.title()} created successfully.'); return redirect(list_url)
    return render(request, 'admin_portal/crud_form.html', {'form': form, 'admin_title': f'Add {model._meta.verbose_name}', 'cancel_url': reverse(list_url)})

@staff_required
def crud_edit(request, entity, pk):
    model, form_class, list_url = _crud_config(entity); _require_model_permission(request.user, model, 'change')
    obj = get_object_or_404(model, pk=pk); form = form_class(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(); AuditLog.objects.create(user=request.user, action=f'Updated {model._meta.verbose_name}', detail=str(obj))
        messages.success(request, f'{model._meta.verbose_name.title()} updated successfully.'); return redirect(list_url)
    return render(request, 'admin_portal/crud_form.html', {'form': form, 'admin_title': f'Edit {model._meta.verbose_name}', 'cancel_url': reverse(list_url), 'object': obj})

@staff_required
@require_POST
def crud_delete(request, entity, pk):
    model, _form_class, list_url = _crud_config(entity); _require_model_permission(request.user, model, 'delete')
    obj = get_object_or_404(model, pk=pk); description = str(obj); obj.delete()
    AuditLog.objects.create(user=request.user, action=f'Deleted {model._meta.verbose_name}', detail=description)
    messages.success(request, f'{model._meta.verbose_name.title()} deleted.'); return redirect(list_url)
@staff_required
def admin_profile(request): return render(request, 'admin_portal/profile.html')
@staff_required
def admin_change_password(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(); update_session_auth_hash(request, user); messages.success(request, 'Password updated.'); return redirect('admin_profile')
    return render(request, 'admin_portal/change_password.html', {'form': form})


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff: return redirect('admin_dashboard')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        if user.is_staff:
            login(request, user); return redirect('admin_dashboard')
        messages.error(request, 'This account is not authorised for the admin portal.')
    return render(request, 'admin_portal/login.html', {'form': form})
