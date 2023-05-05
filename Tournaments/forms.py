from django import forms
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