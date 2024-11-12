from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect

# User manager
class MyUserManager(BaseUserManager):
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

# Custom user model
class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email']),
        ]

# User profile
User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True)
    role = models.CharField(max_length=20)  # Example roles: 'landowner', 'landseeker'
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

# Landowner model
class Landowner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='landowner')
    landowner_id = models.AutoField(primary_key=True)
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Landowner'
        verbose_name_plural = 'Landowners'
        ordering = ['last_name', 'first_name']

# Land model
class Land(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    location = models.CharField(max_length=255,blank=True,null=True)
    size = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)

    def __str__(self):
        return self.name

class LandListing(models.Model):
    land = models.ForeignKey(Land, on_delete=models.CASCADE, default=1)  # assuming the default Land instance has ID 1
    description = models.TextField()
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)

    def __str__(self):
        return f"Listing for {self.land.name}"

# LandSeeker model
class LandSeeker(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(default='2000-01-01')
    crop_requirements = models.TextField()
    desired_land_size = models.FloatField()
    address = models.CharField(max_length=255)
    interests = models.ManyToManyField(Land, through='Interest')
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Land Seeker'
        verbose_name_plural = 'Land Seekers'
        ordering = ['last_name', 'first_name']

# Interest model
class Interest(models.Model):
    land_seeker = models.ForeignKey(LandSeeker, on_delete=models.CASCADE)
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    expressed_interest_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.land_seeker} interested in {self.land} on {self.expressed_interest_date}"

    class Meta:
        verbose_name = 'Interest'
        verbose_name_plural = 'Interests'
        ordering = ['expressed_interest_date']

# Communication model
class Communication(models.Model):
    land_seeker = models.ForeignKey(LandSeeker, on_delete=models.CASCADE, related_name='communications')
    landowner = models.ForeignKey(Landowner, on_delete=models.CASCADE, related_name='communications')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.land_seeker} to {self.landowner} on {self.sent_at}"

    class Meta:
        verbose_name = 'Communication'
        verbose_name_plural = 'Communications'
        ordering = ['sent_at']

# Review model
class Review(models.Model):
    land_seeker = models.ForeignKey(LandSeeker, on_delete=models.CASCADE, related_name='reviews')
    landowner = models.ForeignKey(Landowner, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.land_seeker} for {self.landowner} on {self.review_date} - Rating: {self.rating}"

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['review_date']

# Testimonial model
class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    feedback = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
        ordering = ['name']

# FAQ model
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['question']

# View to manage listings
# def manage_listings(request):
#     # Get the Landowner instance for the logged-in user
#     landowner = get_object_or_404(Landowner, user=request.user)

#     # Fetch the listings for the logged-in Landowner
#     listings = Land.objects.filter(landowner=landowner)

#     if request.method == 'POST':
#         # Handle the update of the land listing
#         listing_id = request.POST.get('listing_id')
#         land_name = request.POST.get('land_name')
#         location = request.POST.get('location')
#         size = request.POST.get('size')
#         soil_type = request.POST.get('soil_type')
#         water_availability = request.POST.get('water_availability') == 'on'

#         # Fetch the specific listing and update it
#         listing = get_object_or_404(Land, id=listing_id, landowner=landowner)
#         listing.name = land_name
#         listing.location = location
#         listing.size = size
#         listing.soil_type = soil_type
#         listing.water_availability = water_availability
#         listing.save()

#         return redirect('manage_listings')  # Redirect to the same page after updating

#     return render(request, 'manage_listings.html', {'listings': listings})


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class LandListing(models.Model):
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="land_listings",blank=True, null=True)
    land_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100,blank=True, null=True)
    size = models.DecimalField(max_digits=10, decimal_places=2, help_text="Size in acres or square meters",blank=True, null=True)
    soil_type = models.CharField(max_length=50,blank=True, null=True)
    water_availability =models.CharField(max_length=100)
    image = models.ImageField(upload_to='land_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.land_name
