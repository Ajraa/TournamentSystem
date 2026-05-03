from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.db.models import Q
from Tournaments.decorators import player_required, founder_required


def index(request):
    return render(request, 'index.html')


@login_required
def role_select(request):
    # Pokud user má profil, redirect na dashboard
    if hasattr(request.user, 'player_profile'):
        return redirect('player_dashboard')
    if hasattr(request.user, 'founder_profile'):
        return redirect('founder_dashboard')
    return render(request, 'role_select.html')


@login_required
def set_role(request, role):
    # Přijímá pouze POST
    if request.method != 'POST':
        return redirect('role_select')

    # Idempotentní — pokud profil existuje, redirect
    if hasattr(request.user, 'player_profile') or hasattr(request.user, 'founder_profile'):
        if hasattr(request.user, 'player_profile'):
            return redirect('player_dashboard')
        return redirect('founder_dashboard')

    if role == 'player':
        Player.objects.create(
            user=request.user,
            fname=request.user.first_name or '',
            lname=request.user.last_name or '',
        )
        return redirect('player_dashboard')
    elif role == 'founder':
        Founder.objects.create(
            user=request.user,
            fname=request.user.first_name or '',
            lname=request.user.last_name or '',
        )
        return redirect('founder_dashboard')
    return redirect('role_select')


# --- Player views ---

@player_required
def player_dashboard(request):
    player = request.user.player_profile
    teams = player.team_set.all()
    return render(request, 'playerMainWindow.html', {'player': player, 'teams': teams})


@player_required
def team_window(request, team_id):
    player = request.user.player_profile
    team = get_object_or_404(Team, id=team_id, players=player)  # membership check
    tournaments = Tournament.objects.filter(teams__id=team_id).all()
    return render(request, 'teamWindow.html', {
        'players': team.players.all(),
        'team': team,
        'player': player,
        'tournaments': tournaments,
    })


@player_required
def kick_player(request, team_id, kicked_player_id):
    player = request.user.player_profile
    team = get_object_or_404(Team, id=team_id, players=player)  # ownership check
    kicked = get_object_or_404(Player, id=kicked_player_id)
    team.players.remove(kicked)
    return redirect('team_window', team_id=team_id)


@player_required
def create_team(request):
    player = request.user.player_profile
    return render(request, 'createTeam.html', {'create_team_form': CreateTeamForm, 'player': player})


@player_required
def add_team(request):
    player = request.user.player_profile
    form = CreateTeamForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        tag = form.cleaned_data['tag']
        team = Team(name=name, tag=tag)
        team.save()
        team.players.add(player)
        return redirect('player_dashboard')
    return redirect('create_team')


@player_required
def join_team(request):
    player = request.user.player_profile
    teams = Team.objects.all().exclude(players=player)
    return render(request, 'joinTeam.html', {'teams': teams, 'player': player})


@player_required
def add_existing_team(request, team_id):
    player = request.user.player_profile
    team = get_object_or_404(Team, id=team_id)
    team.players.add(player)
    return redirect('player_dashboard')


@player_required
def join_tournament(request, team_id):
    player = request.user.player_profile
    team = get_object_or_404(Team, id=team_id)
    tournaments = Tournament.objects.exclude(teams__id=team_id)
    return render(request, 'joinTournament.html', {
        'player': player,
        'team': team,
        'tournaments': tournaments,
    })


@player_required
def add_existing_tournament(request, team_id, tournament_id):
    team = get_object_or_404(Team, id=team_id)
    tournament = get_object_or_404(Tournament, id=tournament_id)
    tournament.teams.add(team)
    return redirect('team_window', team_id=team_id)


# --- Founder views ---

@founder_required
def founder_dashboard(request):
    founder = request.user.founder_profile
    tournaments = Tournament.objects.filter(founder=founder)
    return render(request, 'founderMainWindow.html', {'founder': founder, 'tournaments': tournaments})


@founder_required
def tournament_window(request, tournament_id):
    founder = request.user.founder_profile
    tournament = get_object_or_404(Tournament, id=tournament_id, founder=founder)
    matches = Match.objects.filter(tournament=tournament).all()
    form = CreateMatchForm()
    choices = []
    for i in tournament.teams.all():
        choices.append((i.id, i))
    form.fields['teams'].choices = choices
    return render(request, 'tournamentWindow.html', {
        'founder': founder,
        'tournament': tournament,
        'matches': matches,
        'teams': tournament.teams.all(),
        'create_match_form': form,
    })


@founder_required
def kick_team(request, tournament_id, team_id):
    founder = request.user.founder_profile
    tournament = get_object_or_404(Tournament, id=tournament_id, founder=founder)
    team = get_object_or_404(Team, id=team_id)
    tournament.teams.remove(team)
    return redirect('tournament_window', tournament_id=tournament_id)


@founder_required
def create_tournament(request):
    founder = request.user.founder_profile
    return render(request, 'createTournament.html', {
        'founder': founder,
        'create_tournament_form': CreateTournamentForm,
    })


@founder_required
def add_tournament(request):
    founder = request.user.founder_profile
    form = CreateTournamentForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        max_teams = form.cleaned_data['max_teams']
        start_time = form.cleaned_data['start_time']
        tournament = Tournament(name=name, max_teams=max_teams, start_time=start_time, founder=founder)
        tournament.save()
        return redirect('founder_dashboard')
    return redirect('index')


@founder_required
def add_match(request, tournament_id):
    founder = request.user.founder_profile
    tournament = get_object_or_404(Tournament, id=tournament_id, founder=founder)
    form = CreateMatchForm(request.POST)
    if form.is_valid():
        teams = form.cleaned_data['teams']
        match = Match(tournament=tournament, state='ongoing')
        match.save()
        for i in teams:
            match.teams.add(i)
        return redirect('tournament_window', tournament_id=tournament_id)
    return redirect('tournament_window', tournament_id=tournament_id)


@founder_required
def change_state(request, tournament_id, match_id):
    founder = request.user.founder_profile
    tournament = get_object_or_404(Tournament, id=tournament_id, founder=founder)
    match = get_object_or_404(Match, id=match_id, tournament=tournament)
    if match.state == 'ongoing':
        match.state = 'finished'
    else:
        match.state = 'ongoing'
    match.save()
    return redirect('tournament_window', tournament_id=tournament_id)
