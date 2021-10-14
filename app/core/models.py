from django.db import models
from django.contrib.auth.models import BaseUserManager, \
  AbstractBaseUser, PermissionsMixin
from django.core.validators import  RegexValidator


class UserManager(BaseUserManager):
  """User manager for the user db model"""

  def create_user(self, email, password=None, **extra_fields):
    """Create, save and return new user with email & password"""

    if not email:
      raise ValueError('Users must have a valid email address')

    user = self.model(email=self.normalize_email(email), **extra_fields)

    user.set_password(password)

    user.save(using=self._db)

    return user

  def create_superuser(self, email, password):
    """Create a new super user"""

    user = self.create_user(email=email, password=password)

    user.is_superuser = True

    user.is_staff = True

    user.save(using=self._db)

    return user  

class User(AbstractBaseUser, PermissionsMixin):
  """Db model for application user"""

  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.EmailField(max_length=255, unique=True)
  username = models.CharField(unique=True, max_length=100)
  bio = models.TextField(blank=True)
  country = models.CharField(max_length=255)
  avatar = models.CharField(max_length=255)
  phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
  phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  has_on_boarded = models.BooleanField(default=False)
  is_email_verified = models.BooleanField(default=False)
  is_phone_verified = models.BooleanField(default=False)

  objects = UserManager()

  USERNAME_FIELD = 'email'

