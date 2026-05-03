from django.contrib import admin
from django.urls import path, include
from Tournaments import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    path('', views.index, name='index'),

    path('role-select/', views.role_select, name='role_select'),
    path('role-select/set/<str:role>/', views.set_role, name='set_role'),

    # Player
    path('player/dashboard/', views.player_dashboard, name='player_dashboard'),
    path('player/team/<int:team_id>/', views.team_window, name='team_window'),
    path('player/team/<int:team_id>/kick/<int:kicked_player_id>/', views.kick_player, name='kick_player'),
    path('player/team/create/', views.create_team, name='create_team'),
    path('player/team/create/save/', views.add_team, name='add_team'),
    path('player/team/join/', views.join_team, name='join_team'),
    path('player/team/join/<int:team_id>/', views.add_existing_team, name='add_existing_team'),
    path('player/team/<int:team_id>/tournament/join/', views.join_tournament, name='join_tournament'),
    path('player/team/<int:team_id>/tournament/join/<int:tournament_id>/', views.add_existing_tournament, name='add_existing_tournament'),

    # Founder
    path('founder/dashboard/', views.founder_dashboard, name='founder_dashboard'),
    path('founder/tournament/<int:tournament_id>/', views.tournament_window, name='tournament_window'),
    path('founder/tournament/<int:tournament_id>/kick/<int:team_id>/', views.kick_team, name='kick_team'),
    path('founder/tournament/create/', views.create_tournament, name='create_tournament'),
    path('founder/tournament/create/save/', views.add_tournament, name='add_tournament'),
    path('founder/tournament/<int:tournament_id>/match/add/', views.add_match, name='add_match'),
    path('founder/tournament/<int:tournament_id>/match/<int:match_id>/state/', views.change_state, name='change_state'),
]
