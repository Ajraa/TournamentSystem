from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def index(request):
    players = Player.objects.all()
    
    return render(request, 'index.html', {'players':players})
