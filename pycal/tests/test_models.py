from django.test import TestCase
import pycal.models.profiles as profiles
from django.db.utils import IntegrityError
from django.core import mail

class ProfileTest(TestCase):
    def setUp(self):
        profiles.create_profile('user1', 'email1@email.email', 'password', 'first', 'last') 

    def test_duplicate_email(self):
        self.assertFalse(profiles.create_profile('user2', 'email1@email.email', 'password', 'first', 'last'))
        profile = profiles.Profile.objects.get(user__username='user1')
        profiles.activate_profile(profile)
        self.assertFalse(profiles.create_profile('user2', 'email1@email.email', 'password', 'first', 'last'))
        self.assertTrue(profiles.create_profile('user2', 'email2@email.email', 'password', 'first', 'last'))

    def test_duplicate_username(self):
        self.assertFalse(profiles.create_profile('user1', 'email3@email.email', 'password', 'first', 'last'))
        self.assertTrue(profiles.create_profile('user2', 'email3@email.email', 'password', 'first', 'last'))

    def test_profile_not_active(self):
        self.assertFalse(profiles.Profile.objects.get(user__username='user1').user.is_active)

    def test_activate(self):
        profile = profiles.Profile.objects.get(user__username='user1')
        email = profile.unverified_email
        profiles.activate_profile(profile)
        profile = profiles.Profile.objects.get(user__username='user1')
        self.assertTrue(profile.user.is_active)
        self.assertEquals(profile.unverified_email, '')
        self.assertEquals(profile.activation_id, '')
        self.assertEquals(profile.user.email, email)

    def test_change_unverified_email(self):
        profile = profiles.Profile.objects.get(user__username='user1')
        self.assertFalse(profile.change_email('email1@email.email'))
        self.assertTrue(profile.change_email('email3@email.email'))

    def test_change_verified_email(self):
        profile = profiles.Profile.objects.get(user__username='user1')
        profiles.activate_profile(profile)
        profile = profiles.Profile.objects.get(user__username='user1')
        self.assertFalse(profile.change_email('email1@email.email'))
        self.assertTrue(profile.change_email('email3@email.email'))

    def test_email_used_function(self):
        self.assertFalse(profiles.email_is_used('email2@email.email'))
        self.assertTrue(profiles.email_is_used('email1@email.email'))

    def test_email_notifications_true(self):
        self.assertTrue(profiles.Profile.objects.all().first().email_notifications)

    def test_admin_email(self):
        self.assertEquals(len(mail.outbox), 1)
        self.assertIn('user1', mail.outbox[0].body) 
        self.assertIn('Pycal new user signup', mail.outbox[0].subject) 
