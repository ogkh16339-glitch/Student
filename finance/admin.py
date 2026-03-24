from django.contrib import admin
from .models import Payment, StudentBalance
from django.utils.html import format_html

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('get_student_full_name', 'amount_formatted', 'payment_method', 'date')
    list_filter = ('payment_method', 'date')
    search_fields = ('student__first_name', 'student__last_name', 'amount')
    date_hierarchy = 'date'
    readonly_fields = ('date',)

    def amount_formatted(self, obj):
        return f"{obj.amount:,.0f} so'm".replace(',', ' ')
    amount_formatted.short_description = 'To\'lov summasi'

    def get_student_full_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"
    get_student_full_name.short_description = 'Talaba'


@admin.register(StudentBalance)
class StudentBalanceAdmin(admin.ModelAdmin):
    # XATONI TUZATISH: 'balance' maydonini list_display ga qo'shdik
    list_display = ('get_student_full_name', 'balance', 'balance_status', 'last_updated')
    
    search_fields = ('student__first_name', 'student__last_name')
    
    # Endi 'balance' list_display da borligi uchun list_editable ishlaydi
    list_editable = ('balance',)

    def balance_status(self, obj):
        color = 'green' if obj.balance >= 0 else 'red'
        return format_html(
            '<b style="color: {};">{}</b>',
            color,
            "Qarzdorlik yo'q" if obj.balance >= 0 else "Qarzdor"
        )
    balance_status.short_description = 'Holati'

    def get_student_full_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"
    get_student_full_name.short_description = 'Talaba'