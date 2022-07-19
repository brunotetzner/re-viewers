from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email: str, password: str, **kwargs: dict):
        if not email or not password:
            raise ValueError({ "error": "The email and password must be set" }, 400)
        
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        
        user.set_password(password)
        user.save(using=self.db)
        
        return user
    
    
    def create(self, email: str, password: str, **kwargs: dict):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        
        return self._create_user(email, password, **kwargs)
    
    
    def create_superuser(self, email: str, password: str, **kwargs: dict):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        
        return self._create_user(email, password, **kwargs)
