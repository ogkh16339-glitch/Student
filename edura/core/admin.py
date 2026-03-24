from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, ContactMessage, Timetable

# --- 1. USER VA PROFILE INTEGRATSIYASI ---
# Foydalanuvchi ma'lumotlarini tahrirlaganda profil ham birga chiqadi
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profil ma\'lumotlari'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone')
    
    def get_phone(self, instance):
        # Profil mavjudligini tekshirish (signal bilan yaratilgan bo'lishi kerak)
        return instance.profile.phone_number if hasattr(instance, 'profile') else "-"
    get_phone.short_description = 'Telefon'

# Standart User adminni o'chirib, o'zimiznikini o'rnatamiz
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
admin.site.register(User, UserAdmin)


# --- 2. XABARLAR (CONTACT MESSAGES) ---
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'subject', 'email', 'created_at', 'is_read', 'is_deleted')
    list_filter = ('is_read', 'is_deleted', 'is_starred', 'created_at')
    search_fields = ('full_name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    # Guruhli amallar (Actions)
    actions = ['mark_as_read', 'move_to_trash']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Tanlanganlarni o'qilgan deb belgilash"

    def move_to_trash(self, request, queryset):
        queryset.update(is_deleted=True)
    move_to_trash.short_description = "Tanlanganlarni savatga tashlash"


# --- 3. DARS JADVALI (TIMETABLE) ---
@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    # Jadvalda ko'rinadigan ustunlar
    list_display = ('group', 'get_day_display', 'start_time', 'end_time', 'room')
    
    # Filtrlash (O'ng tomonda)
    list_filter = ('day_of_week', 'room', 'group')
    
    # Qidiruv
    search_fields = ('room', 'group__name')

    def get_day_display(self, obj):
        # Choice fielddan matnli qiymatni olish (Dushanba, Seshanba...)
        return obj.get_day_of_week_display()
    get_day_display.short_description = 'Hafta kuni'


# --- 4. PROFIL (ALOHIDA KO'RISH UCHUN) ---
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username', 'phone_number')