"""
URL configuration for recorda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
     path('api/authent/', include('authent.urls')),
     path('api/land/', include('land.urls')),
      path('api/transaction/', include('transaction.urls')),
       path('api/search/', include('search.urls')),
    path('api/insight/', include('dashboard.urls'))
    #path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    #spath('api/auth/', include('allauth.urls')),

]
