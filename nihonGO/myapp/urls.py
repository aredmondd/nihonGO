from django.urls import path
from . import views

urlpatterns = [
     path('translate/', views.deepl_translate_view, name='deepl_translate'),
     path('', views.home, name="home")
]