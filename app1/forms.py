from django import forms
from .models import Task, Comment


class DateTimeInput(forms.DateTimeInput):
    input_type = "date"


class AddNewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['goal', 'description', 'end_date']
        widgets = {'end_date': DateTimeInput()}


class ShareTask(forms.Form):
    share_with = forms.CharField(max_length=250, widget=forms.TimeInput(attrs={'placeholder': 'Enter a username'}))
    editable = forms.BooleanField(required=False)


class LeaveComment(forms.ModelForm):
    comment_text = forms.CharField(label='', max_length=250,
                                   widget=forms.Textarea(attrs={'placeholder': 'Comment text',
                                                                'style': 'resize:none; height:100px;'
                                                                }))

    class Meta:
        model = Comment
        fields = ['comment_text']
