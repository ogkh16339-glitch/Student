from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png', blank=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    

    def __str__(self):
        return f"{self.user.username} profili"

# Avtomatik ravishda Profil yaratish (Signal)
# Foydalanuvchi ochilishi bilan unga bo'sh profil ham biriktiriladi
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()





class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_starred = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.subject}"




class Timetable(models.Model):
    DAYS_OF_WEEK = (
        (1, 'Dushanba'), 
        (2, 'Seshanba'), 
        (3, 'Chorshanba'),
        (4, 'Payshanba'), 
        (5, 'Juma'), 
        (6, 'Shanba'), 
        (7, 'Yakshanba'),
    )

    group = models.ForeignKey(
        'student_management.Group', 
        on_delete=models.CASCADE, 
        related_name='timetables'
    )
    room = models.CharField(max_length=50)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['day_of_week', 'start_time']
        unique_together = ['room', 'day_of_week', 'start_time']

    def __str__(self):
        return f"{self.group.name} | {self.get_day_of_week_display()} | {self.start_time}"
    
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['is_completed', '-created_at']

    def __str__(self):
        return self.title