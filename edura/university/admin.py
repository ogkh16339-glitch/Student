from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import University, Faculty, Direction, AdmissionResult


admin.site.register(University)
admin.site.register(Faculty)
admin.site.register(Direction)
admin.site.register(AdmissionResult)