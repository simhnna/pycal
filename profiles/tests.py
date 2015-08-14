from django.test import TestCase
import profiles.models as profiles
from django.db.utils import IntegrityError

class ProfileTest(TestCase):
    def setUp(self):
        profiles.create_profile('user1', 'email1@email.email', 'password', 'first', 'last') 

    def test_duplicate_email(self):
       pass

    def test_duplicate_username(self):
        with self.assertRaisesMessage(IntegrityError, 'UNIQUE constraint failed: auth_user.username'):
            profiles.create_profile('user1', 'email3@email.email', 'password', 'first', 'last')

    def test_profile_not_active(self):
        self.assertFalse(profiles.Profile.objects.get(user__username='user1').user.is_active)

    def test_activate(self):
        profile = profiles.Profile.objects.get(user__username='user1')
        email = profile.unverified_email
        self.assertTrue(profiles.activate(profile.activation_id))
        profile = profiles.Profile.objects.get(user__username='user1')
        self.assertTrue(profile.user.is_active)
        self.assertEquals(profile.unverified_email, '')
        self.assertEquals(profile.activation_id, '')
        self.assertEquals(profile.user.email, email)

    def test_invalid_activation_id(self):
        self.assertFalse(profiles.activate('invalid'))

    def test_change_unverified_email(self):
        profile = profiles.Profile.objects.get(user__username='user1')
        self.assertFalse(profile.change_email('email1@email.email'))
        self.assertTrue(profile.change_email('email3@email.email'))

    def test_change_verified_email(self):
        profile = profiles.Profile.objects.get(user__username='user1')
        self.assertTrue(profiles.activate(profile.activation_id))
        profile = profiles.Profile.objects.get(user__username='user1')
        self.assertFalse(profile.change_email('email1@email.email'))
        self.assertTrue(profile.change_email('email3@email.email'))

    def test_email_used_function(self):
        self.assertFalse(profiles.email_is_used('email2@email.email'))
        self.assertTrue(profiles.email_is_used('email1@email.email'))

    def test_email_notifications_true(self):
        self.assertTrue(profiles.Profile.objects.all().first().email_notifications)
 
