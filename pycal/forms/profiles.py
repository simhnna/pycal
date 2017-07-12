from django import forms
from django.forms.formsets import formset_factory
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from pycal.models.profiles import Profile 


class ProfileForm(forms.Form):
    first_name = forms.CharField(label=_('First Name'), max_length=32)
    last_name = forms.CharField(label=_('Last Name'), max_length=32)
    username = forms.CharField(label=_('Username'), max_length=32)

    def clean_username(self):
        if len(self.cleaned_data['username'].split()) > 1:
            raise forms.ValidationError(_('Username must not contain spaces'), 'invalid')
        if 'username' in self.changed_data and User.objects.filter(username=self.cleaned_data['username']):
            raise forms.ValidationError(_('Username is in use'), 'invalid')
        return self.cleaned_data['username']

class RegistrationForm(ProfileForm):
    password = forms.CharField(label=_('Password'), min_length=8, widget=forms.PasswordInput())
    repeat_password = forms.CharField(label=_('Repeat Password'), min_length=8, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        repeated_password = cleaned_data.get('repeat_password')
        if password and repeated_password and password != repeated_password:
            raise forms.ValidationError(_('Passwords did not match'), 'invalid')


class UserAccountForm(ProfileForm):
    email_notifications = forms.BooleanField(label=_('Subscribe to Email notifications'))


ProfileFormset = formset_factory(ProfileForm)
