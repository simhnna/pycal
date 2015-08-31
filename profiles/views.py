from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from profiles.models import Profile, create_profile, email_is_used
from profiles.models import activate as activate_profile


class AccountForm(forms.Form):
    first_name = forms.CharField(label=_('First Name'), max_length=32)
    last_name = forms.CharField(label=_('Last Name'), max_length=32)
    username = forms.CharField(label=_('Username'), max_length=32)
    email = forms.EmailField()
    password = forms.CharField(label=_('Password'), min_length=8, widget=forms.PasswordInput())
    repeat_password = forms.CharField(label=_('Repeat Password'), min_length=8, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(AccountForm, self).clean()
        password = cleaned_data.get('password')
        repeated_password = cleaned_data.get('repeat_password')
        if password and repeated_password and password != repeated_password:
            raise forms.ValidationError(_('Passwords did not match'), 'invalid')

    def clean_email(self):
        if email_is_used(self.cleaned_data['email']):
            raise forms.ValidationError(_('Email is in use'), 'invalid')
        return self.cleaned_data['email']

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']):
            raise forms.ValidationError(_('Username is in use'), 'invalid')
        return self.cleaned_data['username']

class UserAccountForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email_notifications', ]


class EmailChangeForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        if email_is_used(self.cleaned_data['email']):
            raise forms.ValidationError(_('Email is in use'), 'invalid')
        return self.cleaned_data['email']


def activate(request, activation_id):
    if activate_profile(activation_id):
        messages.success(request, _('You can sign in now'))
        return HttpResponseRedirect(reverse('index'))
    else:
        messages.warning(request, _('The code is not right...'))
        return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            new_user = create_profile(username, email, password, first_name, last_name)
            if new_user:
                new_user.profile.send_verification_email(request)
                messages.success(request, _('Yeah, you just signed up'))
                return HttpResponseRedirect(reverse('index'))
        return render(request, 'profiles/register.html',
                      {'form': form,
                       })
    else:
        form = AccountForm()
        return render(request, 'profiles/register.html',
                      {'form': form,
                       })

@login_required
def change_email(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            account = request.user.profile
            account.change_email(form.cleaned_data['email'])
            account.send_verification_email(request)
            messages.info(request, _('Email added. Please verify it, so it is used.'))
            return HttpResponseRedirect(reverse('index'))
    else:
        form = EmailChangeForm()

    return render(request, 'profiles/change_email.html',
                  {'form': form,
                   })


@login_required
def edit_account(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserAccountForm(request.POST)
        if form.is_valid():
            profile.email_notifications = form.cleaned_data['email_notifications']
            profile.save()
            messages.success(request, _('Successfully edited account'))
            return HttpResponseRedirect(reverse('profiles:edit_account'))
        else:
            messages.warning(request, _('Oops, something went wrong'))
    else:
        user = request.user
        form = UserAccountForm(instance=profile,
                               initial={'first_name': user.first_name, 'last_name': user.last_name})

    return render(request, 'profiles/edit_account.html',
                  {'form': form,
                   'feed': profile.feed_id,
                   })
