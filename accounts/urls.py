from django.urls import path, include

from allauth.account.views import LogoutView as LogoutOnGetView

from accounts.views import LoginOnGetView, CustomSignupView

app_name = 'accounts'


urlpatterns = [
    path('cadastrar/', CustomSignupView.as_view(), name='signup'),
    path('entrar/', LoginOnGetView.as_view(), name='login'),
    path('sair/', LogoutOnGetView.as_view(), name='logout'),
]