from os import name
from typing import Tuple
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import uuid
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
# General Profile of the user with details
class UserProfile(models.Model):

    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=12, blank=True)
    city = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)
    gender = models.CharField(choices=GENDERS, max_length=1)
    dob = models.DateField(blank=True)
    qr_code = models.UUIDField(max_length=36, unique=True, default=uuid.uuid4)   # Unique QR code for every User
    profile_pic = models.ImageField(default='default_pic.jpg', upload_to='profilepictures', null=False)
    joined = models.DateField()
    secretkey = models.PositiveIntegerField(blank=True)   # Secret key used for email verification
    email_verified = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)       # User is verified or not (Greater than a certain follower count)(Checked by Admins)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    avencoins = models.DecimalField(decimal_places=2, default=0, max_digits=10)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        indexes = [models.Index(fields=['id']), models.Index(fields=['qr_code'])]

    def __str__(self):
        return "{} - {}".format(self.id, self.auth_user.username)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_pic.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)

# class Creator(models.Model):
#     auth_user = models.OneToOneField(User, on_delete=models.CASCADE)
#     profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     followers_count = models.PositiveIntegerField(max_length=12, default=0)
#     # following_count = models.PositiveIntegerField(max_length=12, default=0)
#     rating = models.DecimalField(decimal_places=2, max_digits=3, blank=False)

class UserRating(models.Model):
    rated_for = models.ForeignKey(User, on_delete=models.CASCADE)
    rated_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(6)], blank=False)
    review = models.TextField(blank=True)

    class Meta:
        unique_together = ['rated_for', 'rated_by']
        
    def __str__(self):
        return f'{self.rated_by.auth_user.username} rated User {self.rated_for.username}'

class Game(models.Model):
    name = models.CharField(max_length=30, unique=True)
    players = models.PositiveIntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    rating = models.DecimalField(decimal_places=2, max_digits=3, blank=False)

    def __str__(self):
        return self.name

class GameRating(models.Model):
    rated_for = models.ForeignKey(Game, on_delete=models.CASCADE)
    rated_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(6)], blank=False)
    review = models.TextField(blank=True)
    reviewed_on = models.DateTimeField(blank=True)

    class Meta:
        unique_together = ['rated_for', 'rated_by']

    def __str__(self):
        return f'{self.rated_by.auth_user.username} rated Game_ID {self.rated_for.pk}'


class Post(models.Model):
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    caption = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=50, blank=False, default='')
    posted_on = models.DateTimeField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True)

    def save(self, *args, **kwargs):
        value = f"{self.pk}-{self.caption}"
        slugi = slugify(value, allow_unicode=True)
        self.slug = slugi
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug

class PostRating(models.Model):
    rated_for = models.ForeignKey(Post, on_delete=models.CASCADE)
    rated_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(6)], blank=False)
    review = models.TextField(blank=True)

    class Meta:
        unique_together = ['rated_for', 'rated_by']

    def __str__(self):
        return f'{self.rated_by.auth_user.username} rated Post_ID {self.rated_for.pk}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    comment_on = models.DateTimeField()

    def __str__(self):
        return f'{self.post.pk}-{self.comment_by.auth_user.username}-{self.pk}'

class PostReport(models.Model):
    report_desc = models.TextField(blank = False)
    reported_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reported_to = models.ForeignKey(Post, on_delete=models.CASCADE)
    report_time = models.DateTimeField()

    class Meta:
        unique_together = ['reported_by', 'reported_to']

    def __str__(self):
        return f"post({self.reported_to.pk})-{self.reported_by.auth_user.username}-{self.pk}"

class UserReport(models.Model):
    report_desc = models.TextField(blank = False)
    reported_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reported_to = models.ForeignKey(User, on_delete=models.CASCADE)
    report_time = models.DateTimeField()

    class Meta:
        unique_together = ['reported_by', 'reported_to']

    def __str__(self):
        return f"user({self.reported_to.username})-{self.reported_by.auth_user.username}-{self.pk}"


class GameReport(models.Model):
    report_desc = models.TextField(blank = False)
    reported_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reported_to = models.ForeignKey(Game, on_delete=models.CASCADE)
    report_time = models.DateTimeField()

    class Meta:
        unique_together = ['reported_by', 'reported_to']

    def __str__(self):
        return f"game({self.reported_to.pk})-{self.reported_by.auth_user.username}-{self.pk}"

class Follower(models.Model):
    
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    followed_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['auth_user', 'followed_by']

    def __str__(self):
        return f'{self.auth_user.username} followed by {self.followed_by.auth_user.username}'


class Following(models.Model):
    
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    followed_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['auth_user', 'followed_to']

    def __str__(self):
        return f'{self.auth_user.username} followed by {self.followed_to.auth_user.username}'

class CreatorNotification(models.Model):
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f'{self.pk}-{self.title}'

class UserNotification(models.Model):
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(CreatorNotification, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk}-{self.content.title}'

