"""
URL configuration for backend_Libreria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# AGREGAR ESTA LÍNEA:
from app_Libreria import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_Libreria.urls')),
    # Si tienes esta línea, ELIMÍNALA o corrígela:
    # path('', views.inicio, name='inicio'),  # ← ESTA LÍNEA ESTÁ CAUSANDO EL ERROR
]