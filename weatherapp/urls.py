from .views import HelloAPI
from django.urls import path


urlpatterns = [
    path('api/hello', HelloAPI.as_view(), name='hello-api'),

]