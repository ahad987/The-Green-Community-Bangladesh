from django.contrib import messages
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import ContactForm, MembershipForm, RegisterForm
from .models import *

def page(request, title, objects=None, detail=None, form=None): return render(request, 'main/generic.html', {'title':title,'objects':objects,'detail':detail,'form':form})
def home(request): return render(request,'main/home.html',{'home_content':HomePageContent.objects.first(),'statistics':HomePageStatistic.objects.filter(active=True),'events':Event.objects.filter(active=True,status='upcoming')[:3],'news':News.objects.filter(active=True)[:3]})
def org_profile(request): return page(request,'About Us',detail=OrganizationProfile.objects.first())
def board_members(request): return page(request,'Board of Members',BoardMember.objects.filter(active=True))
def exec_committee(request): return page(request,'Executive Committee',ExecutiveCommitteeMember.objects.filter(active=True))
def listing(request,title,model,**filters):
    qs=model.objects.filter(active=True,**filters); qs=qs if qs.ordered else qs.order_by('pk'); q=request.GET.get('q','').strip()
    if q: qs=qs.filter(title__icontains=q)
    return page(request,title,Paginator(qs,9).get_page(request.GET.get('page')))
def events_list(request): return listing(request,'Events',Event)
def events_upcoming(request): return listing(request,'Upcoming Events',Event,status='upcoming')
def events_ongoing(request): return listing(request,'Ongoing Events',Event,status='ongoing')
def events_completed(request): return listing(request,'Completed Events',Event,status='completed')
def event_details(request,slug=None): return page(request,'Event details',detail=get_object_or_404(Event,slug=slug,active=True)) if slug else redirect('events_list')
@login_required
def event_register(request,slug):
    event=get_object_or_404(Event,slug=slug,active=True,registration_enabled=True)
    if request.method=='POST':
        if event.status not in (Event.Status.UPCOMING, Event.Status.ONGOING): messages.error(request,'This event is no longer accepting registrations.')
        elif event.registration_deadline and timezone.now() > event.registration_deadline: messages.error(request,'The registration deadline has passed.')
        elif event.capacity and event.registrations.exclude(status=EventRegistration.Status.CANCELLED).count() >= event.capacity: messages.error(request,'This event is already at capacity.')
        else:
            try: EventRegistration.objects.create(user=request.user,event=event); messages.success(request,'Your event registration has been submitted.')
            except IntegrityError: messages.info(request,'You are already registered for this event.')
        return redirect('user_events')
    return page(request,f'Register: {event.title}',detail=event,form=True)
def workshops_list(request): return listing(request,'Workshops',Workshop)
def workshop_details(request,slug=None): return page(request,'Workshop details',detail=get_object_or_404(Workshop,slug=slug,active=True)) if slug else redirect('workshops_list')
@login_required
def workshop_register(request,slug):
    workshop=get_object_or_404(Workshop,slug=slug,active=True,registration_enabled=True)
    if request.method=='POST':
        if workshop.status.lower() in ('completed', 'cancelled', 'closed'): messages.error(request,'This workshop is no longer accepting registrations.')
        elif workshop.capacity and workshop.registrations.exclude(status=WorkshopRegistration.Status.CANCELLED).count() >= workshop.capacity: messages.error(request,'This workshop is already at capacity.')
        else:
            try: WorkshopRegistration.objects.create(user=request.user,workshop=workshop); messages.success(request,'Your workshop registration has been submitted.')
            except IntegrityError: messages.info(request,'You are already registered for this workshop.')
        return redirect('user_workshops')
    return page(request,f'Register: {workshop.title}',detail=workshop,form=True)
def awareness_home(request): return listing(request,'Environmental Awareness',AwarenessArticle)
def awareness_category(request,category): return listing(request,f'Awareness: {category}',AwarenessArticle,category__slug=category)
def awareness_details(request,slug): return page(request,'Awareness article',detail=get_object_or_404(AwarenessArticle,slug=slug,active=True))
def volunteer_home(request): return listing(request,'Volunteer Activities',VolunteerActivity)
def volunteer_category(request,category): return listing(request,f'Volunteer: {category}',VolunteerActivity,category__slug=category)
def volunteer_details(request,slug=None):
    if not slug: return redirect('volunteer_home')
    activity=get_object_or_404(VolunteerActivity,slug=slug,active=True)
    joined=request.user.is_authenticated and activity.participants.filter(user=request.user).exists()
    return render(request,'main/generic.html',{'title':'Volunteer activity','detail':activity,'activity_registration':True,'joined':joined})
@login_required
@require_POST
def volunteer_register(request,slug):
    activity=get_object_or_404(VolunteerActivity,slug=slug,active=True)
    if activity.status.lower() in ('completed','cancelled','closed'):
        messages.error(request,'This activity is no longer accepting participants.')
    else:
        _record, created=VolunteerActivityParticipant.objects.get_or_create(user=request.user,activity=activity)
        messages.success(request,'You joined this volunteer activity.') if created else messages.info(request,'You already joined this activity.')
    return redirect('user_activities')
def gallery_albums(request): return listing(request,'Gallery',GalleryAlbum)
def gallery_photos(request,slug=None):
    album=get_object_or_404(GalleryAlbum,slug=slug,active=True) if slug else None
    return page(request,'Gallery photos',album.images.all() if album else GalleryImage.objects.all(),detail=album)
def gallery_videos(request): return page(request,'Gallery videos',GalleryVideo.objects.all())
def news_list(request): return listing(request,'News',News)
def news_details(request,slug=None): return page(request,'News',detail=get_object_or_404(News,slug=slug,active=True)) if slug else redirect('news_list')
def media_coverage(request): return listing(request,'Media coverage',News)
def success_stories(request): return listing(request,'Success stories',News)
def membership_home(request): return page(request,'Membership',MembershipType.objects.filter(active=True))
def membership_student(request): return page(request,'Student Membership',MembershipType.objects.filter(active=True,name__icontains='student'))
def membership_general(request): return page(request,'General Membership',MembershipType.objects.filter(active=True,name__icontains='general'))
def membership_lifetime(request): return page(request,'Lifetime Membership',MembershipType.objects.filter(active=True,name__icontains='lifetime'))
@login_required
def membership_register(request):
    form=MembershipForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        membership_type=form.cleaned_data['membership_type']
        if Membership.objects.filter(user=request.user,membership_type=membership_type,status__in=[Membership.Status.PENDING,Membership.Status.APPROVED]).exists():
            messages.info(request,'You already have a pending or approved application for this membership type.'); return redirect('user_memberships')
        membership=form.save(commit=False); membership.user=request.user; membership.save(); messages.success(request,'Your membership application is pending review.'); return redirect('user_dashboard')
    return page(request,'Membership registration',form=form)
def contact(request):
    form=ContactForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Thank you. Your message has been received.'); return redirect('contact')
    return page(request,'Contact us',detail=SiteSettings.objects.first(),form=form)
def faq(request): return page(request,'Frequently asked questions',FAQ.objects.filter(active=True))
def privacy_policy(request): return page(request,'Privacy policy')
def terms(request): return page(request,'Terms and conditions')
def login(request):
    if request.user.is_authenticated: return redirect('user_dashboard')
    form=AuthenticationForm(request,data=request.POST or None)
    if request.method=='POST' and form.is_valid(): auth_login(request,form.get_user()); return redirect('admin_dashboard' if form.get_user().is_staff else 'user_dashboard')
    return page(request,'Login',form=form)
def register(request):
    form=RegisterForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): user=form.save(); auth_login(request,user); messages.success(request,'Welcome to TGCB.'); return redirect('user_dashboard')
    return page(request,'Create an account',form=form)
def forgot_password(request): return page(request,'Password reset')
def reset_password(request): return page(request,'Set a new password')
@login_required
def change_password(request):
    from django.contrib.auth.forms import PasswordChangeForm
    from django.contrib.auth import update_session_auth_hash
    form=PasswordChangeForm(request.user,request.POST or None)
    if request.method=='POST' and form.is_valid():
        user=form.save(); update_session_auth_hash(request,user); messages.success(request,'Password updated.'); return redirect('user_dashboard')
    return page(request,'Change password',form=form)
def logout_view(request): logout(request); messages.success(request,'You have been signed out.'); return redirect('home')
def certificate_verify(request,code): return page(request,'Certificate verification',detail=get_object_or_404(Certificate,verification_code=code,status='active'))
