from django.urls import path
from hhscarper import views

app_name = 'hhscarper'

urlpatterns = [
    path('', views.DashoardView.as_view(), name='dashboard'),

    path('requests/', views.RequestListView.as_view(), name='request-list'),
    path('requests/create/', views.RequestCreateView.as_view(), name='request-create'),
    path('requests/detail/<int:pk>/', views.RequestDetailView.as_view(), name='request-detail'),
    path('requests/delete/<int:pk>/', views.RequestDeleteView.as_view(), name='request-delete'),

    path('vacancies/', views.VacancyListView.as_view(), name='vacancy-list'),

    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),

    path('skill-report/<int:pk>/', views.SkillReportDetailView.as_view(), name='skill-report-detail'),
    path('word-report/<int:pk>/', views.WordReportDetailView.as_view(), name='word-report-detail'),

    path('export-data/', views.ExportData.as_view(), name='export-data'),
]
