"""
URL configuration for TournamentSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Tournaments import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('/playerLogin', views.playerLogin, name='playerLogin'),
    path('/playerLogin/verifyPlayerLogin', views.verifyPlayerLogin, name='verifyPlayerLogin'),
    path('/playerMainWindow/<int:player_id>', views.playerMainWindow, name='playerMainWindow'),
    path('/registerPlayer', views.registerPlayer, name='registerPlayer'),
    path('/registerPlayer/addPlayer', views.addPlayer, name='addPlayer'),
    path('/playerMainWindow/<int:player_id>/teamWindow/<int:team_id>', views.teamWindow, name='teamWindow'),
    path('/playerMainWindow/<int:player_id>/createTeam', views.createTeam, name='createTeam'),
    path('/playerMainWindow/<int:player_id>/createTeam/addTeam', views.addTeam, name='addTeam'),
    path('/playerMainWindow/<int:player_id>/joinTeam', views.joinTeam, name='joinTeam'),
    path('/playerMainWindow/<int:player_id>/joinTeam/eddExistingTeam/<int:team_id>', views.addExistingTeam, name='addExistingTeam')
]
