from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class sbw_CustomerManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, name, password, **extra_fields):
        values = [email, name]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, password, **extra_fields)

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, name, password, **extra_fields)


class sbw_customer(AbstractBaseUser):
    email = models.EmailField()
    name = models.CharField(max_length=150, unique=True)
    school_name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    password = models.CharField(max_length=500)
    pick_up_location = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    phonenumber = models.CharField(max_length=20, null=True, blank=True)
    profile = models.ImageField(upload_to="images", null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    unique_business_id = models.CharField(max_length=50, unique=True)
    
    

    objects = sbw_CustomerManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['email', 'phonenumber','password','pick_up_location','school_name']

    def _str_(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name.split()[0]

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True