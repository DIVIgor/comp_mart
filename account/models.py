from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class NewAccManager(BaseUserManager):
    def create_superuser(
        self, email, password, first_name, **other_fields
    ):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if not other_fields.get('is_staff'):
            raise ValueError(
                'is_staff must be set True for superuser.'
            )
        if not other_fields.get('is_superuser'):
            raise ValueError(
                'is_superuser must be set true for superuser.'
            )
        
        return self.create_user(email, password, first_name, **other_fields)
    
    def create_user(self, email, password, first_name, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email'))
        
        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name, **other_fields
        )
        user.set_password(password)
        user.save()
        return user

class CMUserBase(AbstractBaseUser, PermissionsMixin):
    # name
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    # contacts
    email = models.EmailField(_('email address'), unique=True)
    phone_num = models.CharField(max_length=15, blank=True)
    # address
    country = CountryField()
    postcode = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    # user status
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = NewAccManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'div9test@gmail.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.email