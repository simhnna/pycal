from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from events.models import Event, Attendant


class EventForm(forms.ModelForm):
    private = forms.BooleanField(label=_('Private'), required=False)

    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'start_date', 'end_date', 'all_day',
                'details', 'group']

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        if cleaned_data.get('private'):
            cleaned_data['details'] = None
            if not cleaned_data.get('group'):
                self.add_error('group', forms.ValidationError(_('You have to specify a group'),
                                                              'invalid'))
        else:
            cleaned_data['group'] = None
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        if start and end and end <= start:
            raise forms.ValidationError(_('End date has to be after the start Date'), 'invalid')
        if not cleaned_data.get('all_day') and not end:
            raise forms.ValidationError(_('If the event is not an All Day Event, it has to have an end Date'), 'invalid')
        return cleaned_data

    def clean_start_date(self):
        start = self.cleaned_data['start_date']
        if start and start < timezone.now():
            raise forms.ValidationError(_('Start date has to be in the future'), 'invalid')
        return self.cleaned_data['start_date']

    def clean_end_date(self):
        end = self.cleaned_data['end_date']
        if end and end < timezone.now():
            raise forms.ValidationError(_('End date has to be in the future'), 'invalid')
        return self.cleaned_data['end_date']

class ICalUploadForm(forms.Form):
    ical_file = forms.FileField(label=_('Select ICal file to import'))

class DeleteForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = []
