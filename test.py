import unittest
from django.test import Client
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from events.models import Event

class SimpleTest(unittest.TestCase):
	def test_event(self):
		client = Client()
		print("Test1")
		events = Event.objects.all()
		print(events)
		for event in events:
			response = client.get('/events'+event.eventId)
			self.assertEqual(response.status_code, 200)
			print("Event ID",event.eventId,"works")
			print("-"*50)