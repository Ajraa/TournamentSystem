from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from .forms import *
from django.db.models import Q

# Create your views here.
def index(request):
    messages.info(request, 'ahoj')
    return render(request, 'index.html')

def playerLogin(request):
    return render(request, 'playerLogin.html', {'login_form': PlayerLoginForm})

def verifyPlayerLogin(request):
    form = PlayerLoginForm(request.GET)
    if form.is_valid():
        form_username = form.cleaned_data['username']
        form_password = form.cleaned_data['password']
        player = Player.objects.filter(username = form_username, password = form_password)
       
        if player.exists() > 0:
            return redirect('playerMainWindow', player_id = player.id)
    
def playerMainWindow(request, player_id):
    teams = Team.objects.filter(players__id=player_id)
    player = Player.objects.filter(id = player_id).first()
    return render(request, 'playerMainWindow.html', {'player_id': player_id, 'teams': teams, 'player':player})

def registerPlayer(request):
    return render(request, 'playerRegister.html', {'register_form': PlayerRegisterForm})

def addPlayer(request):
    form = PlayerRegisterForm(request.POST)
    if form.is_valid():
        fname = form.cleaned_data['fname']
        lname = form.cleaned_data['lname']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        
        player = Player(fname = fname, lname = lname, username = username, password = password)
        player.save()
        return redirect('playerMainWindow', player_id = player.id)
    
def teamWindow(request, player_id, team_id):
    team = get_object_or_404(Team, pk = team_id)
    messages.info(request, team.players)
    return render(request, 'teamWindow.html', {'players': team.players.all(), 'team': team, 'player_id': player_id})

def createTeam(request, player_id):
    return render(request, 'createTeam.html', {'create_team_form': CreateTeamForm, 'player_id': player_id})

def addTeam(request, player_id):
    form = CreateTeamForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        tag = form.cleaned_data['tag']
        
        team = Team(name = name, tag = tag)
        team.save()
        player = Player.objects.filter(id = player_id).first()
        team.players.add(player)
        
        return redirect('playerMainWindow', player_id = player_id)
    
def joinTeam(request, player_id):
    teams = Team.objects.all().exclude(players__id = player_id)
    return render(request, 'joinTeam.html', {'teams': teams, 'player_id': player_id})

def addExistingTeam(request, player_id, team_id):
    team = Team.objects.filter(id = team_id).first()
    player = Player.objects.first(id = player_id)
    team.players.add(player)
    
    return redirect('playerMainWindow', player_id = player_id)

def founderLogin(request):
    return render(request, 'founderLogin.html', {'login_form': FounderLoginForm})

def verifyFounderLogin(request):
    form = FounderLoginForm(request.GET)
    if form.is_valid():
        form_username = form.cleaned_data['username']
        form_password = form.cleaned_data['password']
        founder = Founder.objects.filter(username = form_username, password = form_password)
       
        if founder.exists() > 0:
            return redirect('founderMainWindow', founder_id = founder.id)
        
def registerFounder(request):
    return render(request, 'founderRegister.html', {'register_form': FounderRegisterForm})

def addFounder(request):
    form = FounderRegisterForm(request.POST)
    if form.is_valid():
        fname = form.cleaned_data['fname']
        lname = form.cleaned_data['lname']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        
        founder = Founder(fname = fname, lname = lname, username = username, password = password)
        founder.save()
        return redirect('founderMainWindow', founder_id = founder.id)
    
def founderMainWindow(request, founder_id):
    founder = Founder.objects.filter(id = founder_id).first()
    tournaments = Tournament.objects.filter(founder = founder).all()