from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group

from tempfile import TemporaryFile

from events.models import Event, Attendant, process_ical_events
from events.forms import EventForm, DeleteForm, ICalUploadForm


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, instance=Event(created_by=request.user))
        if form.is_valid():
            e = form.save()
            messages.success(request, _('Event created'))
            e.send_email_notifications(request.build_absolute_uri(reverse('events:attend',args=(e.id,))))
            return HttpResponseRedirect(reverse('events:detail', args=(e.id,)))
    else:
        form = EventForm()

    return render(request, 'events/edit_event.html',
                  {'form': form,
                   'create_event': True,
                   })

@login_required
@permission_required('events.delete_Event', raise_exception=True)
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.user.id == event.created_by_id or request.user.is_superuser:
        if request.method == 'POST':
            form = DeleteForm(request.POST)
            if form.is_valid():
                event.delete()
                messages.success(request, _('Event deleted'))
                return HttpResponseRedirect(reverse('index'))
        else:
            form = DeleteForm()

        return render(request, 'events/detail.html',
                      {'form': form,
                       'event': event,
                       'delete_event': True
                       })
    messages.warning(request, _('You are not allowed to do this!'))
    return HttpResponseRedirect(reverse('events:detail', args=(event.id,)))

@login_required
def attend(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.user in event.attendant_set.all():
        messages.error(request, _('You are allready attending'))
    else:
        a = Attendant()
        a.user = request.user
        a.event = event
        a.save()
        messages.success(request, _('You have been marked as attending'))
    return HttpResponseRedirect(reverse('events:detail', args=(event_id,)))

@login_required
def unattend(request, event_id):
    attendant = get_object_or_404(Attendant, user=request.user, event__id=event_id)
    attendant.delete()
    messages.success(request, _('You have been marked as not attending'))
    return HttpResponseRedirect(reverse('events:detail', args=(event_id,)))

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.user.id != event.created_by_id and not request.user.is_superuser:
        messages.warning(request, _('You are not allowed to do this'))
        return HttpResponseRedirect(reverse('events:detail', args=(event.id,)))
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, _('Event edited'))
            return HttpResponseRedirect(reverse('events:detail', args=(event.id,)))

    else:
        form = EventForm(instance=event)
    return render(request, 'events/edit_event.html',
                  {'form': form,
                   'event_id': event.id,
                   'edit': True,
                   })

@login_required
@staff_member_required
def upload_ical(request):
    if request.method == 'POST':
        form = ICalUploadForm(request.POST, request.FILES)
        if form.is_valid():
            with TemporaryFile() as ical_file:
                for chunk in request.FILES['ical_file'].chunks():
                    ical_file.write(chunk)
                ical_file.seek(0)
                data = ical_file.read()
                created_count, updated_count = process_ical_events(data, request.user)
            messages.success(request, 'Created {} events and updated {} events'.format(created_count, updated_count))

    else:
        form = ICalUploadForm()
    return render(request, 'events/upload_ical.html',
            {'form': form})


def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.group and not request.user.groups.filter(name=event.group).exists():
        messages.warning(request, _('You are not allowed to do this!'))
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'events/detail.html',
                  {'event': event,
                   'is_attending': event.is_attending(request.user),
                   'attendants': event.attendants(),
                   'is_event': True,
                   })
