from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
	path('donor/<str:eventId>',views.donor),
	path('receiver/submit/<str:eventId>',views.receiverSubmit),
	path('receiver/<str:eventId>',views.receiver),

	path('',views.index),
]