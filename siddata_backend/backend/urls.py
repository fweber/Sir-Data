"""siddata_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views
from . import api_views

urlpatterns = [
    # Authentication
    path('login', auth_views.LoginView.as_view(template_name="backend/login.html"), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),

    # HTML views for OER interface
    path('show_oer', views.show_oer, name="show_oer"),
    path('learning_buddies', views.learning_buddies, name="learning_buddies"),
    path('profile', views.profile, name="profile"),
    path('learning_content', views.learning_content, name="learning_content"),
    path('learning_playground', views.learning_playground, name="learning_playground"),

    # js
    path('backend.js', views.backend_js, name='backend.js'),

    ]
