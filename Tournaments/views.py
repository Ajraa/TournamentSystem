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
       
        if player.exists():
            return redirect('playerMainWindow', player_id = player.first().id)
    
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
    tournaments = Tournament.objects.filter(teams__id = team_id).all()
    return render(request, 'teamWindow.html', {'players': team.players.all(), 'team': team, 'player_id': player_id, 'tournaments': tournaments})

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
            return redirect('founderMainWindow', founder_id = founder.first().id)
        
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
    
    return render(request, 'founderMainWindow.html', {'founder': founder, 'tournaments': tournaments})

def tournamentWindow(request, founder_id, tournament_id):
    tournament = Tournament.objects.filter(id = tournament_id).first()
    matches = Match.objects.filter(tournament = tournament).all()
    form = CreateMatchForm()
    choices = []
    for i in tournament.teams.all():
        choices.append((i.id, i))
    form.fields['teams'].choices = choices
    
    return render(request, 'tournamentWindow.html', {'founder_id': founder_id, 'tournament': tournament, 'matches': matches,
                                                     'teams': tournament.teams.all(), 'create_match_form': form})
    
def createTournament(request, founder_id):
    return render(request, 'createTournament.html', {'founder_id': founder_id, 'create_tournament_form': CreateTournamentForm})

def addTournament(request, founder_id):
    form = CreateTournamentForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        max_teams = form.cleaned_data['max_teams']
        start_time = form.cleaned_data['start_time']
        
        founder = Founder.objects.filter(id = founder_id).first()
        tournament = Tournament(name = name, max_teams = max_teams, start_time = start_time, founder = founder)
        tournament.save()
        
        return redirect('founderMainWindow', founder_id = founder.id)
    return redirect('index')

def matchWindow(request, tournament_id, match_id):
    match = Match.objects.filter(id = match_id).first()
    teams = match.teams.all()
    return render(request, 'matchWindow.html', {'tournament_id': tournament_id, 'teams': teams})

def joinTournament(request, player_id, team_id):
    tournaments = Tournament.objects.exclude(teams__id = team_id)
    return render(request, 'joinTournament.html', {'player_id': player_id, 'team_id': team_id, 'tournaments': tournaments})

def addExistingTournament(request, player_id, team_id, tournament_id):
    team = Team.objects.filter(id = team_id).first()
    tournament = Tournament.objects.filter(id = tournament_id).first()
    tournament.teams.add(team)
    
    return redirect('teamWindow', player_id= player_id, team_id = team_id)

def kickPlayer(request, player_id, team_id, kicked_player_id):
    team = Team.objects.filter(id= team_id).first()
    player = Player.objects.filter(id = kicked_player_id).first()
    team.players.remove(player)
    
    return redirect('teamWindow', player_id= player_id, team_id = team_id)

def kickTeam(request, founder_id, tournament_id, team_id):
    tournament = Tournament.objects.filter(id = tournament_id).first()
    team = Team.objects.filter(id=team_id).first()
    tournament.teams.remove(team)
    
    return redirect('tournamentWindow', founder_id=founder_id, tournament_id=tournament_id)

def addMatch(request, founder_id, tournament_id):
    tounament = Tournament.objects.filter(id = tournament_id).first()
    form = CreateMatchForm(request.POST)
    if form.is_valid():
        
        teams = form.cleaned_data['teams']
        
        match = Match(tournament=tounament, state='ongoing')
        match.save()
        for i in teams:
            match.teams.add(i)
        return redirect('tournamentWindow', founder_id=founder_id, tournament_id=tournament_id)

def changeState(request, founder_id, tournament_id, match_id):
    match = Match.objects.filter(id = match_id).first()
    if match.state == 'ongoing':
        match.state = 'finished'
    else:
        match.state = 'ongoing'
    match.save()
    return redirect('tournamentWindow', founder_id=founder_id, tournament_id=tournament_id)