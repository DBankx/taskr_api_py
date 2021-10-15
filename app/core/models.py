from django.db import models
from django.contrib.auth.models import BaseUserManager, \
  AbstractBaseUser, PermissionsMixin
from django.core.validators import  RegexValidator
from django.conf import settings


class UserManager(BaseUserManager):
  """User manager for the user db model"""

  def create_user(self, email, password=None, **extra_fields):
    """Create, save and return new user with email & password"""

    if not email:
      raise ValueError('Users must have a valid email address')

    user = self.model(email=self.normalize_email(email), avatar=f'https://ui-avatars.com/api/?name={extra_fields.get("name")}', **extra_fields)

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

  name_regex = RegexValidator(regex=r"^([ \u00c0-\u01ffa-zA-Z'\-])+$", message='Name format is invalid')
  name = models.CharField(validators=[name_regex], max_length=255, blank=False, null=False)
  email = models.EmailField(max_length=255, unique=True, blank=False)
  username = models.CharField(unique=True, max_length=100, blank=False)
  bio = models.TextField(blank=True)
  country = models.CharField(max_length=255, blank=True)
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


class Task(models.Model):
	"""Db model for task"""

	title = models.CharField(max_length=255, blank=False)
	description = models.TextField(blank=True)
	price = models.DecimalField(decimal_places=2, max_digits=5, blank=False)
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	delivery_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title
