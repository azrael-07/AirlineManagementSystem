from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Person, Customer, Admin as AdminRole, Crew, Pilot, FrontDeskAssit

# Customizing the User Admin Panel
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
admin.site.register(Person)
admin.site.register(Customer)
admin.site.register(AdminRole)
admin.site.register(Crew)
admin.site.register(Pilot)
admin.site.register(FrontDeskAssit)