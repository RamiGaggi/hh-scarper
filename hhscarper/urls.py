from django.urls import path
from hhscarper import views

app_name = 'hhscarper'

urlpatterns = [
    path('', views.DashoardView.as_view(), name='dashboard'),
    path('requests', views.RequestListView.as_view(), name='request-list'),
    path('requests/create/', views.RequestCreateView.as_view(), name='request-create'),
    path('requests/detail/<int:pk>/', views.RequestDetailView.as_view(), name='request-detail'),
]
