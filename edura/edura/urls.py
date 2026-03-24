from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  
from quiz.views import QuizListView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace="core")),
    path('quiz/', include('quiz.urls')),
    path('', QuizListView.as_view(), name='home'),
    path('accounts/', include('users.urls')),
    path('students/', include('student_management.urls', namespace="students")),
    path('universities/', include('university.urls')),
    
    
]

# MEDIA va STATIC fayllarni DEBUG rejimida o'qish uchun
if settings.DEBUG:
    # Bu qism yuklangan media rasmlarni ko'rsatadi
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Bu qism static (CSS, JS, tayyor rasmlar) fayllarni ko'rsatadi
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])