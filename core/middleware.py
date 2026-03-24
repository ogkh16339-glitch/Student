from django.utils import timezone

class UpdateLastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # request.user endi mavjud, chunki AuthenticationMiddleware tepada
        if request.user.is_authenticated:
            from core.models import Profile
            Profile.objects.update_or_create(
                user=request.user,
                defaults={'last_seen': timezone.now()}
            )
        return self.get_response(request)