from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
# for internalization support in future
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

# Create your models here.
# This is the Manager model of the custom user model that defines the functions thats needed for an user creation


class CustomUserManager(BaseUserManager):
    '''
    Custom manager for CustomUser model
    '''

    # This function creats the user, the extra fields will the contain all the additional fields we need
    # If you need to add validation for any field then mention it as args for this function
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        # normalizes the email given
        email = self.normalize_email(email=email)
        # sets the default value for a field
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # converts the password to hashed string
        user.save(using=self._db)
        print(f"User details: {user}")
        return user

    # This is the function which gets called when we create a superuser
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    '''
    Custom user model where email is the unique identifier for authentication
    '''
    #  The _("email_address") part is used for internationalization (i18n). It marks the field's verbose name (email_address) for translation into other languages.
    # Here the _ is used for internalization of that field
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), max_length=30, unique=True)
    firstname = models.CharField(_("first name"), max_length=150, blank=True)
    lastname = models.CharField(_("last name"), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this admin site.")
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=("Designates whether the user should be treated as active. "
                   "Unselect this instead of deleting accounts."
                   )
    )
    date_joined = models.DateTimeField(_("date joined"), default=now)

    # Here we call the manager class and link it with the model
    objects = CustomUserManager()

    # This below statement tells the model that while we execute the command of createsuperuser
    # instead of prompting the user with their username this will prompt them for the email
    USERNAME_FIELD = 'email'

    # The fields inside this list will be prompted to the user for input while creating a superuser
    REQUIRED_FIELDS = ["username"]

    class Meta:
        # The name that will be displayed in the Django Admin panel
        verbose_name = _("user")
        verbose_name_plural = _("users")

    # Returns the strigified version of the object, here it returns the user email
    def __str__(self):
        return self.email
