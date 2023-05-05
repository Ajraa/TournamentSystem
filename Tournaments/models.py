from django.db import models

# Create your models here.

class Player(models.Model):
    fname = models.CharField(max_length = 50)
    lname = models.CharField(max_length = 50)
    username = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    
    
    def __str__(self):
        return f'{self.fname} {self.lname}, {self.username}'
    
class Team(models.Model):
    name = models.CharField(max_length = 20)
    tag = models.CharField(max_length = 3)
    players = models.ManyToManyField(Player)
    
    def __str__(self):
        return f'{self.tag} {self.name}'
    
class Founder(models.Model):
    fname = models.CharField(max_length = 50)
    lname = models.CharField(max_length = 50)
    username = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    
    def __str__(self):
        return f'{self.fname} {self.lname}, {self.username}'

class Tournament(models.Model):
    name = models.CharField(max_length=30, null=True)
    max_teams = models.IntegerField(null=True)
    start_time = models.DateTimeField(null=True)
    founder = models.ForeignKey(Founder, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team)
    
    def __str__(self):
        return f'{self.name} - {self.founder}'
    
class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team)
    state = models.CharField(max_length = 9)
    
    def __str__(self):
        return f'Match - {self.state} - {list(self.teams.all())}'