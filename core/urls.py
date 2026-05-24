from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    path('report/', views.report_issue, name='report'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('report/<int:pk>/', views.report_detail, name='report_detail'),
    path('export-pdf/', views.export_pdf, name='export_pdf'),
]