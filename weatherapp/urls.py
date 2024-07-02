from .views import greeting
from django.urls import path


urlpatterns = [
    path('api/hello', greeting, name='hello-api'),

]