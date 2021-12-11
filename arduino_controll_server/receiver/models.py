from django.db import models
from django.utils.timezone import now

class User(models.Model):
	username = models.CharField(max_length=128)

	token = models.CharField('Your TOKEN', max_length=64)
	group = models.CharField('Your GROUP', max_length=64)

	def __str__(self):
		return f'{self.username} - {self.token} - {self.group}'


class Log(models.Model):
	who = models.ForeignKey(User, on_delete=models.CASCADE)
	event = models.CharField(max_length=64)

	date = models.DateTimeField(default=now)

	def __str__(self):
		return f'{self.who.username} - {self.event} - {self.date}'
