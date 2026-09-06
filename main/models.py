import uuid
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: abstract = True


class SiteSettings(TimeStampedModel):
    site_name = models.CharField(max_length=150, default='The Green Community Bangladesh'); tagline = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='branding/', blank=True); favicon = models.ImageField(upload_to='branding/', blank=True)
    email = models.EmailField(blank=True); phone = models.CharField(max_length=40, blank=True); address = models.TextField(blank=True); footer_text = models.TextField(blank=True)
    facebook_url = models.URLField(blank=True); youtube_url = models.URLField(blank=True); instagram_url = models.URLField(blank=True); linkedin_url = models.URLField(blank=True)
    def save(self, *args, **kwargs): self.pk = 1; super().save(*args, **kwargs)
    def __str__(self): return self.site_name

class HomePageContent(TimeStampedModel):
    hero_title=models.CharField(max_length=255,default='Together for a Sustainable Future'); hero_subtitle=models.CharField(max_length=255,blank=True); hero_description=models.TextField(blank=True); hero_image=models.ImageField(upload_to='home/',blank=True)
    about_title=models.CharField(max_length=255,default='Who We Are'); about_text=models.TextField(blank=True); about_image=models.ImageField(upload_to='home/',blank=True)
    def save(self,*args,**kwargs): self.pk=1; super().save(*args,**kwargs)
    def __str__(self): return 'Homepage content'
class HomePageStatistic(models.Model):
    title=models.CharField(max_length=100); value=models.CharField(max_length=40); icon=models.CharField(max_length=80,blank=True); ordering=models.PositiveIntegerField(default=0); active=models.BooleanField(default=True)
    class Meta: ordering=['ordering','id']
    def __str__(self): return self.title
class OrganizationProfile(TimeStampedModel):
    title=models.CharField(max_length=255,default='About The Green Community Bangladesh'); content=models.TextField(blank=True); image=models.ImageField(upload_to='organization/',blank=True); history=models.TextField(blank=True); mission=models.TextField(blank=True); vision=models.TextField(blank=True); objectives=models.TextField(blank=True); founder_message=models.TextField(blank=True)
    def save(self,*args,**kwargs): self.pk=1; super().save(*args,**kwargs)
    def __str__(self): return self.title
class Person(models.Model):
    name=models.CharField(max_length=150); designation=models.CharField(max_length=150); photo=models.ImageField(upload_to='people/',blank=True); biography=models.TextField(blank=True); email=models.EmailField(blank=True); facebook_url=models.URLField(blank=True); linkedin_url=models.URLField(blank=True); display_order=models.PositiveIntegerField(default=0); active=models.BooleanField(default=True)
    class Meta: abstract=True; ordering=['display_order','name']
    def __str__(self): return f'{self.name} — {self.designation}'
class BoardMember(Person): pass
class ExecutiveCommitteeMember(Person): pass

class NamedCategory(models.Model):
    name=models.CharField(max_length=100,unique=True); slug=models.SlugField(unique=True,blank=True)
    class Meta: abstract=True; ordering=['name']
    def save(self,*args,**kwargs):
        if not self.slug: self.slug=slugify(self.name)
        super().save(*args,**kwargs)
    def __str__(self): return self.name
class EventCategory(NamedCategory): pass
class WorkshopCategory(NamedCategory): pass
class AwarenessCategory(NamedCategory): pass
class VolunteerActivityCategory(NamedCategory): pass
class NewsCategory(NamedCategory): pass
class SluggedContent(TimeStampedModel):
    title=models.CharField(max_length=255); slug=models.SlugField(unique=True,blank=True); description=models.TextField(); featured_image=models.ImageField(upload_to='content/',blank=True); featured=models.BooleanField(default=False); active=models.BooleanField(default=True)
    class Meta: abstract=True
    def save(self,*args,**kwargs):
        if not self.slug:
            base=slugify(self.title) or 'item'; candidate=base; counter=2
            while type(self).objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate=f'{base}-{counter}'; counter+=1
            self.slug=candidate
        super().save(*args,**kwargs)
    def __str__(self): return self.title
class Event(SluggedContent):
    class Status(models.TextChoices): UPCOMING='upcoming','Upcoming'; ONGOING='ongoing','Ongoing'; COMPLETED='completed','Completed'; CANCELLED='cancelled','Cancelled'
    category=models.ForeignKey(EventCategory,null=True,blank=True,on_delete=models.SET_NULL,related_name='events'); date=models.DateField(); start_time=models.TimeField(blank=True,null=True); end_time=models.TimeField(blank=True,null=True); venue=models.CharField(max_length=200); address=models.TextField(blank=True); registration_enabled=models.BooleanField(default=True); registration_deadline=models.DateTimeField(blank=True,null=True); capacity=models.PositiveIntegerField(blank=True,null=True,validators=[MinValueValidator(1)]); status=models.CharField(max_length=12,choices=Status.choices,default=Status.UPCOMING)
    class Meta: ordering=['date','start_time']
class Workshop(SluggedContent):
    category=models.ForeignKey(WorkshopCategory,null=True,blank=True,on_delete=models.SET_NULL,related_name='workshops'); date=models.DateField(); time=models.TimeField(blank=True,null=True); venue=models.CharField(max_length=200); speaker=models.CharField(max_length=200,blank=True); registration_enabled=models.BooleanField(default=True); capacity=models.PositiveIntegerField(blank=True,null=True); status=models.CharField(max_length=20,default='upcoming')
    class Meta: ordering=['date','time']
class AwarenessArticle(SluggedContent):
    category=models.ForeignKey(AwarenessCategory,on_delete=models.PROTECT,related_name='articles'); summary=models.TextField(blank=True); content=models.TextField(); author=models.CharField(max_length=150,blank=True); published_date=models.DateField()
    class Meta: ordering=['-published_date']
class VolunteerActivity(SluggedContent):
    category=models.ForeignKey(VolunteerActivityCategory,null=True,blank=True,on_delete=models.SET_NULL,related_name='activities'); location=models.CharField(max_length=200); activity_date=models.DateField(); impact_summary=models.TextField(blank=True); status=models.CharField(max_length=20,default='upcoming')
    class Meta: ordering=['-activity_date']
class News(SluggedContent):
    category=models.ForeignKey(NewsCategory,null=True,blank=True,on_delete=models.SET_NULL,related_name='news'); summary=models.TextField(blank=True); content=models.TextField(); author=models.CharField(max_length=150,blank=True); published_date=models.DateField()
    class Meta: ordering=['-published_date']
class EventRegistration(TimeStampedModel):
    class Status(models.TextChoices): PENDING='pending','Pending'; APPROVED='approved','Approved'; CANCELLED='cancelled','Cancelled'
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='event_registrations'); event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name='registrations'); status=models.CharField(max_length=12,choices=Status.choices,default=Status.PENDING); attended=models.BooleanField(default=False)
    class Meta: constraints=[models.UniqueConstraint(fields=['user','event'],name='unique_event_registration')]; ordering=['-created_at']
class WorkshopRegistration(TimeStampedModel):
    class Status(models.TextChoices): PENDING='pending','Pending'; APPROVED='approved','Approved'; CANCELLED='cancelled','Cancelled'
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='workshop_registrations'); workshop=models.ForeignKey(Workshop,on_delete=models.CASCADE,related_name='registrations'); status=models.CharField(max_length=12,choices=Status.choices,default=Status.PENDING); attended=models.BooleanField(default=False)
    class Meta: constraints=[models.UniqueConstraint(fields=['user','workshop'],name='unique_workshop_registration')]; ordering=['-created_at']
class VolunteerActivityParticipant(TimeStampedModel):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='activity_participations'); activity=models.ForeignKey(VolunteerActivity,on_delete=models.CASCADE,related_name='participants'); status=models.CharField(max_length=20,default='registered'); attended=models.BooleanField(default=False)
    class Meta: constraints=[models.UniqueConstraint(fields=['user','activity'],name='unique_activity_participation')]
class GalleryAlbum(SluggedContent):
    description=models.TextField(blank=True); cover_image=models.ImageField(upload_to='gallery/',blank=True)
class GalleryImage(models.Model):
    album=models.ForeignKey(GalleryAlbum,on_delete=models.CASCADE,related_name='images'); image=models.ImageField(upload_to='gallery/'); caption=models.CharField(max_length=255,blank=True); display_order=models.PositiveIntegerField(default=0); uploaded_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['display_order','id']
class GalleryVideo(models.Model):
    album=models.ForeignKey(GalleryAlbum,on_delete=models.CASCADE,related_name='videos'); title=models.CharField(max_length=255); video_url=models.URLField(); thumbnail=models.ImageField(upload_to='gallery/',blank=True); description=models.TextField(blank=True)
class MembershipType(models.Model):
    name=models.CharField(max_length=100,unique=True); description=models.TextField(blank=True); benefits=models.TextField(blank=True); eligibility=models.TextField(blank=True); active=models.BooleanField(default=True); display_order=models.PositiveIntegerField(default=0)
    class Meta: ordering=['display_order','name']
    def __str__(self): return self.name
class Membership(TimeStampedModel):
    class Status(models.TextChoices): PENDING='pending','Pending'; APPROVED='approved','Approved'; REJECTED='rejected','Rejected'; EXPIRED='expired','Expired'
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='memberships'); membership_type=models.ForeignKey(MembershipType,on_delete=models.PROTECT); membership_id=models.CharField(max_length=30,unique=True,blank=True); approval_date=models.DateField(blank=True,null=True); expiry_date=models.DateField(blank=True,null=True); status=models.CharField(max_length=12,choices=Status.choices,default=Status.PENDING)
    def save(self,*args,**kwargs):
        if not self.membership_id: self.membership_id=f'TGCB-{uuid.uuid4().hex[:8].upper()}'
        super().save(*args,**kwargs)
class Certificate(TimeStampedModel):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='certificates'); certificate_type=models.CharField(max_length=100); certificate_number=models.CharField(max_length=40,unique=True,blank=True); title=models.CharField(max_length=255); issue_date=models.DateField(); event=models.ForeignKey(Event,null=True,blank=True,on_delete=models.SET_NULL); workshop=models.ForeignKey(Workshop,null=True,blank=True,on_delete=models.SET_NULL); activity=models.ForeignKey(VolunteerActivity,null=True,blank=True,on_delete=models.SET_NULL); verification_code=models.UUIDField(default=uuid.uuid4,unique=True,editable=False); status=models.CharField(max_length=20,default='active')
    def save(self,*args,**kwargs):
        if not self.certificate_number: self.certificate_number=f'TGCB-CERT-{uuid.uuid4().hex[:8].upper()}'
        super().save(*args,**kwargs)
class PartnerOrganization(models.Model):
    name=models.CharField(max_length=150); logo=models.ImageField(upload_to='partners/',blank=True); website=models.URLField(blank=True); description=models.TextField(blank=True); display_order=models.PositiveIntegerField(default=0); active=models.BooleanField(default=True)
    class Meta: ordering=['display_order','name']
class Testimonial(models.Model):
    name=models.CharField(max_length=150); designation=models.CharField(max_length=150,blank=True); photo=models.ImageField(upload_to='testimonials/',blank=True); content=models.TextField(); active=models.BooleanField(default=True); display_order=models.PositiveIntegerField(default=0)
    class Meta: ordering=['display_order','name']
class FAQ(models.Model):
    question=models.CharField(max_length=255); answer=models.TextField(); category=models.CharField(max_length=100,blank=True); display_order=models.PositiveIntegerField(default=0); active=models.BooleanField(default=True)
    class Meta: ordering=['display_order','id']
class ContactMessage(TimeStampedModel):
    name=models.CharField(max_length=150); email=models.EmailField(); subject=models.CharField(max_length=255); message=models.TextField(); resolved=models.BooleanField(default=False)
    def __str__(self): return self.subject
class Notification(TimeStampedModel):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='notifications'); title=models.CharField(max_length=255); message=models.TextField(); notification_type=models.CharField(max_length=50,default='general'); is_read=models.BooleanField(default=False)
    class Meta: ordering=['-created_at']
class AuditLog(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL); action=models.CharField(max_length=255); detail=models.TextField(blank=True); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
