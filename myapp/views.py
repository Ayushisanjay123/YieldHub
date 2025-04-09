from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils import timezone
from .models import *
from .models import Land
from .models import Interest 
from .models import LandSeeker
from django.contrib.auth import get_backends
from .models import Agreement, Payment
from .models import Broker
from django.db import IntegrityError
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_backends,logout
from .models import MyUser, LandOwner, LandSeeker, Broker
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        address = request.POST['address']
        pincode = request.POST['pincode']
        gender = request.POST['gender']
        role = request.POST['role']
        photo = request.FILES.get('photo')

        # Check if email already exists
        if MyUser.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'error': 'Email already exists. Please use a different one.'
            })

        try:
            user = MyUser.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                address=address,
                pincode=pincode,
                gender=gender,
                photo=photo,
            )
            user.save()

            # Assign role
            if role == 'landowner':
                LandOwner.objects.create(user=user)
            elif role == 'landseeker':
                LandSeeker.objects.create(user=user)
            elif role == 'broker':
                Broker.objects.create(user=user)

            # Manually set authentication backend
            user.backend = get_backends()[0].__class__.__module__ + '.' + get_backends()[0].__class__.__name__
            login(request, user)

            return redirect(f'/{role}/dashboard')

        except IntegrityError:
            return render(request, 'register.html', {
                'error': 'An error occurred during registration. Please try again.'
            })

    return render(request, 'register.html')



def custom_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            if hasattr(user, 'landowner'):
                return redirect('/landowner/dashboard')
            elif hasattr(user, 'landseeker'):
                return redirect('/landseeker/dashboard')
            elif hasattr(user, 'broker'):
                return redirect('/broker/dashboard')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  

@login_required
def landowner_dashboard(request):
    landowner = request.user.landowner  # Get the logged-in user's landowner profile

    if request.method == 'POST':
        location = request.POST.get('location')
        size = request.POST.get('size')
        water = request.POST.get('water_availability') == 'True'
        soil = request.POST.get('soil_type')

        if location and size and soil:
            Land.objects.create(
                owner=landowner,
                location=location,
                size=size,
                water_availability=water,
                soil_type=soil
            )
            return redirect('landowner_dashboard')  # Prevents form re-submission
        else:
            # Optional: Add context for showing an error in the template
            error = "Please fill out all fields correctly."

    lands = Land.objects.filter(owner=landowner)
    interests = Interest.objects.filter(land__in=lands)

    context = {
        'lands': lands,
        'interests': interests,
        # Optional: 'error': error
    }
    return render(request, 'landowner_profile.html', context)

@login_required
def landseeker_dashboard(request):
    lands = Land.objects.all()
    seeker = request.user.landseeker
    return render(request, 'landseeker_profile.html', {'lands': lands, 'seeker': seeker})

@login_required
def express_interest(request, land_id):
    land = get_object_or_404(Land, id=land_id)
    Interest.objects.create(seeker=request.user.landseeker, land=land, expressed_on=timezone.now())
    return redirect('/landseeker/dashboard')

@login_required
def broker_dashboard(request):
    broker = get_object_or_404(Broker, user=request.user)
    agreements = Agreement.objects.filter(broker=broker)
    payments = Payment.objects.filter(agreement__broker=broker)

    return render(request, 'broker_dashboard.html', {
        'agreements': agreements,
        'payments': payments
    })

@login_required
def create_agreement(request):
    if request.method == 'POST':
        land_id = request.POST['land_id']
        seeker_id = request.POST['seeker_id']
        start = request.POST['start_date']
        end = request.POST['end_date']
        terms = request.POST['terms']

        land = Land.objects.get(id=land_id)
        seeker = LandSeeker.objects.get(id=seeker_id)
        broker = request.user.broker

        agreement = Agreement.objects.create(
            land=land, 
            landowner=land.owner, 
            landseeker=seeker, 
            broker=broker,
            start_date=start, 
            end_date=end, 
            terms=terms
        )

        Payment.objects.create(
            agreement=agreement, 
            amount=5000,  # Example amount
            payment_date=timezone.now(), 
            status='Paid'
        )

        return redirect('/broker/dashboard')
    return render(request, 'agreement.html')

@login_required
def view_report(request):
    reports = Report.objects.all()
    return render(request, 'report.html', {'reports': reports})

def land_search(request):
    query = request.GET.get('query')
    results = Land.objects.filter(is_available=True)

    if query:
        results = results.filter(location__icontains=query)

    return render(request, 'land_search.html', {'lands': results})

@login_required
def add_land(request):
    if request.method == 'POST':
        location = request.POST['location']
        size = request.POST['size']
        soil_type = request.POST['soil_type']
        water_availability = request.POST.get('water_availability') == 'on'
        is_available = request.POST.get('is_available') == 'on'

        Land.objects.create(
            owner=request.user.landowner,
            location=location,
            size=size,
            soil_type=soil_type,
            water_availability=water_availability,
            is_available=is_available
        )
        return redirect('my_lands')
    return render(request, 'landowner/add_land.html')

@login_required
def edit_land(request, land_id):
    land = get_object_or_404(Land, id=land_id, owner=request.user.landowner)
    if request.method == 'POST':
        land.location = request.POST['location']
        land.size = request.POST['size']
        land.soil_type = request.POST['soil_type']
        land.water_availability = request.POST.get('water_availability') == 'on'
        land.is_available = request.POST.get('is_available') == 'on'
        land.save()
        return redirect('my_lands')
    return render(request, 'landowner/edit_land.html', {'land': land})

def my_interests(request):
    # You can customize this part to filter based on the logged-in user if needed
    interests = Interest.objects.all()  # Replace this with filtered data if needed
    return render(request, 'my_interests.html', {'interests': interests})

def edit_landseeker_profile(request):
    landseeker = get_object_or_404(LandSeeker, user=request.user)

    if request.method == 'POST':
        landseeker.first_name = request.POST.get('first_name')
        landseeker.last_name = request.POST.get('last_name')
        landseeker.date_of_birth = request.POST.get('date_of_birth')
        landseeker.address = request.POST.get('address')
        landseeker.phone = request.POST.get('phone')
        landseeker.pincode = request.POST.get('pincode')
        landseeker.gender = request.POST.get('gender')
        landseeker.agricultural_expanse_id = request.POST.get('agricultural_expanse_id')
        
        if request.FILES.get('photo'):
            landseeker.photo = request.FILES['photo']

        landseeker.save()
        return redirect('landseeker_profile')  # or another page

    return render(request, 'edit_landseeker_profile.html', {'landseeker': landseeker})


@login_required
def view_my_lands(request):
    # Assumes each Land instance has an `owner` ForeignKey pointing to the logged-in user
    user = request.user
    lands = Land.objects.filter(owner=user)
    return render(request, 'view_my_lands.html', {'lands': lands})

@login_required
def delete_land(request, land_id):
    land = get_object_or_404(Land, id=land_id, owner=request.user)

    if request.method == "POST":
        land.delete()
        return redirect('view_my_lands')

    return render(request, 'confirm_delete_land.html', {'land': land})

def services(request):
    return render(request, 'services.html')

def contact(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request, 'faq.html')

def about(request):
    return render(request, 'about.html')

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')  # Make sure this matches the URL name
        else:
            messages.error(request, 'Invalid admin credentials')
            return redirect('admin_login')  # Note: this should match the URL name

    return render(request, 'admin_login.html')



def custom_logout(request):
    logout(request)
    return redirect('login') 


@user_passes_test(lambda u: u.is_superuser)
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')
