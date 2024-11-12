from django.contrib import admin
from .models import LandSeeker, Landowner, UserProfile, MyUser,LandListing

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

class MyUserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline,)
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')

class LandSeekerAdmin(admin.ModelAdmin):
    list_display = ('user_first_name', 'user_last_name', 'user_address', 'date_of_birth', 'user_gender', 'crop_requirements', 'desired_land_size')

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = 'First Name'

    def user_last_name(self, obj):
        return obj.user.last_name
    user_last_name.short_description = 'Last Name'

    def user_address(self, obj):
        return obj.user.userprofile.address
    user_address.short_description = 'Address'

    def user_gender(self, obj):
        return obj.user.userprofile.gender
    user_gender.short_description = 'Gender'

class LandownerAdmin(admin.ModelAdmin):
    list_display = ('user_first_name', 'user_last_name', 'user_address', 'contact_number', 'user_gender')

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = 'First Name'

    def user_last_name(self, obj):
        return obj.user.last_name
    user_last_name.short_description = 'Last Name'

    def user_address(self, obj):
        return obj.user.userprofile.address
    user_address.short_description = 'Address'

    def user_gender(self, obj):
        return obj.user.userprofile.gender
    user_gender.short_description = 'Gender'

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(LandSeeker, LandSeekerAdmin)
admin.site.register(Landowner)
admin.site.register(LandListing)
