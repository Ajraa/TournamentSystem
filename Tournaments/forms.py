from django import forms
from django.forms import widgets
from .models import *

class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ['players']

class CreateTournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        exclude = ['founder', 'teams']
        widgets = {
            'start_time': widgets.DateInput(attrs={'type': 'date'})
        }

class CreateMatchForm(forms.ModelForm):
    class Meta:
        model = Match
        exclude = ['tournament', 'state']
