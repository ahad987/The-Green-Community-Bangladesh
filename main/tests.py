from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from main.models import Event, EventRegistration


class PublicWorkflowTests(TestCase):
    def test_active_admin_created_content_is_public_and_registerable(self):
        user = User.objects.create_user('member', password='pass')
        event = Event.objects.create(title='Green Rally', description='Awareness rally', date=date(2030, 3, 3), venue='Dhaka')
        self.assertContains(self.client.get(reverse('events_list')), 'Green Rally')
        self.client.force_login(user)
        response = self.client.post(reverse('event_register', args=[event.slug]))
        self.assertRedirects(response, reverse('user_events'))
        self.assertTrue(EventRegistration.objects.filter(user=user, event=event).exists())

    def test_inactive_content_is_not_public(self):
        event = Event.objects.create(title='Draft Event', description='Draft', date=date(2030, 3, 3), venue='Dhaka', active=False)
        self.assertNotContains(self.client.get(reverse('events_list')), event.title)
        self.assertEqual(self.client.get(reverse('event_detail', args=[event.slug])).status_code, 404)
