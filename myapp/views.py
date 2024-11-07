from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import LandListing

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import get_user_model
from datetime import datetime
from .models import Land,Landowner, LandSeeker, Interest, UserProfile

# Import the custom user model
MyUser = get_user_model()

# Index view (Homepage)
def index(request):
    return render(request, 'index.html')

# Land list view
class LandListingView(View):
    def get(self, request):
        lands = Land.objects.all()
        current_year = datetime.now().year

        context = {
            'lands': lands,
            'current_year': current_year,
        }

        return render(request, 'land_listing.html', context)

# View for displaying the land seeker's interests
@method_decorator(login_required, name='dispatch')
class MyInterestsView(ListView):
    template_name = 'my_interests.html'
    context_object_name = 'interests'

    def get_queryset(self):
        land_seeker = get_object_or_404(LandSeeker, user=self.request.user)
        return Interest.objects.filter(land_seeker=land_seeker)

# Land seeker profile view
@method_decorator(login_required, name='dispatch')
class LandSeekerProfileView(DetailView):
    model = LandSeeker
    template_name = 'landseeker_profile.html'
    context_object_name = 'land_seeker'

    def get_object(self, queryset=None):
        return get_object_or_404(LandSeeker, user=self.request.user)

# Land owner profile view
@method_decorator(login_required, name='dispatch')
class LandOwnerProfileView(DetailView):
    model = Landowner
    template_name = 'landowner_dashboard.html'
    context_object_name = 'land_owner'

    def get_object(self, queryset=None):
        return get_object_or_404(Landowner, user=self.request.user)

# Custom login view to handle role-based redirection
class CustomLoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user using email and password
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.role == 'landowner':
                    return redirect('landowner_dashboard')
                elif user_profile.role == 'landseeker':
                    return redirect('landseeker_profile')
            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found.")
                return redirect('index')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

# Registration view
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')

        # Validate required fields
        if not all([first_name, last_name, email, password, role]):
            messages.error(request, "All fields are required.")
            return redirect('register')

        # Check for existing email
        if MyUser.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect('register')

        # Create the user
        try:
            user = MyUser.objects.create_user(
                email=email, password=password, first_name=first_name, last_name=last_name
            )
            # Create user profile with role
            user_profile = UserProfile.objects.create(user=user, role=role, gender=gender)

            # Role-specific profile creation
            if role == 'landowner':
                Landowner.objects.create(user=user, gender=gender)
            elif role == 'landseeker':
                LandSeeker.objects.create(user=user, gender=gender)

            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"Registration failed: {e}")
            return redirect('register')

# Custom logout view
class CustomLogoutView(LogoutView):
    next_page = 'login'

# Static pages views
def services(request):
    return render(request, 'services.html')
def logout1(request):
    return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# Featured lands view
def featured_lands(request):
    lands = Land.objects.all()
    return render(request, 'featured_lands.html', {'lands': lands})

# Testimonials page
def testimonials(request):
    return render(request, 'testimonials.html')

# FAQ page
def faq(request):
    return render(request, 'faq.html')

# Land details view
def land_details(request, pk):
    try:
        land = Land.objects.get(pk=pk)
    except Land.DoesNotExist:
        raise Http404("No Land matches the given query.")

    return render(request, 'land_details.html', {'land': land})

@login_required
def landowner_dashboard(request):
    return render(request, 'landowner_dashboard.html')

@login_required
def landseeker_profile(request):
    return render(request, 'landseeker_profile.html')


@login_required
def add_land_listing(request):
    if request.method == "POST":
        land_name = request.POST.get('land_name')
        location = request.POST.get('location')
        size = request.POST.get('size')
        soil_type = request.POST.get('soil_type')
        water_availability = request.POST.get('water_availability')
        image = request.FILES.get('image')
        description = request.POST.get('description')

        # Save data to the model
        land_listing = LandListing(
            owner=request.user,
            land_name=land_name,
            location=location,
            size=size,
            soil_type=soil_type,
            water_availability=water_availability,
            image=image,
            description=description
        )
        land_listing.save()

        return redirect('landowner_dashboard')  # Redirect to the dashboard or another page after saving
    return render(request, 'add_land_listing.html')


@login_required
def manage_listings(request):
    # Get the Landowner instance for the logged-in user
    landowner = get_object_or_404(Landowner, user=request.user)  # Adjust this if the relationship is different

    # Fetch the listings for the logged-in Landowner
    listings = Land.objects.filter(landowner=landowner)

    if request.method == 'POST':
        # Handle the update of the land listing
        listing_id = request.POST.get('listing_id')
        land_name = request.POST.get('land_name')
        location = request.POST.get('location')
        size = request.POST.get('size')
        soil_type = request.POST.get('soil_type')
        water_availability = request.POST.get('water_availability')

        # Fetch the specific listing and update it
        listing = get_object_or_404(Land, id=listing_id, landowner=landowner)
        listing.name = land_name  # Ensure this matches your model's field names
        listing.location = location
        listing.size = size
        listing.soil_type = soil_type
        listing.water_availability = water_availability
        listing.save()

        return redirect('manage_listings')  # Redirect to the same page after updating

    return render(request, 'manage_listings.html', {'listings': listings})
