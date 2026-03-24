from django import forms
from django.contrib.auth.models import User
from student_management.models import Student

class StudentRegistrationForm(forms.ModelForm):
    # User modeliga tegishli maydonlar
    username = forms.CharField(max_length=150, help_text="Tizimga kirish uchun login")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Xavfsiz parol kiriting")
    email = forms.EmailField(required=True)

    class Meta:
        model = Student
        # Student modelidan qaysi maydonlarni ko'rsatish kerakligi
        fields = ['first_name', 'last_name', 'birth_date', 'gender', 'current_academic_level', 'photo']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        # 1. Avval User-ni saqlaymiz
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        
        # 2. Keyin Student-ni saqlaymiz va uni User-ga bog'laymiz
        student = super().save(commit=False)
        student.user = user
        
        if commit:
            student.save()
        return student