from django.contrib import admin
from Tournaments.models import Player, Founder, Team, Tournament, Match

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['fname', 'lname', 'get_email']

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

@admin.register(Founder)
class FounderAdmin(admin.ModelAdmin):
    list_display = ['fname', 'lname', 'get_email']

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'founder']

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['tournament', 'state']
