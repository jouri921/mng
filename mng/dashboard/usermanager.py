from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

 




class User(AbstractBaseUser):    
    name = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(verbose_name='email address',max_length=255, unique=True,)
    gender = models.CharField(max_length=6, choices=(('Male', 'Male'), ('Female', 'Female')))
    notify_user_by_email = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) 
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
    
    
    
    
    
    
    
    from .models import User, Post
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserForm(UserCreationForm):
    class Meta():
        model = User
        fields = ('name', 'email', 'user_image', 'password1', 'password2')
    
    
    
    
    

def user_update(request, slug):
    user_info = get_object_or_404(User, email=slug)
    form = UserForm(instance=user_info)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user_info)
        if form.is_valid():
            form.save()
            messages.success(request, 'User has been updated')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Form! Please try again!')
            
    context = {
        'user_info' : user_info,
        'form' : form
    }
    return render(request, 'blogApp/user_update.html', context)

def user_register(request):
    form = UserForm()   
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form)
            photo = form.cleaned_data['user_image']
            name = form.cleaned_data['name']
            username = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password, name=name, photo=photo)
            messages.success(request, 'Registered successfully')
            return redirect('login')
        else :
            messages.error(request, "Registration failed")
            
    context = {
        'register_form' : form
    }
    return render(request, 'blogApp/register_page.html', context)
            
def user_login(request):
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        user = form.get_user()
        if user:
            messages.success(request, 'Login successfully')
            login(request, user)
            return redirect('home')
    context = {
        'login_form' : form
    }
    return render(request, 'blogApp/login_page.html', context)

def user_logout(request):
    messages.success(request, 'Logout successfully')
    logout(request)
    return redirect('home')



























































from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.deletion import CASCADE
from django.template.defaultfilters import slugify

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email field is mandatory')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff True')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser True')
        
        return self.create_user(email, password, **extra_fields)
        
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email Address', unique=True)
    name = models.CharField(max_length=30, unique=True)
    user_image = models.ImageField(upload_to='userphotos/', default='avatar.png')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__ (self):
        return self.email
    
    class Meta:
        ordering = ["email"]
        verbose_name_plural = "Users"
        db_table = "Users" 

class Post(models.Model):
    title = models.CharField(max_length=30, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='postimages/')
    publish_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    CATEGORY = {
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Fullstack', 'Fullstack'),
    }
    category = models.CharField(max_length=20, choices=CATEGORY)
    STATUS = {
        ('Draft', 'Draft'),
        ('Published', 'Published')
    }
    status = models.CharField(max_length=20, choices=STATUS)
    post_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    User.username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
        
    def __str__ (self):
        return self.title
    
    class Meta:
        ordering = ["title"]
        verbose_name_plural = "Posts"
        db_table = "Posts"
        
class Likes(models.Model):
    likes_owners = models.ForeignKey(User, on_delete=CASCADE)
    likes_posts = models.ForeignKey(Post, on_delete=CASCADE)
    
    def __str__ (self):
        return self.likes_posts
    
    def total_likes(self):
        return self.like_set.all().count()
    
    class Meta:
        ordering = ["likes_posts"]
        verbose_name_plural = "Likes"
        db_table = "Likes"
    
class Comments(models.Model):
    content = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True) 
    comments_owners = models.ForeignKey(User, on_delete=CASCADE)
    comments_posts = models.ForeignKey(Post, on_delete=CASCADE)
    
    def __str__ (self):
        return self.comments_posts
    
    class Meta:
        ordering = ["comments_posts"]
        verbose_name_plural = "Comments"
        db_table = "Comments"
    
class PostViews(models.Model):
    views_owners = models.ForeignKey(User, on_delete=CASCADE)
    views_posts = models.ForeignKey(Post, on_delete=CASCADE)
    
    def __str__ (self):
        return self.views_posts
    
    class Meta:
        ordering = ["views_posts"] 
        verbose_name_plural = "Postviews"
        db_table = "Postviews"