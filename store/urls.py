from django.urls import path
from . import views


app_name = 'store'

urlpatterns = [  
    path('', views.IndexView.as_view(), name='index'),
    path('adm/', views.AdminDashboardView.as_view(), name='admin_dashboard'),

]