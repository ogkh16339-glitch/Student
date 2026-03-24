from django.urls import path
from . import views

app_name = 'users' # Bu namespace uchun juda muhim

urlpatterns = [
    path('register/', views.register, name='register'),
    # Mana bu qator borligiga va name='student_profile' ekanligiga ishonch hosil qiling:
    path('profile/', views.student_profile, name='student_profile'), 
    path('notification/read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    
]