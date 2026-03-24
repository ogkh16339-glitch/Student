from django import forms
from django.contrib.auth.models import User
from student_management.models import News
from django import forms
from .models import ContactMessage

from django import forms
from .models import Timetable

# 1. Foydalanuvchi ma'lumotlarini tahrirlash formasi
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

# 2. Yangilik qo'shish formasi
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'image', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Yangilik sarlavhasini kiriting...'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 6, 
                'placeholder': 'To\'liq matnni shu yerga yozing...'
            }),
        }




class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['full_name', 'email', 'subject', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ali Valiyev'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Savol turi'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Xabaringizni yozing...'}),
        }


class TimetableForm(forms.ModelForm):
    group = forms.ModelChoiceField(
        queryset=None, 
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Guruh"
    )

    class Meta:
        model = Timetable
        # 'teacher' maydoni olib tashlandi
        fields = ['group', 'room', 'day_of_week', 'start_time', 'end_time']
        widgets = {
            'room': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Xona...'}),
            'day_of_week': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            from student_management.models import Group
            self.fields['group'].queryset = Group.objects.all()
        except:
            self.fields['group'].queryset = Timetable.objects.none()