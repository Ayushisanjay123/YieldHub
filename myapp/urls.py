from django.urls import path
from . import views
from .views import (
    CustomLoginView,
    CustomLogoutView,
    RegisterView,
    LandSeekerProfileView,
    LandOwnerProfileView,
    LandListingView,
    MyInterestsView,
    landowner_dashboard,
    landseeker_profile,
     manage_listings
)

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('featured-lands/', views.featured_lands, name='featured_lands'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('faq/', views.faq, name='faq'),
    path('land-details/<int:pk>/', views.land_details, name='land_details'),
    path('lands/', LandListingView.as_view(), name='land_list'),
    path('my-interests/', MyInterestsView.as_view(), name='my_interests'),
    path('landowner_dashboard/', landowner_dashboard, name='landowner_dashboard'),
    path('landseeker_profile/', landseeker_profile, name='landseeker_profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout1/', views.logout1, name='logout1'),
    path('manage-listings/', manage_listings, name='manage_listings'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # Only one logout path
    path('add-land-listing/', views.add_land_listing, name='add_land_listing'),
    path('add_land_listing1/', views.add_land_listing1, name='add_land_listing1'),
    path('land-listings/', views.land_listing_list, name='land_listing_list')
]
