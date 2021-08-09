from django.urls import path
from hh_scarper import views

app_name = 'hh_scarper'

urlpatterns = [
    path('', views.index),
]
