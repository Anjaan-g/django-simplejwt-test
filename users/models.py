import uuid
import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager

# Create your models here.
ROLES = (('Superadmin','Superadmin'),('Admin','Admin'),('User','User'))
class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_uuid = models.CharField(max_length=255,unique=True)
    email = models.EmailField(unique=True, db_index=True,null=True)
    phone_no = models.CharField(max_length=50,null=True,unique=True)
    first_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=120, blank=True)
   
    is_admin = models.BooleanField('admin', default=False)
    role = models.CharField(max_length=40,choices=ROLES,default='User',blank=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_no', ]

    ordering = ('created',)

    # class Meta:
    #     managed=True
    #     db_table = 'account_customuser'

    def get_full_name(self):
        if self.first_name and self.last_name:
            return (self.first_name +" " +self.last_name)
        else:
            return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        if self.email:
            return f'{self.email}'
        else:
            return f'{self.phone_no}'
            
    # def save(self, *args, **kwargs):
    #     # call the compress function
    #     if self.avatar:
    #         new_image = compress(self.avatar)
    #         # set self.image to new_image
    #         self.avatar = new_image
    #         # save
    #     super().save(*args, **kwargs)