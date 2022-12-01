from email.policy import default
from statistics import mode
from unittest.util import _MAX_LENGTH
from xmlrpc.client import boolean
from django.db import models

# Create your models here.
class questions(models.Model):
    question = models.CharField(max_length=255)
    withname = models.BooleanField(default=False)
class duelll(models.Model):
    question = models.CharField(max_length=255)
    withname = models.BooleanField(default=False)
class koo(models.Model):
    question = models.CharField(max_length=255)
    withname = models.BooleanField(default=False)
class casuall(models.Model):
    question = models.CharField(max_length=255)
    withname = models.BooleanField(default=False)
class questionshot(models.Model):
    question = models.CharField(max_length=255)
    withname = models.BooleanField(default=False)

class gamesss(models.Model):
    gameid = models.CharField(max_length=255)
    userid = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    M = models.IntegerField(default=10)
    

