from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import messages
from events.models import Event
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.decorators import permission_required

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'start_date', 'end_date']
        widgets={
                'title':forms.TextInput(attrs={'placeholder':'title','class':'form-control',
                    'required':''}),
                'description':forms.Textarea(attrs={'placeholder':'description','class':'form-control','required':''}),
                'location':forms.TextInput(attrs={'placeholder':'location','class':'form-control','required':''}),
                'start_date':forms.TextInput(attrs={'placeholder':'start_date','class':'form-control','required':'','readonly':''}),
                'end_date':forms.TextInput(attrs={'placeholder':'end_date','class':'form-control','required':'','readonly':''}),
                }


    def clean_start_date(self):
        if self.cleaned_data['start_date'] < timezone.now():
            raise forms.ValidationError(_('Start date has to be in the future'), 'invalid')
        return self.cleaned_data['start_date']

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        if self.cleaned_data['end_date'] < timezone.now():
            raise forms.ValidationError(_('End date has to be in the future'), 'invalid')
        elif start_date and self.cleaned_data.get('end_date') <= start_date:
            raise forms.ValidationError(_('End date has to be after the start Date'), 'invalid')
        return self.cleaned_data['end_date']


class DeleteForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = []

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, instance=Event(created_by=request.user))
        if form.is_valid():
            e = form.save()
            messages.success(request, _('Event created'))
            e.send_email_notifications()
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

        return render(request, 'events/delete_event.html',
                {'form': form,
                    'event': event,
                    })
    messages.warning(request, _('You are not allowed to do this!'))
    return HttpResponseRedirect(reverse('events:detail', args=(event.id,)))
        
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
        if event.created_by.id != request.user.id:
             messages.warning(request, _('You are not allowed to do this!'))
             return HttpResponseRedirect(reverse('events:detail', args=(event.id,)))
        form = EventForm(instance=event)
    return render(request, 'events/edit_event.html',
            {'form': form,
                'event_id': event.id,
                'edit': True,
                })


def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'events/detail.html',
            {'event': event,
                })
