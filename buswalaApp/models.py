from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class sbw_CustomerManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, name, password, **extra_fields):
        print(password)
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
    customer_status = models.IntegerField(default=0)
    otp_mob_mail = models.CharField(max_length=50, null=True, blank=True)
    
    objects = sbw_CustomerManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['email', 'phonenumber','password','pick_up_location','school_name','unique_business_id']

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
    
class sbw_driver(models.Model):
    #write driver fieds like driver_name, bus_no, address, driver_phone_no, driver_email, password,price,active_student_count,ratings,bus_driver_image
    driver_name = models.CharField(max_length=50)
    bus_no = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    driver_phone_no = models.CharField(max_length=20)
    driver_email = models.EmailField()
    password = models.CharField(max_length=500)
    profile = models.ImageField(upload_to="images", null=True, blank=True)
    bus_driver_image = models.ImageField(upload_to="images", null=True, blank=True)
    active_student_count = models.IntegerField(default=0)
    ratings = models.IntegerField(default=0)
    bus_status = models.IntegerField(default=0)
    unique_business_id = models.CharField(max_length=50, unique=True)
    driver_status = models.IntegerField(default=0)
    otp_mob_mail = models.CharField(max_length=50, null=True, blank=True)
    driver_price = models.IntegerField(default=0)
    REQUIRED_FIELDS = ['driver_name','bus_no','address','driver_phone_no','driver_email','password','driver_price']

    def _str_(self):
        return self.driver_email


#write a reviews about user and driver 
class sbw_review(models.Model):
    review_title = models.CharField(max_length=50)
    review_content = models.CharField(max_length=500)
    review_rating = models.IntegerField(default=0)
    review_date = models.DateTimeField(default=timezone.now)
    review_user = models.ForeignKey(sbw_customer, on_delete=models.CASCADE)
    review_driver = models.ForeignKey(sbw_driver, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.review_title
    
#create user booking driver bus
class sbw_bookingOrder(models.Model):
    booking_date = models.DateTimeField(default=timezone.now)
    booking_status = models.IntegerField(default=0)
    booking_driver = models.ForeignKey(sbw_driver, on_delete=models.CASCADE)
    booking_customer = models.ForeignKey(sbw_customer, on_delete=models.CASCADE)
    booking_price = models.IntegerField(default=0)
    booking_bus_no = models.CharField(max_length=50)
    booking_bus_location = models.CharField(max_length=50)
    booking_bus_image = models.ImageField(upload_to="images", null=True, blank=True)
    booking_bus_status = models.IntegerField(default=0)
    booking_bus_driver_image = models.ImageField(upload_to="images", null=True, blank=True)
    booking_payment_mode = models.CharField(max_length=100)
    booking_school_name = models.CharField(max_length=100)
    booking_order_id = models.CharField(max_length=100)

    def __str__(self):
        return self.booking_customer.name + " " + self.booking_driver.driver_name


