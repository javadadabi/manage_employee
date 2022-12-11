from django import forms
from django.forms import ModelChoiceField
from .models import Work


class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    gender = forms.ChoiceField(choices=((None, ''), ('F', 'Female'), ('M', 'Male'), ('O', 'Other')))
    receive_news = forms.BooleanField(required=False, label='I want to receive news and special offers')
    agree_toc = forms.BooleanField(required=True, label='I agree with the Terms and Conditions')


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
    start_time = forms.DateTimeField(widget=forms.SelectDateWidget())
    expected_duration = forms.DurationField(required=False)
    end_time = forms.DateTimeField(widget=forms.SelectDateWidget(), required=False)
    done = forms.BooleanField(required=False)

