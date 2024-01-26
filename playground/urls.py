from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello),
    path('caching/', views.trying_cache),
    path('hello_view/', views.HelloView.as_view())
]
