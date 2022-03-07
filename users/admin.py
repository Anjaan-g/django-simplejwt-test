from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'user_uuid','role','first_name', 'last_name','phone_no',
                    'is_active', 'is_admin',]
    list_filter = [ 'is_active','role','is_admin']
    list_editable = ('role',)

    fieldsets = (

        (None, {'fields': ('first_name', 'last_name','user_uuid','role', 'email','phone_no' ,'password')}),

        ('Permissions', {'fields': ('is_staff',
                                    'is_admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name','user_uuid', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)