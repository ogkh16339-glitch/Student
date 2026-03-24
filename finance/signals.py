from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from .models import Payment, StudentBalance

@receiver(post_save, sender=Payment)
def update_student_balance(sender, instance, created, **kwargs):
    """To'lov saqlangandan keyin talaba balansini yangilash"""
    if created:  # Faqat yangi to'lov yaratilganda (bir marta) ishlaydi
        try:
            # 1. Talaba uchun balans ob'ektini olish yoki (yo'q bo'lsa) yaratish
            balance_obj, _ = StudentBalance.objects.get_or_create(student=instance.student)
            
            # 2. To'lov summasi borligini tekshirish va Decimal'ga o'tkazish
            if instance.amount:
                # request.POST dan kelyotgan bo'lsa str bo'lishi mumkin, shuning uchun Decimal(str()) xavfsiz
                amount_to_add = Decimal(str(instance.amount))
                
                # 3. Balansni yangilash
                balance_obj.balance += amount_to_add
                balance_obj.save()
                
        except Exception as e:
            # Xatolikni konsolga chiqarish (masalan, StudentBalance topilmasa)
            print(f"Balansni yangilashda xato yuz berdi: {e}")