from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.forms import ModelChoiceField, NumberInput, DateTimeInput
from .models import Work


class WorkChoiceField(ModelChoiceField):
    """Return work_title as option string """

    def label_from_instance(self, obj):
        return obj.work_title


class TaskForm(forms.Form):
    task_name = forms.CharField()
    belong_to_work = WorkChoiceField(queryset=Work.objects.all())
    description = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 5, 'placeholder': 'A brief description about this task'}
    ),
        max_length=4000, required=False,
        help_text='The max length of the text is 4000.')
    start_time = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget())
    expected_duration = forms.DurationField(required=False, error_messages={'invalid': 'Please insert a valid format'
                                                                                       'like: days '
                                                                                       'hours:minutes:seconds'})
    end_time = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget(), required=False)
    done = forms.BooleanField(required=False)

