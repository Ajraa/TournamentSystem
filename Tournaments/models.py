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
    #captain = models.ForeignKey(Player, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.tag} {self.name}'
    
class Founder(models.Model):
    fname = models.CharField(max_length = 50)
    lname = models.CharField(max_length = 50)
    username = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    #koment
    
    def __str__(self):
        return f'{self.fname} {self.lname}, {self.username}'

class Tournament(models.Model):
    founder = models.ForeignKey(Founder, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team)
    
    def __str__(self):
        return f'Tournament - {self.founder}, {self.teams}'
    
class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    #left_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    #right_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team)
    state = models.CharField(max_length = 9)
    
    def __str__(self):
        return f'Match - {self.state} - {self.tournament}, {self.teams}'