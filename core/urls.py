from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('carrinho/', include('cart.urls')),
    path('perfil/', include('accounts.urls')),
    path('perfil/', include('allauth.urls')),
    path('pedidos/', include('checkout.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)