from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.template import Context
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.core.mail import send_mail

import string
import random

class Profile(models.Model):
    user = models.OneToOneField(User)
    email_notifications = models.BooleanField(default=False)
    unverified_email = models.EmailField(blank=True, null=True)
    activation_id = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return "{}'s profile".format(self.user)

    def populate(self, username, email, password, first_name, last_name):
        self.unverified_email = email
        self.generate_activation_id()
        user = User.objects.create_user(username, '', password)
        user.first_name = first_name
        user.last_name = last_name
        self.user = user
        user.save()


    def generate_activation_id(self):
        self.activation_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase +
            string.digits) for x in range(64))

    def change_email(self, new_email):
        if self.unverified_email == new_email or self.user.email == new_email:
            return False
        self.unverified_email = new_email
        self.generate_activation_id()
        self.save()
        return True

    def send_verification_email(self, request):
        c = Context({'profile': self,
            'link': request.build_absolute_uri(reverse('profiles:activate',
            args=(self.activation_id,)))})
        message = render_to_string('profiles/activatation_email.txt', c)
        send_mail('Verification Mail', message, 'donotreply@serve-me.info',
                [self.unverified_email])
        return True

def activate(activation_id):
    for p in Profile.objects.filter(activation_id = activation_id):
        p.user.email = p.unverified_email
        p.unverified_email = ''
        p.activation_id = ''
        p.user.is_active = True
        p.user.save()
        p.save()
        return True

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Profile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)

