"""
Test cases
"""
import unittest
from django.test import Client
from django.contrib.auth import get_user_model


class SimpleTest(unittest.TestCase):

	def test_signup(self):
		client = Client()
		response = client.get('/signup')
		self.assertEqual(response.status_code, 200)
		print("Sign up page working")
		print("-"*50)

	def test_login_page(self):
		client = Client()
		response = client.get('/login')
		self.assertEqual(response.status_code, 200)
		print("Login page working")
		print("-"*50)

	def test_UserLogin(self):
		client = Client()

		listUser = [
		'pass',
		'pass',
		'wrong',
		'wrong'
		]

		listPassword = [
		'pass',
		'wrong',
		'pass',
		'wrong'
		]
		User = get_user_model()
		user = User.objects.create_user('pass', 'temporary@gmail.com', 'pass')

		
		#print(client.login(username='pass',password='wrong'))
		
		for i in range(4):
			if i == 0:

				self.assertEqual( client.login(username=listUser[i], password=listPassword[i]), True)

			else:
				self.assertNotEqual( client.login(username=listUser[i], password=listPassword[i]), True)

		print("-"*50)


		#user = User.objects.create_user(username='pass1', email='temporary@gmail.com', password='pass1')
		#print(user)
		#self.assertEqual(client.login(username="temp",password="temp"),True)

