from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.template import Context
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail, mail_admins

import string
import random

class Profile(models.Model):
    user = models.OneToOneField(User)
    email_notifications = models.BooleanField(default=True)
    unverified_email = models.EmailField(blank=True, null=True)
    activation_id = models.CharField(max_length=64, blank=True)
    feed_id = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return "{}'s profile".format(self.user)

    def generate_activation_id(self):
        activation_id = generate_random_id()
        while Profile.objects.filter(activation_id=activation_id).exists():
            activation_id = generate_random_id()
        self.activation_id = activation_id
        self.save()

    def change_email(self, new_email):
        if self.unverified_email == new_email or self.user.email == new_email:
            return False
        self.unverified_email = new_email
        self.save()
        return True

    def send_verification_email(self, request):
        self.generate_activation_id()
        c = Context({'profile': self,
                     'activation_link': request.build_absolute_uri(reverse('profiles:activate', args=(self.activation_id,))),
                     'feed_link': request.build_absolute_uri(reverse('events:private_feed', args=(self.feed_id,)))})
        message = render_to_string('profiles/activation_email.txt', c)
        send_mail('Verification Mail', message, 'pycal@serve-me.info',
                  [self.unverified_email])
        return True

    def send_welcome_email(self, request):
        c = Context({'profile': self,
                     'feed_link': request.build_absolute_uri(reverse('events:private_feed',
                                                                args=(self.feed_id,)))})
        message = render_to_string('profiles/welcome_email.txt', c)
        send_mail('Verification Mail', message, 'pycal@serve-me.info',
                  [self.user.email])
        return True


def generate_random_id():
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                   for x in range(64))

def activate_token(activation_id):
    if Profile.objects.filter(activation_id=activation_id).exists():
        activate_profile(Profile.objects.get(activation_id=activation_id))
        return True
    return False

def activate_profile(profile):
    if profile:
        profile.user.email = profile.unverified_email
        profile.unverified_email = ''
        profile.activation_id = ''
        profile.user.is_active = True
        profile.user.save()
        profile.save()


def create_profile(username, email, password, first_name, last_name):
    if User.objects.filter(username=username).exists() or email_is_used(email):
        return False
    user = User.objects.create_user(username, '', password, first_name=first_name, last_name=last_name)
    user.is_active = False
    user.save()
    user.profile.unverified_email = email

    feed = generate_random_id()
    while Profile.objects.filter(feed_id=feed).exists():
        feed = generate_random_id()
    user.profile.feed_id = feed
    user.profile.save()

    mail_admins('Pycal new user signup', '{} {} ({}) signed up'.format(first_name, last_name, username))
    return user

def email_is_used(email):
    return (User.objects.filter(email=email).exists() or
            Profile.objects.filter(unverified_email=email).exists())

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
