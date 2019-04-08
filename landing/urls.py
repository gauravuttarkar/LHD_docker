from django.urls import path
from . import views
from events import urls as events_urls
from django.urls import path, include
from donations import urls as donations_urls

urlpatterns = [
    path('', views.home),
    path('events/', include(events_urls)),
    path('donations/', include(donations_urls)),
    path('login', views.login1,name="login"),
    path('login-submit', views.logging_in, name="logging_in"),
    path('signup', views.signup,name="signup"),
    path('signup_submit', views.signup_submit, name="signup_submit"),
    path('logout', views.logout,name="logout"),

]

