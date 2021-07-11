from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('prices',views.prices ,name='prices'),
    path('pred_price', views.pred_price , name='pred_price'),
    path('result', views.result, name='result'),
]
