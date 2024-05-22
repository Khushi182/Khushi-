from django.contrib import admin
from authapp.models import Membership
from .models import KickboxingRegistration
from .models import ZumbaRegistration
from .models import CrossfitRegistration
from .models import YogaRegistration
from .models import Trainer
from .models import FreePassRequest

# Register your models here.
@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'address', 'age', 'gender', 'phone_number', 'date_of_joining',]


@admin.register(KickboxingRegistration)
class KickboxingRegistrationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'date_of_joining', 'age', 'gender', 'phone_number', 'payment_option']

    def has_add_permission(self, request, obj=None):
        # Disable the ability to add new KickboxingRegistration instances from the admin
        return False

@admin.register(ZumbaRegistration)
class ZumbaRegistrationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'date_of_joining', 'age', 'gender', 'phone_number', 'payment_option']

    def has_add_permission(self, request, obj=None):
        # Disable the ability to add new KickboxingRegistration instances from the admin
        return False

@admin.register(CrossfitRegistration)
class CrossfitRegistrationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'date_of_joining', 'age', 'gender', 'phone_number', 'payment_option']

    def has_add_permission(self, request, obj=None):
        # Disable the ability to add new KickboxingRegistration instances from the admin
        return False

@admin.register(YogaRegistration)
class YogaRegistrationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'date_of_joining', 'age', 'gender', 'phone_number', 'payment_option']

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'age', 'gender', 'address', 'phone_number', 'email']

@admin.register(FreePassRequest)
class FreePassRequestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'age', 'phone_number', 'email', 'trial_date']
