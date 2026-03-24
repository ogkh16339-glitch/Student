import base64
import json
import os
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Student

@csrf_exempt
def update_student_profile_picture(request):
    if request.method == 'POST':
        try:
            # JavaScript JSON yuborgani uchun ma'lumotni body orqali olamiz
            data = json.loads(request.body)
            student_id = data.get('student_id')
            image_data = data.get('image')  # Base64 string

            if not image_data or not student_id:
                return JsonResponse({'status': 'error', 'message': 'Ma’lumotlar to‘liq emas'}, status=400)

            # 1. Talabani qidirish
            try:
                student = Student.objects.get(id=student_id)
            except Student.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Talaba topilmadi'}, status=404)

            # 2. Base64 stringni qayta ishlash
            # Format: "data:image/png;base64,iVBOR..."
            if "base64," not in image_data:
                return JsonResponse({'status': 'error', 'message': 'Rasm formati noto‘g‘ri'}, status=400)

            header, imgstr = image_data.split(';base64,')
            ext = header.split('/')[-1]  # png, jpg, jpeg

            # 3. Eski rasmni o'chirish (Server xotirasini tejash uchun)
            if student.photo and os.path.isfile(student.photo.path):
                # Agar bu default rasm bo'lmasa, o'chiramiz
                if 'profile-img.png' not in student.photo.path:
                    os.remove(student.photo.path)

            # 4. Yangi rasmni yaratish
            file_name = f"student_{student_id}_{os.urandom(4).hex()}.{ext}"
            image_file = ContentFile(base64.b64decode(imgstr), name=file_name)

            # 5. Saqlash
            student.photo.save(file_name, image_file, save=True)

            return JsonResponse({
                'status': 'success',
                'message': 'Profil rasmi muvaffaqiyatli yangilandi!',
                'image_url': student.photo.url
            })

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Noto‘g‘ri JSON formati'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f"Xatolik yuz berdi: {str(e)}"}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Faqat POST so‘rov qabul qilinadi'}, status=405)