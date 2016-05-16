from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from pycal.models.events import Event, Category, RemoteCalendar
from pycal.models.profiles import Profile


admin.site.register(Category)


class DateListFilter(admin.SimpleListFilter):
    title = _('Event')
    parameter_name = 'event'

    def lookups(self, request, model_admin):
        return (
                ('past', _('in the past')),
                ('present', _('ongoing')),
                ('future', _('in the future')),
                )

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == 'past':
            return queryset.filter(dtend__lte=now)
        if self.value() == 'future':
            return queryset.filter(dtstart__gte=now)
        if self.value() == 'present':
            return queryset.filter(dtstart__lte=now, dtend__gte=now)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
  list_display = ('title', 'location', 'dtstart')
  ordering = ('-dtstart',)
  list_filter = ('dtstart', DateListFilter, 'group', 'category')


@admin.register(RemoteCalendar)
class RemoteCalendarAdmin(admin.ModelAdmin):
    actions = ['poll_remote_calendars']

    def poll_remote_calendars(self, request, queryset):
        updated_count = 0
        created_count = 0
        for cal in queryset:
            created, updated = cal.poll_calendar()
            created_count += created
            updated_count += updated
        self.message_user(request, 'Created {} events and updated {} events'.format(created_count, updated_count))

    poll_remote_calendars.short_description = 'Poll the selected Remote Calendars'


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class OwnUserAdmin(UserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, OwnUserAdmin)
