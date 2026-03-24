from django.db import models

# Create your models here.
from django.db import models
from student_management.models import Student, Group

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Naqd'),
        ('card', 'Plastik (Click/Payme)'),
        ('bank', 'Bank o\'tkazmasi'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.first_name} - {self.amount} so'm"

    class Meta:
        verbose_name = "To'lov"
        verbose_name_plural = "To'lovlar"

class StudentBalance(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='balance')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.first_name} | Balans: {self.balance}"