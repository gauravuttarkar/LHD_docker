from django.db import models

# Create your models here.
class User(models.Model):
	uid = models.AutoField(primary_key = True)
	first_name = models.CharField(max_length = 30)
	last_name = models.CharField(max_length = 30, null= True)
	address = models.TextField()
	city = models.CharField(max_length = 30)
	state = models.CharField(max_length = 30)
	email = models.EmailField(max_length = 30)
	phone_number = models.CharField(max_length = 10)
	password = models.CharField(max_length = 20)
	date_of_birth = models.DateTimeField(null = True)
