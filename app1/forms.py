from django import forms
from .models import Task


class DateTimeInput(forms.DateTimeInput):
    input_type = "date"


class AddNewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['goal', 'description', 'end_date']
        widgets = {'end_date': DateTimeInput()}


class ShareTask(forms.Form):
    share_with = forms.CharField(max_length=250, initial="Enter a username")