from django.urls import path
from hhscarper import views

app_name = 'hhscarper'

urlpatterns = [
    path('', views.VacancyListView.as_view(), name='dashboard'),
    path('get_urls/', views.test_view, name='test'),
]
