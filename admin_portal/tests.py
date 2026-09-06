from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from main.models import AuditLog, Event, EventRegistration, Notification


class AdminPortalWorkflowTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('portal-admin', 'admin@example.com', 'pass')
        self.user = User.objects.create_user('volunteer', 'user@example.com', 'pass')

    def test_general_user_cannot_access_admin_portal(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('admin_dashboard'))
        self.assertRedirects(response, f"{reverse('admin_login')}?next={reverse('admin_dashboard')}")

    def test_admin_can_create_edit_and_delete_event(self):
        self.client.force_login(self.admin)
        payload = {'title': 'Community Cleanup', 'description': 'Clean the park', 'date': '2030-01-10',
                   'venue': 'Central Park', 'registration_enabled': 'on', 'status': 'upcoming', 'active': 'on'}
        response = self.client.post(reverse('admin_crud_create', args=['event']), payload)
        self.assertRedirects(response, reverse('admin_events'))
        event = Event.objects.get(title='Community Cleanup')
        self.assertEqual(event.slug, 'community-cleanup')
        self.assertTrue(AuditLog.objects.filter(action='Created event').exists())
        payload.update(title='Community Cleanup Updated')
        self.client.post(reverse('admin_crud_edit', args=['event', event.pk]), payload)
        event.refresh_from_db(); self.assertEqual(event.title, 'Community Cleanup Updated')
        self.client.post(reverse('admin_crud_delete', args=['event', event.pk]))
        self.assertFalse(Event.objects.filter(pk=event.pk).exists())

    def test_admin_can_manage_registration_and_notification(self):
        event = Event.objects.create(title='Tree Day', description='Plant trees', date=date(2030, 1, 1), venue='Field')
        registration = EventRegistration.objects.create(user=self.user, event=event)
        self.client.force_login(self.admin)
        response = self.client.post(reverse('admin_crud_edit', args=['event-registration', registration.pk]), {'status': 'approved', 'attended': 'on'})
        self.assertRedirects(response, reverse('admin_event_registrations'))
        registration.refresh_from_db(); self.assertTrue(registration.attended); self.assertEqual(registration.status, 'approved')
        self.client.post(reverse('admin_crud_create', args=['notification']), {'user': self.user.pk, 'title': 'Welcome', 'message': 'Hello', 'notification_type': 'general'})
        self.assertTrue(Notification.objects.filter(user=self.user, title='Welcome').exists())
