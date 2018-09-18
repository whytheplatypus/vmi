from django.urls import path

from . import views

urlpatterns = [
    path('openid-configuration', views.Wellknown.as_view()),
]
