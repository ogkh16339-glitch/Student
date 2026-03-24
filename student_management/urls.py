from django.urls import path
from . import views, ajax_views

app_name = 'students'

urlpatterns = [
    # Talabalar boshqaruvi
    path("list/", views.student_list, name='student_list'), 
    path("create/", views.student_create, name='student_create'),
    path("<uuid:pk>/update/", views.student_edit, name='student_edit'),
    path("<uuid:pk>/delete/", views.student_delete, name='student_delete'),
    path("<uuid:pk>/profile/", views.student_profile, name='student_profile'),

    # Davomat va Baholash
    path('attendance/', views.mark_attendance, name='attendance'), 
    path('attendance/report/', views.attendance_report, name='attendance_report'),
    path('mark-grades/', views.mark_grades, name='mark_grades'),
    path('gpa-analytics/', views.gpa_analytics, name='gpa_analytics'),
    

    # Ajax
    path("ajax/update-profile-picture/", ajax_views.update_student_profile_picture, name="ajax_update_student_profile_picture"),
]