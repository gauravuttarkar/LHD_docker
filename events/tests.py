
import unittest
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from .models import Event

from django.db import connections



class SimpleTest(unittest.TestCase):
	def test_event(self):
		client = Client()
		events = Event.objects.all()
		response = client.get('/events/')
		self.assertEqual(response.status_code, 200)
		print("Event ID",'ibWygf5WTkdGnP9yTy',"works")
		print("-"*50)





		#user = User.objects.create_user(username='pass1', email='temporary@gmail.com', password='pass1')
		#print(user)
		#self.assertEqual(client.login(username="temp",password="temp"),True)

