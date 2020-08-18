from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    # path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    #path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('login/', views.login),
]
