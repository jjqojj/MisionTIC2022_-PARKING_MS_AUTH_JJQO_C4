from django.db                   import models
from django.contrib.auth.models  import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, ):
        #validate that username don't be empty
        if not username:
            raise ValueError('the username must not be empty')

        user = self.model(username=username)
        user.set_password(password)

        #saving the user in the database
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given username and password.
        """
        user = self.create_user(username=username, password=password)
        # user.is_staff = True
        user.is_admin = True

        #saving the superuser in the database
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    #is_active = models.BooleanField(default=True)
    id = models.BigAutoField(primary_key=True)
    username = models.CharField('username',max_length=50, unique=True)
    password = models.CharField('password',max_length=256)
    name= models.CharField('name',max_length=50,null=True, blank=True)
    email = models.EmailField('email',max_length=100,null=True, blank=True)

    def save(self,**kwargs):
        some_salt = 'A9LdseGRzMZDzGEy8D3b4M4'
        self.password = make_password(self.password,some_salt)

        #calling the superclass (AbstractBaseUser) save in db, reciving the kwargs
        super().save(**kwargs)
    
    objects = UserManager()
    USERNAME_FIELD = 'username'