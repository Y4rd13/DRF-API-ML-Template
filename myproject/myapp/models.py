from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager):
    def create_user(self, email, username, password, account_type='test'):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('Users must have a username')
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            account_type=account_type,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staffuser(self, email, username, password, account_type='developer'):
        user = self.create_user(email, username, password, account_type)
        user.is_staff = True
        user.save()
        return user

    def create_admin(self, email, username, password, account_type='admin'):
        user = self.create_user(email, username, password, account_type)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user

    def create_superuser(self, email, username, password, account_type='superuser'):
        user = self.create_user(email, username, password, account_type)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ACCOUNT_TYPES = (
        ('test', 'Test'),
        ('staging', 'Staging'),
        ('production', 'Production'),
        ('developer', 'Developer'),
        ('admin', 'Admin'),
        ('superuser', 'Superuser'),
    )
    username = models.CharField(max_length=255, unique=True, db_index=True, error_messages={'unique': ("A user with that username already exists.")})
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='test')
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True, verbose_name="Email", error_messages={'unique': ("A user with that email already exists.")})
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=255, blank=True)

    refresh_token = models.TextField(blank=True, null=True)
    
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username' # or 'email'
    REQUIRED_FIELDS = [] # don't user same as USERNAME_FIELD

    def __str__(self):
        return self.username # or 'email'

    def get_username(self):
        return self.username

    def get_account_type(self):
        return self.account_type

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True