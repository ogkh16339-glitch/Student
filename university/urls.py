from django.urls import path
from . import views

urlpatterns = [
    path('', views.university_list, name='university_list'),
    
    path('<slug:slug>/', views.university_detail, name='university_detail'),
    
]