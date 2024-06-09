"""
URL configuration for Accuknox_Social_Media project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
app_name = 'Social_Media'

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/login-api/", include("Social_Media.login_api.urls")),
    path("api/relations/", include("Social_Media.relations.urls")),
]