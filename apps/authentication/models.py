from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group, Permission
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields ):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email = email , **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user 
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
#Account model 
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique = True)
    password = models.CharField( max_length = 128)

    #required Fields in User Auth
    is_active = models.BooleanField(default= True)
    is_staff = models.BooleanField(default= True)

    #Prevents conflict with Django’s default User.groups. and user_permissions 
    groups = models.ManyToManyField(Group, related_name="authentication_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="authentication_user_permissions", blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

#Person Model   
class Person(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    name = models.CharField(max_length= 100)
    address1 = models.CharField(max_length= 100)
    address2 = models.CharField(max_length= 100, blank=True , null= True) #Optional Field
    pinCode = models.IntegerField()
    phone = models.CharField(max_length= 10)

    def __str__(self):
        return self.name

class Customer(Person):
    pass

class Admin(Person):
    pass

class FrontDeskAssit(Person):
    pass

class Crew(Person):
    pass

class Pilot(Person):
    pass









