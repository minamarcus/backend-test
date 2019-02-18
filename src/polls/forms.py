from django import forms
from polls.choices import *


class VotingForm(forms.Form):
    vote = forms.ChoiceField(choices=COMPLEXITY, label="", initial='', widget=forms.Select(), required=True)


class PollForm(forms.Form):
    title = forms.CharField(
            widget=forms.TextInput(
                attrs={"class": "form-control"}
                )
            )
    description = forms.CharField(
            widget=forms.Textarea(
                attrs={"class": "form-control"}
                )
            )
