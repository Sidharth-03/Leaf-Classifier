from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.Welcome),
    path('home.html',views.Welcome),
    path('contact.html',views.Contact),
    path('mainpage.html',views.Mainpage),
    path('result',views.Predictor,name='result'),
    path('login.html', views.Login, name='login'),
    path('signup.html', views.Register, name='register'),



]
