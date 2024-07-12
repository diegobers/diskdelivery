from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

app_name = 'store'


urlpatterns = [  
    path('', views.IndexView.as_view(), name='index'),
    path('adm/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('entrar/', LoginView.as_view(template_name='layouts/admin-login.html'), name='login'),
]