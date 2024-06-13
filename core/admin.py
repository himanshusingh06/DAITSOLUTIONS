from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, Service, UserService

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture')
    search_fields = ('user__username', 'user__email')
    list_filter = ('user__is_active', 'user__is_staff', 'user__is_superuser')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

class UserServiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'customer_description', 'status', 'details')
    search_fields = ('user__username', 'service__name', 'customer_description', 'status', 'details')
    list_filter = ('service', 'status')
    list_editable = ('status', 'details')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(UserService, UserServiceAdmin)
