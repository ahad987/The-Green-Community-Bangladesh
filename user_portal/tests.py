from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from main.models import Notification, VolunteerActivity, VolunteerActivityParticipant


class UserPortalSecurityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user-one', password='pass')
        self.other = User.objects.create_user('user-two', password='pass')
        self.client.force_login(self.user)

    def test_dashboard_and_profile_are_database_backed(self):
        response = self.client.get(reverse('user_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['event_count'], 0)
        response = self.client.post(reverse('user_edit_profile'), {'first_name': 'Green', 'last_name': 'Volunteer', 'email': 'green@example.com', 'phone': '123'})
        self.assertRedirects(response, reverse('user_profile'))
        self.user.refresh_from_db(); self.assertEqual(self.user.first_name, 'Green')

    def test_user_cannot_mark_another_users_notification(self):
        notification = Notification.objects.create(user=self.other, title='Private', message='Secret')
        response = self.client.post(reverse('user_notification_read', args=[notification.pk]))
        self.assertEqual(response.status_code, 404)

    def test_user_can_join_activity_once(self):
        activity = VolunteerActivity.objects.create(title='Canal Cleanup', description='Cleanup', location='Canal', activity_date=date(2030, 2, 2))
        url = reverse('volunteer_register', args=[activity.slug])
        self.client.post(url); self.client.post(url)
        self.assertEqual(VolunteerActivityParticipant.objects.filter(user=self.user, activity=activity).count(), 1)
