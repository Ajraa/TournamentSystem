from django import forms
from django.forms import widgets
from .models import *

class PlayerLoginForm(forms.ModelForm):
    class Meta():
        model = Player
        exclude = ['fname', 'lname']
        
class PlayerRegisterForm(forms.ModelForm):
    class Meta():
        model = Player
        exclude = []
        
class CreateTeamForm(forms.ModelForm):
    class Meta():
        model = Team
        exclude = ['players']
        
class FounderLoginForm(forms.ModelForm):
    class Meta():
        model = Founder
        exclude = ['fname', 'lname']
        
class FounderRegisterForm(forms.ModelForm):
    class Meta:
        model = Founder
        exclude = []
        
class CreateTournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        exclude = ['founder', 'teams']
        widgets = {
            'start_time': widgets.DateInput(attrs={'type': 'date'})
        }