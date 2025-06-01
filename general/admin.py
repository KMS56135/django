from django.contrib import admin
from .models import Yacht, YachtPhoto, Booking, UserProfile

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('yacht', 'user', 'start_date', 'end_date')
    list_filter = ('yacht', 'user', 'start_date')
    search_fields = ('yacht__name', 'user__username')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)

@admin.register(Yacht)
class YachtAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_day', 'location')
    search_fields = ('name', 'location')

@admin.register(YachtPhoto)
class YachtPhotoAdmin(admin.ModelAdmin):
    list_display = ('yacht', 'description')
    search_fields = ('yacht__name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'phone')

# Register your models here.
