from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from address.models import AddressField


# Create your models here.

class InfoPrompt(models.Model):
    org_name = models.CharField(max_length=200)
    org_email = models.CharField(max_length=200)
    # map_updated = models.DateTimeField("last updated")


    def __str__(self):
        return self.org_name

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    org_name = models.CharField(_('organization name'), max_length=30, blank=True)
    # address = models.CharField(_('address'), max_length=60, blank=True)
    # phone = models.CharField(_('phone'), max_length=17, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the org_name plus the address, with a space in between.
        """
        full_name = '%s of %s' % (self.org_name, self.address)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.org_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

class Profile(models.Model):
    associated_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    org_name = models.CharField('Your Organization', max_length=30, blank=True, default='')
    org_desc = models.TextField(max_length=500, blank=True)
    org_phone = models.CharField(_('phone'), max_length=17, blank=True)
    org_email = models.EmailField('Your Organizations Email', max_length=254, unique=True)
    org_address = AddressField(null=True, blank=True)
    ############
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    ############

    # org_address = models.ManyToManyField(
    #      'Address', 
    #      through='AddressInfo'
    #      through_fields=('address', 'profile')
    # )

  
    # If we don't have this, it's going to say profile object only
    def __str__(self):
         return f'{self.user.username} Profile'  # it's going to print username Profile

    def save(self, *args, **kwargs):
            super().save(*args, **kwargs)

            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)