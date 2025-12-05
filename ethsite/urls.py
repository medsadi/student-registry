from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('walletapp.urls')),
    path('admin/', admin.site.urls),
]
