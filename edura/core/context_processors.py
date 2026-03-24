from .models import ContactMessage

def unread_messages_data(request):
    """
    Barcha sahifalar uchun o'qilmagan xabarlar soni va 
    oxirgi 5 ta xabarni taqdim etadi.
    """
    if request.user.is_authenticated and request.user.is_superuser:
        # O'qilmagan xabarlar ro'yxati (is_read=False)
        unread_qs = ContactMessage.objects.filter(is_read=False).order_by('-created_at')
        
        return {
            'unread_count': unread_qs.count(),        # Jami soni: {{ unread_count }}
            'unread_msgs_list': unread_qs[:5]         # Oxirgi 5 tasi: {% for msg in unread_msgs_list %}
        }
    
    # Agar foydalanuvchi admin bo'lmasa, bo'sh ma'lumot qaytaramiz
    return {
        'unread_count': 0,
        'unread_msgs_list': []
    }