# models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin

# Custom User Manager
# --------------------------
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# --------------------------
# Custom User Model
# --------------------------
class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('landowner', 'Land Owner'),
        ('landseeker', 'Land Seeker'),
        ('broker', 'Broker'),
    )
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.email} - {self.role}"

class LandOwner(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class AgriculturalExpertise(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class LandSeeker(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=255, null=True)
    photo = models.ImageField(upload_to='seeker_photos/', null=True)
    agricultural_expertise = models.ForeignKey(AgriculturalExpertise, on_delete=models.SET_NULL, null=True)
    crop_requirement = models.CharField(max_length=255, null=True)
    desired_land_size = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Land(models.Model):
    owner = models.ForeignKey(LandOwner, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, default="To be updated")
    size = models.DecimalField(max_digits=10, decimal_places=2)
    water_availability = models.BooleanField(default=False)
    soil_type = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.location

class Interest(models.Model):
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    seeker = models.ForeignKey(LandSeeker, on_delete=models.CASCADE)
    expressed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seeker.user.email} interested in {self.land.location}"

class Broker(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.user.email

class Agreement(models.Model):
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    landowner = models.ForeignKey(LandOwner, on_delete=models.CASCADE)
    landseeker = models.ForeignKey(LandSeeker, on_delete=models.CASCADE)
    broker = models.ForeignKey(Broker, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    terms = models.TextField()

    def __str__(self):
        return f"Agreement for {self.land.location}"

class Payment(models.Model):
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100, default="Cash")

    def __str__(self):
        return f"Payment for {self.agreement.land.location}"

class Report(models.Model):
    generated_by = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
    generated_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"Report by {self.generated_by.email} on {self.generated_on}"
