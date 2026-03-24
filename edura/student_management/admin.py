from django.contrib import admin
from .models import (
    Subject, Teacher, Group, Student, Attendance, 
    Grade, Notification, News, Comment, VideoNews
)

# 1. Talabalar boshqaruvi
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'current_academic_level', 'enrollment_status', 'age', 'get_gpa')
    list_filter = ('enrollment_status', 'current_academic_level', 'gender', 'created_at')
    search_fields = ('first_name', 'last_name', 'id')
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)
    
    # Rasm bor-yo'qligini ko'rsatish (ixtiyoriy)
    def age(self, obj):
        return obj.age
    age.short_description = 'Yoshi'

# 2. O'qituvchilar va Guruhlar
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'phone', 'salary_percentage', 'is_active')
    list_filter = ('is_active', 'subject')
    search_fields = ('user__first_name', 'user__last_name', 'phone')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_level', 'created_at')
    search_fields = ('name',)

# 3. Davomat va Baholash
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'updated_at')
    list_filter = ('status', 'date')
    search_fields = ('student__first_name', 'student__last_name')
    date_hierarchy = 'date'

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'score', 'date')
    list_filter = ('subject', 'date')
    search_fields = ('student__first_name', 'subject__name')

# 4. Yangiliklar va Media
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'views_count', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content')
    inlines = [CommentInline] # Yangilik ichida kommentlarni ko'rish

@admin.register(VideoNews)
class VideoNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title',)

# 5. Boshqa modellar
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'is_read', 'created_at')
    list_filter = ('is_read',)

admin.site.register(Comment)

from .models import YouTubeVideo  # Model nomini tekshirib oling

@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    # Admin panel ro'yxatida ko'rinadigan ustunlar
    list_display = ('title', 'playlist_id', 'is_active')
    
    # Qaysi ustunlar bo'yicha qidirish mumkinligi
    search_fields = ('title', 'playlist_id')
    
    # O'ng tomonda filtrlar paneli
    list_filter = ('is_active',)
    
    # Ro'yxatning o'zida tahrirlash imkoniyati
    list_editable = ('is_active',)