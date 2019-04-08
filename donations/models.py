from django.contrib.auth.models import User
from django.db import models
from events.models import Event

# Create your models here.

class Receiver(models.Model):
	eventId = models.ForeignKey(Event,on_delete=models.CASCADE)	
	userName = models.ForeignKey(User,on_delete=models.CASCADE,default=0)
	fileName = models.CharField(max_length=20, null=True,default=None)
	bankDetails = models.CharField(max_length=20, null=True,default=None)
	comments = models.CharField(max_length=50, null=True,default=None)
