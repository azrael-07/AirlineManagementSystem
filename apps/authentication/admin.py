from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Customer, Admin, Crew, Pilot, FrontDeskAssit

# Custom User Admin Panel
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(User, CustomUserAdmin)

# Registering Concrete Person-Based Models
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "frequentFlyingNumber")
    search_fields = ("user__email", "frequentFlyingNumber")

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ("user", "name")
    search_fields = ("user__email", "name")

@admin.register(FrontDeskAssit)
class FrontDeskAssistAdmin(admin.ModelAdmin):
    list_display = ("user", "name")
    search_fields = ("user__email", "name")

@admin.register(Pilot)
class PilotAdmin(admin.ModelAdmin):
    list_display = ("user", "name")
    search_fields = ("user__email", "name")

@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ("user", "name")
    search_fields = ("user__email", "name")