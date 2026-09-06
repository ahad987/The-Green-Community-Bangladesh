from django import forms

from main.models import (
    AwarenessArticle, BoardMember, Certificate, Event, EventRegistration,
    ExecutiveCommitteeMember, GalleryAlbum, Membership, News, Notification,
    VolunteerActivity, VolunteerActivityParticipant, Workshop,
    WorkshopRegistration,
)


class StyledModelForm(forms.ModelForm):
    """Shared Bootstrap styling for the custom administration portal."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = 'form-check-input' if isinstance(field.widget, forms.CheckboxInput) else 'form-control'
            field.widget.attrs.setdefault('class', css)


class EventForm(StyledModelForm):
    class Meta:
        model = Event
        exclude = ('slug',)
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}), 'start_time': forms.TimeInput(attrs={'type': 'time'}),
                   'end_time': forms.TimeInput(attrs={'type': 'time'}), 'registration_deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'})}


class WorkshopForm(StyledModelForm):
    class Meta:
        model = Workshop
        exclude = ('slug',)
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}), 'time': forms.TimeInput(attrs={'type': 'time'})}


class AwarenessForm(StyledModelForm):
    class Meta:
        model = AwarenessArticle
        exclude = ('slug',)
        widgets = {'published_date': forms.DateInput(attrs={'type': 'date'})}


class ActivityForm(StyledModelForm):
    class Meta:
        model = VolunteerActivity
        exclude = ('slug',)
        widgets = {'activity_date': forms.DateInput(attrs={'type': 'date'})}


class NewsForm(StyledModelForm):
    class Meta:
        model = News
        exclude = ('slug',)
        widgets = {'published_date': forms.DateInput(attrs={'type': 'date'})}


class GalleryAlbumForm(StyledModelForm):
    class Meta:
        model = GalleryAlbum
        exclude = ('slug',)


class BoardMemberForm(StyledModelForm):
    class Meta:
        model = BoardMember
        fields = '__all__'


class CommitteeMemberForm(StyledModelForm):
    class Meta:
        model = ExecutiveCommitteeMember
        fields = '__all__'


class MembershipForm(StyledModelForm):
    class Meta:
        model = Membership
        fields = ('user', 'membership_type', 'membership_id', 'approval_date', 'expiry_date', 'status')
        widgets = {'approval_date': forms.DateInput(attrs={'type': 'date'}), 'expiry_date': forms.DateInput(attrs={'type': 'date'})}


class CertificateForm(StyledModelForm):
    class Meta:
        model = Certificate
        exclude = ('verification_code',)
        widgets = {'issue_date': forms.DateInput(attrs={'type': 'date'})}


class NotificationForm(StyledModelForm):
    class Meta:
        model = Notification
        fields = ('user', 'title', 'message', 'notification_type', 'is_read')


class EventRegistrationForm(StyledModelForm):
    class Meta:
        model = EventRegistration
        fields = ('status', 'attended')


class WorkshopRegistrationForm(StyledModelForm):
    class Meta:
        model = WorkshopRegistration
        fields = ('status', 'attended')


class ActivityParticipantForm(StyledModelForm):
    class Meta:
        model = VolunteerActivityParticipant
        fields = ('status', 'attended')
