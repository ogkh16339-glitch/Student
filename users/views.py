from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm
from student_management.models import Attendance, Grade


# Notification modelini qayerda yaratgan bo'lsangiz, o'sha yerdan import qiling
# Masalan: from student_management.models import Attendance, Grade, Notification
from student_management.models import Attendance, Grade, Notification
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from student_management.models import Attendance, Grade, Notification
# ... qolgan importlar



@login_required
def student_profile(request):
    # 1. Admin bo'lsa dashboardga yuboramiz
    if request.user.is_superuser:
        return redirect('core:dashboard')

    try:
        # 2. Foydalanuvchining talaba profilini olamiz
        student = request.user.student_profile
        
        # 3. Ma'lumotlarni bazadan tortamiz
        # Baholar va Davomat (oxirgi sanasi bo'yicha)
        grades = student.grades.all().order_by('-date')
        attendances = Attendance.objects.filter(student=student).order_by('-date')
        
        # 4. BILDIRISHNOMALARNI OLAMIZ (Yangi qo'shilgan qism)
        # Oxirgi 5 ta bildirishnomani vaqt bo'yicha tartiblab olamiz
        notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:5]
        
        context = {
            'student': student,
            'grades': grades,
            'attendances': attendances,
            'notifications': notifications, # Bu qatorda HTMLga ma'lumot uzatiladi
        }
        return render(request, 'users/profile.html', context)
    
    except Exception as e:
        # Agar foydalanuvchida talaba profili bo'lmasa xato bermasligi uchun
        messages.error(request, "Sizning hisobingizga talaba profili biriktirilmagan.")
        return redirect('core:dashboard')



def register(request):
    # Login qilgan bo'lsa, tegishli joyga yuboramiz
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('core:dashboard')
        return redirect('users:student_profile')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Ro'yxatdan o'tdingiz! Endi tizimga kiring.")
            return redirect('core:login')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})





from django.http import JsonResponse
from student_management.models import Notification

@login_required
def mark_notification_read(request, notification_id):
    if request.method == 'POST':
        try:
            notification = Notification.objects.get(id=notification_id, recipient=request.user)
            notification.is_read = True
            notification.save()
            return JsonResponse({'status': 'success'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Topilmadi'}, status=404)
    return JsonResponse({'status': 'error'}, status=400)