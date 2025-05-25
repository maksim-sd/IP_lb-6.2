from django.urls import path
from .api import api
from . import views


urlpatterns = [
    path('', views.main),
    path('api/', api.urls)
]