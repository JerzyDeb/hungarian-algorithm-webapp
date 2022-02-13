"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import os

from accounts import views as account_views

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from items.views import PanelView
from plans.views import PlanView
from project.views import media_access
from project.views import AboutView


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('signup/', account_views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('panel/', PanelView.as_view(),  name='panel'),
    path('panel/plans', PlanView.as_view(),  name='plans'),
    path('about', AboutView.as_view(), name='about'),
    path('instruction/', TemplateView.as_view(template_name='instruction.html'), name='instruction'),
    url(r'^media/(?P<path>.*)', media_access, name='media'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

