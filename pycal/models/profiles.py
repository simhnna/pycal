from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.template import Context
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail, mail_admins
from allauth.account.models import EmailAddress

import string
import random

class Profile(models.Model):
    user = models.OneToOneField(User)
    email_notifications = models.BooleanField(default=True)
    feed_id = models.CharField(max_length=64, unique=True, null=True, blank=True)

    def __str__(self):
        return "{}'s profile".format(self.user)


def generate_random_id():
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                   for x in range(64))

def email_is_used(email):
    return EmailAddress.objects.filter(email=email).exists()

def create_profile(username, email, password, first_name, last_name):
    if User.objects.filter(username=username).exists() or email_is_used(email):
        return False
    user = User.objects.create_user(username, '', password, first_name=first_name, last_name=last_name)
    user.is_active = False
    user.save()

    feed = generate_random_id()
    while Profile.objects.filter(feed_id=feed).exists():
        feed = generate_random_id()
    user.profile.feed_id = feed
    user.profile.save()

    mail_admins('Pycal new user signup', '{} {} ({}) signed up'.format(first_name, last_name, username))
    return user

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
