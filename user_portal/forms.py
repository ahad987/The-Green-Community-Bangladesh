from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control'}), 'last_name': forms.TextInput(attrs={'class': 'form-control'}), 'email': forms.EmailInput(attrs={'class': 'form-control'})}

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.exclude(pk=self.instance.pk).filter(email__iexact=email).exists():
            raise forms.ValidationError('Another account already uses this email address.')
        return email


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('photo', 'phone', 'address', 'education', 'skills_interests')
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'education': forms.TextInput(attrs={'class': 'form-control'}),
            'skills_interests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
