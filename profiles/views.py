from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from profiles.models import create_profile, generate_random_id
from profiles.models import activate_token, activate_profile
from profiles.forms import ProfileForm, RegistrationForm, UserAccountForm, EmailChangeForm, ProfileFormset


def activate(request, activation_id):
    if activate_token(activation_id):
        messages.success(request, _('You can sign in now'))
        return HttpResponseRedirect(reverse('index'))
    else:
        messages.warning(request, _('The code is not right...'))
        return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
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
        form = RegistrationForm()
        return render(request, 'profiles/register.html',
                      {'form': form,
                       })

@user_passes_test(lambda u: u.is_superuser)
def admin(request):
    return render(request, 'profiles/admin_index.html')

@user_passes_test(lambda u: u.is_superuser)
def add_profile(request):
    if request.method == 'POST':
        profile_formset = ProfileFormset(request.POST)
        if profile_formset.is_valid():
            user_added = False
            for form in profile_formset:
                if form.cleaned_data:
                    username = form.cleaned_data['username']
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    email = form.cleaned_data['email']
                    password = generate_random_id()
                    new_user = create_profile(username, email, password, first_name, last_name)
                    activate_profile(new_user.profile)
                    new_user.profile.send_welcome_email(request)
                    user_added = True
            if user_added:
                messages.success(request, _('The profiles have been created'))
            profile_formset = ProfileFormset()

        else:
            messages.warning(request, _('Please check the fields below for error'))
    else:
        profile_formset = ProfileFormset()
    return render(request, 'profiles/add_profile.html', {'profile_formset': profile_formset,})

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
