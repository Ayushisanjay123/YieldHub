from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.index, name='index'),
    path('login/', views.custom_login, name='login'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('about/', views.about, name='about'),
    path('logout/', views.custom_logout, name='logout'),
    path('manage-users/', views.manage_users, name='manage_users'),  # define this
path('generate-reports/', views.generate_reports, name='generate_reports'),  # define this
path('manage-communications/', views.manage_communications, name='manage_communications'),  # define this
path('platform-security/', views.platform_security, name='platform_sec
    
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('landowner/dashboard/', views.landowner_dashboard, name='landowner_dashboard'),
    path('landseeker/dashboard/', views.landseeker_dashboard, name='landseeker_dashboard'),
    path('broker/dashboard/', views.broker_dashboard, name='broker_dashboard'),

    # New for Land Seeker
    path('land/search/', views.land_search, name='land_search'),
    path('my-interests/', views.my_interests, name='my_interests'),
    path('landseeker/profile/edit/', views.edit_landseeker_profile, name='edit_landseeker_profile'),

    # New for Landowner Dashboard
    path('landowner/lands/', views.view_my_lands, name='view_my_lands'),
    path('landowner/lands/add/', views.add_land, name='add_land'),
    path('landowner/lands/<int:land_id>/edit/', views.edit_land, name='edit_land'),
    path('landowner/lands/<int:land_id>/delete/', views.delete_land, name='delete_land'),

    # Interest & Agreements
    path('express_interest/<int:land_id>/', views.express_interest, name='express_interest'),
    path('create_agreement/', views.create_agreement, name='create_agreement'),

    # Reports
    path('reports/', views.view_report, name='reports'),
]
