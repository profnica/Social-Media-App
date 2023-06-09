from .models import CustomUser

class EmailAuthBackend:
    """
    Authenticate using an e-mail address.
    """
    def authenticate(self, request, email=None, password=None):
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            pass
        
        
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        
        except CustomUser.DoesNotExist:
            pass
            