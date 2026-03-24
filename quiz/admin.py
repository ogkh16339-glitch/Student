from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Quiz, Question, Answer, QuizResult

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4 # Default holda 4 ta variant chiqaradi

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuizResult)