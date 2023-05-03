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