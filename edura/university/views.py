from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import University


from django.shortcuts import render
from .models import University

def university_list(request):
    universities = University.objects.all()
    return render(request, 'university/list.html', {'universities': universities})

from django.shortcuts import get_object_or_404

def university_detail(request, slug):
    university = get_object_or_404(University, slug=slug)
    return render(request, 'university/detail.html', {'university': university})