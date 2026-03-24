from django.shortcuts import render, get_object_or_404,redirect
from .forms import StudentForm 
from django.contrib import messages
from .models import Student, Attendance, Grade
from datetime import date
from django.db.models import Q

from django.db.models import Avg


from django.core.paginator import Paginator # Sahifalash uchun

from django.shortcuts import render
from  .models import News  # News modelini import qilamiz
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from .models import Student



def index(request):
    # Eng so'nggi 3 ta yangilikni olamiz
    latest_news = News.objects.all().order_by('-created_at')[:3]
    return render(request, 'student_management/index.html', {'latest_news': latest_news})


def student_list(request):
    query = request.GET.get('q')
    course = request.GET.get('course')
    
    # Barcha talabalarni tartib bilan olish
    student_list = Student.objects.all().order_by('-created_at')

    # Filtrlash (avvalgi kodimiz)
    if query:
        student_list = student_list.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
    if course:
        student_list = student_list.filter(current_academic_level=course)

    # PAGINATION QISMI:
    paginator = Paginator(student_list, 10) # Har bir sahifada 10 tadan talaba
    page_number = request.GET.get('page')
    students = paginator.get_page(page_number)

    return render(request, 'list.html', {'students': students})


# 2. Yangi talaba qo'shish (form.html uchun)
def student_create(request):
    if request.method == "POST":
        # Rasm yuklanishi uchun request.FILES juda muhim
        form = StudentForm(request.POST, request.FILES) 
        if form.is_valid():
            student=form.save()
            messages.success(request, f"Student {student}was created sucessfully")
            # Saqlab bo'lgach, ro'yxat sahifasiga o'tish
            return redirect("students:student_profile", pk=student.pk)
    else:
        # Agar metod GET bo'lsa, bo'sh forma ochiladi
        form = StudentForm()
    
    context = {
        'form': form,
        'title': 'Add New Student',
    }
    return render(request, 'form.html', context)


def student_edit(request,pk):

    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        # Rasm yuklanishi uchun request.FILES juda muhim
        form = StudentForm(request.POST, request.FILES, instance=student) 
        if form.is_valid():
            student=form.save()
            messages.success(request, f"Student {student}was updated sucessfully")
            # Saqlab bo'lgach, ro'yxat sahifasiga o'tish
            return redirect("students:student_profile", pk=student.pk)
    else:
        # Agar metod GET bo'lsa, bo'sh forma ochiladi
        form = StudentForm(instance=student)
    
    context = {
        'form': form,
        'title': 'Update Student',
    }
    return render(request, 'form.html', context)




def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, f"Student {student}was created sucessfully")
        return redirect('students:student_list')





# views.py ichida


def student_profile(request, pk):
    # 1. Talabani UUID bo'yicha qidiramiz (topilmasa 404 beradi)
    student = get_object_or_404(Student, pk=pk)
    
    # 2. Talabaning barcha baholarini olamiz
    # related_name='grades' modelda yozilgan bo'lishi shart
    # select_related('subject') bazaga so'rovlar sonini kamaytiradi
    grades = student.grades.all().select_related('subject').order_by('-date')
    
    # 3. GPA (O'rtacha ball) ni hisoblaymiz
    # aggregate funksiyasi lug'at qaytaradi, shuning uchun ['score__avg'] ni olamiz
    average = grades.aggregate(Avg('score'))['score__avg']
    
    # Agar baholar bo'lmasa 0 qaytaramiz, bo'lsa 1 xonagacha yaxlitlaymiz
    gpa = round(average, 1) if average is not None else 0
    
    # 4. Ma'lumotlarni HTMLga yuboramiz
    context = {
        'student': student,
        'grades': grades,
        'gpa': gpa,
    }
    
    
    return render(request, 'profile.html', context)

from django.contrib import messages

def mark_attendance(request):
    today = date.today()
    students = Student.objects.filter(enrollment_status='active').order_by('first_name') # Alifbo tartibida
    
    if request.method == 'POST':
        saved_count = 0
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=today,
                    defaults={'status': status}
                )
                saved_count += 1
        
        messages.success(request, f"Muvaffaqiyatli: {saved_count} ta talaba uchun davomat saqlandi.")
        return redirect('students:student_list')

    # Qolgan qismlari o'zgarishsiz qoladi...
    current_attendance = Attendance.objects.filter(date=today)
    attendance_dict = {item.student_id: item.status for item in current_attendance}

    for student in students:
        student.today_status = attendance_dict.get(student.id, '')

    return render(request, 'students/attendance.html', {
        'students': students,
        'today': today,
    })



from django.shortcuts import render
from .models import Attendance
from datetime import date

def attendance_report(request):
    # Sanani olish
    date_str = request.GET.get('date')
    
    if not date_str:
        selected_date = date.today() # Obyekt ko'rinishida olish yaxshiroq
    else:
        # Xavfsizlik uchun stringni sana obyektiga aylantirish tavsiya etiladi
        selected_date = date_str

    # Ma'lumotlarni bazadan olish
    # .select_related('student') — bazaga so'rovlar sonini kamaytiradi (optimizatsiya)
    # .order_by('updated_at') — kiritilgan vaqti bo'yicha tartiblaydi
    records = Attendance.objects.filter(date=selected_date).select_related('student').order_by('updated_at')
    
    context = {
        'records': records,
        'selected_date': str(selected_date), # HTML inputda ko'rinishi uchun string qilamiz
    }
    
    return render(request, 'students/attendance_report.html', context)


from django.shortcuts import render, redirect
from .models import Student, Subject, Grade
from django.contrib import messages

from .models import Notification # Notification modelini import qilishni unutmang

def mark_grades(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject')
        subject = Subject.objects.get(id=subject_id)
        students = Student.objects.all()

        for student in students:
            score = request.POST.get(f'grade_{student.id}')
            if score:  # Agar baho kiritilgan bo'lsa
                # 1. Bahoni saqlaymiz
                grade_obj, created = Grade.objects.update_or_create(
                    student=student,
                    subject=subject,
                    defaults={'score': score}
                )
                
                # 2. BILDIRISHNOMA SHU YERDA:
                # Faqat baho kiritilgan talabaga xabar yuboramiz
                Notification.objects.create(
                    recipient=student.user,
                    message=f"Sizga {subject.name} fanidan {score} baho qo'yildi!"
                )
        
        messages.success(request, f"{subject.name} fanidan baholar va bildirishnomalar yuborildi!")
        return redirect('students:student_list')

    # GET so'rovi qismi...
    subjects = Subject.objects.all()
    students = Student.objects.all()
    return render(request, 'students/mark_grades.html', {
        'subjects': subjects,
        'students': students
    })




def gpa_analytics(request):
    # 1. Faol talabalarni baholari bilan birga olish
    students = Student.objects.filter(enrollment_status='active').prefetch_related('grades')

    all_students_data = []

    for s in students:
        full_name = f"{s.first_name} {s.last_name}"
        
        # Talabaning barcha baholarining o'rtacha qiymatini hisoblash
        # 'grades' bu Student modelidagi related_name yoki kichik harfdagi model nomi
        avg_grade = s.grades.aggregate(Avg('score'))['score__avg']
        
        gpa_val = round(float(avg_grade), 1) if avg_grade is not None else 0.0
        level = s.get_current_academic_level_display()
        
        all_students_data.append((full_name, gpa_val, level))

    # 2. GPA bo'yicha saralash (eng yuqori yuqorida)
    all_students_data.sort(key=lambda x: x[1], reverse=True)

    # 3. Grafik va Leaderboard uchun qismlarga bo'lish
    top_10 = all_students_data[:10]
    names = [item[0] for item in top_10]
    gpas = [item[1] for item in top_10]
    leaderboard_top3 = all_students_data[:3]

    context = {
        'names': names,
        'gpas': gpas,
        'all_students': all_students_data,
        'leaderboard_top3': leaderboard_top3,
    }
    
    return render(request, 'students/gpa_analytics.html', context)




