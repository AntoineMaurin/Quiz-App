"""Quiz_App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from quiz_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.discoverpage),
    path('play', views.playpage),
    path('pickdifficulty', views.pick_a_difficulty),
    path('pickdifficulty/<slug:quiz_slug>', views.pick_a_difficulty),
    path('cancelquiz', views.cancelquiz),
    path('search', views.search),
    path('lang/<str:language>', views.set_language),
    path('', include('quiz_creation.urls')),
    path('<str:difficulty>/<slug:quiz_slug>', views.playquiz),
]
