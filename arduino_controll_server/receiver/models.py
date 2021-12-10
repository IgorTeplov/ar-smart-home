from django.db import models


class CommandLog(models.Model):
	who = models.CharField(max_length=64)
	command = models.CharField(max_length=64)
	key = models.CharField(max_length=64)

class EnterLog(models.Model):
	who = models.CharField(max_length=64)
	key = models.CharField(max_length=64)
