"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path, reverse

from rest_framework_jwt.views import obtain_jwt_token
from accounts.api.views import UserCreateView

urlpatterns = [
    path('api/posts/', include('posts.urls')),
    path('api/likes/', include('likes.urls')),
    # path('api/users/', include('accounts.urls')),
    path('api/login/', obtain_jwt_token, name='login'),
    path('api/register/', UserCreateView.as_view(), name='register'),
    path('admin/', admin.site.urls),
]