"""pro1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from mst import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index),
    path('pdd/', views.pdd),
    path('read/', views.read),
    path('m0/', views.m0),
    path('m1/', views.m1),
    path('m2/', views.m2),
    path('m3/', views.m3),

    path('m4/', views.m4),
    path('m44/', views.m44),
    path('reply2/',views.reply2_main),
    path('reply2_list/',views.reply2_list),

    path('m5/', views.m5),
    path('m6/', views.m6),
    path('m7/', views.m7),

    path('kr_sec/',views.kr_sec),
    path('kr_stock/',views.kr_stock),

]

#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.STATIC_URL)

