import uuid
from datetime import date
from django.db import models
from django.utils import timezone
from django.conf import settings 
from django.contrib.auth.models import User


# 1. Subject modelini birinchi yaratamiz (Grade dan tepada bo'lishi shart)
class Subject(models.Model):
    name = models.CharField('Subject Name', max_length=100)
    code = models.CharField('Subject Code', max_length=10, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name



class Teacher(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=100) # Qaysi fandan dars berishi
    salary_percentage = models.IntegerField(default=50) # O'quvchidan tushgan pulning necha foizi unga?
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.subject})"

# Group modeliga o'qituvchini bog'lashni unutmang
# Group modeli ichiga: teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)



class Group(models.Model):
    name = models.CharField('Guruh nomi', max_length=100)
    academic_level = models.CharField('Daraja', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"


# 2. Student modeli


# User modeliga bog'lanish uchun

class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    ACADEMIC_LEVEL_CHOICES = (
        ('P.1', 'Primary 1'),
        ('P.2', 'Primary 2'),
        ('P.3', 'Primary 3'),
        ('P.4', 'Primary 4'),
        ('P.5', 'Primary 5'),
    )

    ENROLLMENT_STATUS_CHOICES = (
        ('active', 'Active'),
        ('dismissed', 'Dismissed'),
        ('graduated', 'Graduated'),
        ('transferred', 'Transferred'),
    )

    # --- YANGI QO'SHILGAN QISMI ---
    # Har bir talabani tizim foydalanuvchisi (User) bilan bog'laymiz
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='student_profile',
        null=True, # Avvaldan bor talabalar uchun xato bermasligi uchun
        blank=True
    )
    # ------------------------------

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField('First Name', max_length=50)
    last_name = models.CharField('Last Name', max_length=50)
    birth_date = models.DateField('Birth Date')
    gender = models.CharField('Gender', max_length=10, choices=GENDER_CHOICES, default='M')
    current_academic_level = models.CharField('Current Academic Level', max_length=10, choices=ACADEMIC_LEVEL_CHOICES)
    enrollment_status = models.CharField('Enrollment Status', max_length=20, choices=ENROLLMENT_STATUS_CHOICES, default='active')
    photo = models.ImageField('Photo', upload_to='students/photos', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        today = date.today()
        if not self.birth_date:
            return "N/A"
        born = self.birth_date
        # Yoshi aniq hisoblash (tug'ilgan kun o'tgan yoki o'tmaganini tekshiradi)
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    @property
    def get_gpa(self):
        from django.db.models import Avg
        # related_name='grades' ishlatilgani uchun self.grades ishlaydi
        res = self.grades.aggregate(avg=Avg('score'))['avg']
        return round(res, 1) if res else 0.0

    class Meta:
        verbose_name = "Talaba"
        verbose_name_plural = "Talabalar"
        ordering = ['-created_at']

    # student_management/models.py ichida
def full_name(self):
    return f"{self.first_name} {self.last_name}"


def __str__(self):
        # Endi {{ student }} deb yozilganda ism va familiya chiqadi
        return f"{self.first_name} {self.last_name}"

# 3. Attendance modeli
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('present', 'Keldi'),
        ('absent', 'Kelmadi'),
        ('late', 'Kechikdi'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now=True) # Har saqlaganda vaqtni yangilaydi

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.first_name} - {self.date} ({self.status})"

# 4. Grade modeli (Subject va Student'dan keyin kelishi kerak)
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='student_grades')
    score = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.score}"

    class Meta:
        ordering = ['-date']





class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Xabar: {self.recipient.username} uchun"
    





class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    content = models.TextField(verbose_name="Yangilik matni")
    image = models.ImageField(upload_to='news_images/', blank=True, null=True, verbose_name="Rasm")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Muallif")
    
    # Mana shu maydonlar views.py da ishlatilgan:
    views_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    likes = models.ManyToManyField(User, related_name='news_likes', blank=True, verbose_name="Layklar")
    dislikes = models.PositiveIntegerField(default=0)
    favorites = models.ManyToManyField(User, related_name='favorite_news', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.news.title}"
    

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'news') # Bir kishi bir xil maqolani ikki marta saqlay olmaydi
        




from django.db import models
from django.contrib.auth.models import User

class VideoNews(models.Model):
    title = models.CharField(max_length=255, verbose_name="Video sarlavhasi")
    video_file = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name="Video fayl")
    video_url = models.URLField(blank=True, null=True, verbose_name="YouTube havola")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Video yangilik"
        verbose_name_plural = "Video yangiliklar"





class YouTubeVideo(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    playlist_id = models.CharField(max_length=100, help_text="Pleylist ID sini kiriting (masalan: PL...)")
    is_active = models.BooleanField(default=True, verbose_name="Saytda ko'rsatish")

    def __str__(self):
        return self.title