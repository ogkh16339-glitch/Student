from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Asosiy sahifalar
    path('', views.dashboard, name='dashboard'),
    path('home/', views.home, name='home'),
    
    # Avtorizatsiya
    path('login/', views.admin_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Yangiliklar (News)
    path('news/', views.news_list, name='news_list'),
    path('news/add/', views.add_news_frontend, name='add_news'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    
    # Like va Comment (Interaktivlik)
    path('news/<int:pk>/like/', views.like_news, name='like_news'),
    path('news/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('news-reaction/<int:pk>/<str:action>/', views.news_reaction, name='news_reaction'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'), # Bu ishlayapti
    path('news/bookmark/<int:news_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('profile/saved/', views.saved_news, name='saved_news'),

    path('task/add/', views.add_task, name='add_task'),
    path('task/toggle/<int:pk>/', views.toggle_task, name='toggle_task'),
    path('task/delete/<int:pk>/', views.delete_task, name='delete_task'),
    

    path('video/add/', views.add_video, name='add_video'),
    
    # Profil
    path('profile/', views.admin_profile, name='admin_profile'),
    path('profile/settings/', views.admin_profile, name='profile'),
    
    # Boshqa sahifalar
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('messages/', views.all_messages, name='all_messages'),
    path('message/<int:pk>/', views.read_message, name='read_message'),

    path('messages/', views.all_messages, name='all_messages'),
    path('message/<int:pk>/', views.read_message, name='read_message'),
    path('message/delete/<int:pk>/', views.delete_message, name='delete_message'),
    path('message/star/<int:pk>/', views.toggle_star_message, name='toggle_star_message'),
    path('message/reply/<int:pk>/', views.reply_message, name='reply_message'),
    path('api/check-messages/', views.check_messages_api, name='check_messages_api'),

    path('timetable/', views.timetable_view, name='timetable'),
    #path('timetable/delete/<int:pk>/', views.delete_timetable, name='delete_timetable'),
    
    path('timetable/delete/<int:id>/', views.delete_timetable, name='delete_timetable'),

    path('payments/', views.payment_list, name='payment_list'),
    
    path('payments/<int:pk>/', views.payment_detail, name='payment_detail'),

    path('timetable/export/', views.export_timetable_excel, name='export_timetable_excel'),
    path('timetable/import/', views.import_timetable_excel, name='import_timetable_excel'),

    path('timetable/', views.timetable_view, name='timetable'),
    path('timetable/export/', views.export_timetable_excel, name='export_timetable_excel'), # BU QATOR SHART
    path('timetable/import/', views.import_timetable_excel, name='import_timetable_excel'), # BU QATOR SHART
    path('timetable/delete/<int:id>/', views.delete_timetable, name='delete_timetable'),
]