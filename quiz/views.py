from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from .models import Quiz, Question, Answer, QuizResult
from student_management.models import Subject, Student

# 1. Testlar ro'yxati va fan bo'yicha filtr
class QuizListView(ListView):
    model = Quiz
    template_name = 'quiz/quiz_list.html'
    context_object_name = 'quizzes'

    def get_queryset(self):
        # Fan bo'yicha filtrlash mantiqi
        subject_id = self.request.GET.get('subject')
        if subject_id:
            return Quiz.objects.filter(subject_id=subject_id)
        return Quiz.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        # Tanlangan fanni select menyusida saqlab qolish uchun
        context['selected_subject'] = self.request.GET.get('subject')
        return context


# 2. Test ishlash jarayoni va natijani hisoblash
class QuizDetailView(View):
    def get(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        # Savollarni har safar har xil tartibda chiqarish
        questions = quiz.questions.all().order_by('?') 
        return render(request, 'quiz/quiz_detail.html', {
            'quiz': quiz,
            'questions': questions
        })

    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        questions = quiz.questions.all()
        score = 0
        total_questions = questions.count()

        for question in questions:
            # Formadan 'question_ID' nomi bilan kelgan javobni olish
            selected_answer_id = request.POST.get(f'question_{question.id}')
            
            if selected_answer_id:
                try:
                    answer = Answer.objects.get(id=selected_answer_id)
                    if answer.is_correct:
                        score += 1
                except Answer.DoesNotExist:
                    continue

        # Natija foizini va xatolar sonini hisoblash
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        wrong_answers = total_questions - score # O'zgaruvchi nomi to'g'irlandi

        # Talaba profilini olish (Admin yoki boshqa profil bo'lsa xato bermasligi uchun try-except)
        try:
            student_profile = request.user.student_profile
        except (AttributeError, Student.DoesNotExist):
            return render(request, 'quiz/quiz_result.html', {
                'error': "Sizda talaba profili mavjud emas. Natija saqlanmadi.",
                'result': {
                    'quiz': quiz,
                    'score_percentage': percentage,
                    'total_questions': total_questions,
                    'correct_answers': score
                },
                'wrong_answers': wrong_answers
            })

        # Natijani bazaga saqlash
        result = QuizResult.objects.create(
            student=student_profile,
            quiz=quiz,
            total_questions=total_questions,
            correct_answers=score,
            score_percentage=percentage
        )

        # Natija sahifasiga barcha kerakli ma'lumotlarni yuborish
        return render(request, 'quiz/quiz_result.html', {
            'result': result,
            'wrong_answers': wrong_answers
        })