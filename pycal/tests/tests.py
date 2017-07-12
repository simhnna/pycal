from django.test import TestCase, Client
from pycal.forms.profiles import RegistrationForm 
from pycal.models.profiles import create_profile

class TestRegistrationForm(TestCase):

    def setUp(self):
        create_profile('user1', 'email1@email.email', 'password', 'first', 'last')
        user = create_profile('user2', 'email2@email.email', 'password', 'first', 'last')
        user.is_active = True
        user.save()

    def test_valid_form(self):
        data = {
                'first_name': 'first',
                'last_name': 'last',
                'username': 'meh',
                'email': 'email@email.email',
                'password': 'password',
                'repeat_password': 'password'
                }
        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_used_email(self):
        data = {
                'first_name': 'first',
                'last_name': 'last',
                'username': 'meh',
                'email': 'email1@email.email',
                'password': 'password',
                'repeat_password': 'password'
                }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        data['email'] = 'email2@email.email'
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_used_user(self):
        data = {
                'first_name': 'first',
                'last_name': 'last',
                'username': 'user1',
                'email': 'email@email.email',
                'password': 'password',
                'repeat_password': 'password'
                }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        data = {
                'first_name': 'first',
                'last_name': 'last',
                'username': 'meh',
                'email': 'email',
                'password': 'password',
                'repeat_password': 'password'
                }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_password_mismatch(self):
        data = {
                'first_name': 'first',
                'last_name': 'last',
                'username': 'meh',
                'email': 'email@email.email',
                'password': 'password',
                'repeat_password': 'password1'
                }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_too_short_passwords(self):
        data = {
                'first_name': 'first',
                'last_name': 'last',
                'username': 'meh',
                'email': 'email@email.email',
                'password': 'pass',
                'repeat_password': 'pass'
                }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())

