from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
	eventId = models.CharField(max_length=100, null=False,default=None,primary_key=True)

class SafeLocation(models.Model):
	userName = models.ForeignKey(User,on_delete=models.CASCADE,default=0)
	eventId = models.ForeignKey(Event,on_delete=models.CASCADE)	
	latitude = models.DecimalField(max_digits=10,decimal_places=5, null=True,default=None)
	longitude = models.DecimalField(max_digits=10,decimal_places=5, null=True,default=None)

class DangerLocation(models.Model):
	userName = models.ForeignKey(User,on_delete=models.CASCADE,default=0)
	eventId = models.ForeignKey(Event,on_delete=models.CASCADE)	
	latitude = models.DecimalField(max_digits=10,decimal_places=5, null=True,default=None)
	longitude = models.DecimalField(max_digits=10,decimal_places=5, null=True,default=None)

class HelpLocation(models.Model):
	userName = models.ForeignKey(User,on_delete=models.CASCADE,default=0)
	eventId = models.ForeignKey(Event,on_delete=models.CASCADE)	
	latitude = models.DecimalField(max_digits=10,decimal_places=5, null=True,default=None)
	longitude = models.DecimalField(max_digits=10,decimal_places=5, null=True,default=None)		

class UserComments(models.Model):
	userName = models.ForeignKey(User,on_delete=models.CASCADE)
	eventId = models.ForeignKey(Event,on_delete=models.CASCADE,null=False,default=None)	
	userComment =  models.CharField(max_length=3000, null=True,default=None)

class bankDetails(models.Model):
	userName =  models.ForeignKey(User,on_delete=models.CASCADE)
	bankDetails = models.CharField(max_length=3000, null=True,default=None)

class Donations(models.Model):
	eventId = models.ForeignKey(Event,on_delete=models.CASCADE)
	receiver = models.ForeignKey(User,on_delete=models.CASCADE)

	