from django.urls import path
from hhscarper import views

app_name = 'hhscarper'

urlpatterns = [
    path('', views.DashoardView.as_view(), name='dashboard'),
    path('requests/create/', views.CreateRequestView.as_view(), name='request-create'),
    path('requests', views.ListRequestView.as_view(), name='request-list'),
]
