from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    # Define choices as a class attribute
    STATUS_CHOICES = (
        (1, "Active"),
        (2, "Inactive"),
        (3, "Terminated"),
    )  

    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)    
    last_login = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username

    def has_module_perms(self, app_label):
        return True    

    def has_perm(self, perm, obj=None):
        return True
    

class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')

    class Meta:
        unique_together = ('from_user', 'to_user')

