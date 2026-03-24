from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
# student_management appidan kerakli modellarni chaqiramiz
from student_management.models import Subject, Student 

class Quiz(models.Model):
    title = models.CharField(max_length=255, verbose_name="Test nomi")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes', verbose_name="Fan")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    duration_minutes = models.PositiveIntegerField(default=30, verbose_name="Davomiyligi (minutda)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.subject.name})"

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Testlar"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name="Savol matni")
    image = models.ImageField(upload_to='quiz/questions/', blank=True, null=True, verbose_name="Savol rasmi")

    def __str__(self):
        return self.text[:50]

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255, verbose_name="Variant matni")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'ri javobmi?")

    def __str__(self):
        return self.text

class QuizResult(models.Model):
    # Student modeliga bog'laymiz
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    score_percentage = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.quiz.title} ({self.score_percentage}%)"

    class Meta:
        verbose_name = "Test natijasi"
        verbose_name_plural = "Test natijalari"