from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from profiles.models import Profile


class AccountForm(forms.Form):
    first_name = forms.CharField(max_length=32, 
            widget=forms.TextInput(attrs={'placeholder': _('first_name'), 'class': 'form-control'}))
    last_name = forms.CharField(max_length=32, 
            widget=forms.TextInput(attrs={'placeholder': _('last_name'), 'class': 'form-control'}))
    username = forms.CharField(max_length=32, 
            widget=forms.TextInput(attrs={'placeholder': _('user_name'), 'class': 'form-control'}))
    email = forms.EmailField(
            widget=forms.TextInput(attrs={'placeholder': _('email'), 'class': 'form-control'}))
    password = forms.CharField(
            widget=forms.PasswordInput(attrs={'placeholder': _('password'), 'class': 'form-control'}))
    password2 = forms.CharField(
            widget=forms.PasswordInput(attrs={'placeholder': _('repeat_password'), 'class': 'form-control'}))

    def clean_password2(self):
        if self.cleaned_data['password2'] != self.cleaned_data['password']:
            raise forms.ValidationError(_('passwords didn\'t match'), 'ivalid')
        return self.cleaned_data['password2']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']) or Profile.objects.filter(unverified_email=self.cleaned_data['email']):
            raise forms.ValidationError(_('Email is in use'), 'invalid')
        return self.cleaned_data['email']
    
    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']):
            raise forms.ValidationError(_('Username is in use'), 'invalid')
        return self.cleaned_data['username']


class UserAccountForm(forms.ModelForm):
    first_name = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'placeholder':
        _('first_name'),
        'class': 'form-control'}))
    last_name = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'placeholder':
        _('last_name'),
        'class': 'form-control'}))
    class Meta:
        model = Profile
        fields = ['email_notifications',]

    def __init__(self, *args, **kwargs):
        super(UserAccountForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['first_name', 'last_name', 'email_notifications']


class EmailChangeForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':
        _('email'),
        'class': 'form-control'}))

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']) or Profile.objects.filter(unverified_email=self.cleaned_data['email']):
            raise forms.ValidationError(_('Email is in use'), 'invalid')
        return self.cleaned_data['email']


def activate(request, activation_id):
    if (Profile.activate(activation_id)):
        messages.success(request, _('You can sign in now'))
        return HttpResponseRedirect(reverse('index'))
    else:
        messages.warning(request, _('The code is not right...'))
        return HttpResponseRedirect(reverse('index'))

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['new_password1'] != form.cleaned_data['new_password2']:
                messages.warning(request, _('passwords did not match'))
            else:
                request.user.set_password(form.cleaned_data['new_password1'])
                request.user.save()
                messages.success(request, _('Password changed successfully'))
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.warning(request, _('Your old password was not correct'))
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'profiles/change_password.html',
            {'form': form,
                })

def register(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            new_user = Profile()
            new_user.populate(username, email, password, first_name, last_name)
            new_user.send_verification_email(request)
            messages.success(request, _('Yeah, you just signed up'))
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.warning(request, _('Check the errors...'))
            return render(request, 'profiles/register.html',
            {'form': form,
                })
    else:
        form = AccountForm()
        return render(request, 'profiles/register.html',
            {'form': form,
                })

@login_required
def sign_out(request):
    auth.logout(request)
    messages.success(request, _('You have been signed out'))
    return HttpResponseRedirect(reverse('index'))

@login_required
def change_email(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            account = request.user.profile
            account.change_email(form.cleaned_data['email'])
            messages.info(request, _('Email added. Please verify it, so it is used.'))
            return HttpResponseRedirect(reverse('index'))
        messages.warning(request, _('Email in use'))
    else:
        form = EmailChangeForm()

    return render(request, 'profiles/change_email.html',
            {'form':form,
                })

@login_required
def edit_account(request):
    if request.method == 'POST':
        form = UserAccountForm(request.POST)
        if form.is_valid():
            a = request.user.profile
            a.email_notifications = form.cleaned_data['email_notifications']
            a.user.first_name = form.cleaned_data['first_name']
            a.user.last_name = form.cleaned_data['last_name']
            a.user.save()
            a.save()
            messages.success(request, _('Successfully edited account'))
            return HttpResponseRedirect(reverse('profiles:edit_account'))
        else:
            messages.warning(request, _('Oops, something went wrong'))
    else:
        u = request.user
        form = UserAccountForm(instance=u.profile, initial={'first_name':u.first_name,'last_name':u.last_name})
        
    return render(request, 'profiles/edit_account.html',
            {'form':form,
                })



def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username = username, password = password)
            messages.success(request, _('Yeah, you are in!'))
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
        if form.get_user() is not None:
            messages.warning(request, _('Your account is not active...'))
        else:
            messages.warning(request, _('Sorry, this username/password match is not correct'))
    else:
        form = AuthenticationForm()
    return render(request, 'profiles/sign_in.html',
            {'form': form,
                })
