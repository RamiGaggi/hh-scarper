from django.urls import path
from hhscarper import views

app_name = 'hhscarper'

urlpatterns = [
    path('', views.index),
]
