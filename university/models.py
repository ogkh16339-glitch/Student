from django.db import models

# Create your models here.
from django.db import models


from django.db import models
from django.utils.text import slugify

class University(models.Model):
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='universities/', blank=True, null=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, blank=True)  # slug field qo‘shildi

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # 🔥 BU YERDA save() metodi
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Faculty(models.Model):
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name='faculties'
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.university.name})"


class Direction(models.Model):
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name='directions'
    )
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='directions'
    )

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.university.name}"


class AdmissionResult(models.Model):
    LANGUAGE_CHOICES = (
        ('uz', 'O‘zbek'),
        ('ru', 'Rus'),
    )

    STUDY_TYPE = (
        ('day', 'Kunduzgi'),
        ('evening', 'Kechki'),
        ('external', 'Sirtqi'),
    )

    direction = models.ForeignKey(
        Direction,
        on_delete=models.CASCADE,
        related_name='results'
    )

    year = models.IntegerField()
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES)
    study_type = models.CharField(max_length=10, choices=STUDY_TYPE)

    grant_score = models.FloatField()
    contract_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.direction.name} ({self.year})"