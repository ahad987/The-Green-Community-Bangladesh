from django.contrib import admin
from . import models

@admin.register(models.SiteSettings, models.HomePageContent, models.OrganizationProfile)
class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): return not self.model.objects.exists()

@admin.register(models.Event, models.Workshop, models.AwarenessArticle, models.VolunteerActivity, models.News)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'featured', 'created_at')
    list_filter = ('active', 'featured')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(models.EventRegistration, models.WorkshopRegistration, models.VolunteerActivityParticipant)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'attended', 'created_at')
    list_filter = ('status', 'attended')
    search_fields = ('user__username', 'user__email')

@admin.register(models.Membership, models.Certificate, models.Notification, models.ContactMessage, models.AuditLog)
class OperationsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at')
    search_fields = ('user__username', 'user__email')

for model in [models.HomePageStatistic, models.BoardMember, models.ExecutiveCommitteeMember, models.EventCategory, models.WorkshopCategory, models.AwarenessCategory, models.VolunteerActivityCategory, models.NewsCategory, models.GalleryAlbum, models.GalleryImage, models.GalleryVideo, models.MembershipType, models.PartnerOrganization, models.Testimonial, models.FAQ]:
    admin.site.register(model)
