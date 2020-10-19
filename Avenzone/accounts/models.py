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


def get_upload_path_images(instance, filename):
    # upload path for images
    return 'posts/images/{0}/{1}'.format(instance.user.id, filename)


def get_upload_path_files(instance, filename):
    # upload path for files
    return 'posts/images/{0}/{1}'.format(instance.user.id, filename)

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
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    gender = models.CharField(choices=GENDERS, max_length=1, default='')
    dob = models.DateField(blank=True)
    # Unique QR code for every User
    qr_code = models.UUIDField(max_length=36, unique=True, default=uuid.uuid4)
    profile_pic = models.ImageField(
        default='default_pic.jpg', upload_to='profilepictures', null=False)
    joined = models.DateField()
    # Secret key used for email verification
    secretkey = models.PositiveIntegerField(blank=True)
    email_verified = models.BooleanField(default=False)
    # User is verified or not (Greater than a certain follower count)(Checked by Admins)
    is_verified = models.BooleanField(default=False)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    avencoins = models.DecimalField(decimal_places=2, default=0, max_digits=10)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        indexes = [models.Index(fields=['id']),
                   models.Index(fields=['qr_code'])]

    def __str__(self):
        return "{} - {}".format(self.id, self.auth_user.username)

    def save(self, *args, **kwargs):  # change image to 300x300 if bigger
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


# Rating for user by another user
class UserRating(models.Model):
    rated_for = models.ForeignKey(User, on_delete=models.CASCADE)
    rated_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rate = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(6)], blank=False)
    review = models.TextField(blank=True)

    # rated for and raded by must be unique together so one cannot repeat
    class Meta:
        unique_together = ['rated_for', 'rated_by']

    def __str__(self):
        return f'{self.rated_by.auth_user.username} rated User {self.rated_for.username}'


class Game(models.Model):                                                     # Table for games
    name = models.CharField(max_length=50, unique=True)
    players = models.PositiveIntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    thumbpic = models.ImageField(
        default='controller_default.jpg', upload_to='gamethumbnails', null=False)
    rating = models.DecimalField(decimal_places=2, max_digits=3, blank=False)
    desc = models.TextField(blank=True)
    steamlink = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.name

    # Game thumbnail more than 400x300 will be converted
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.thumbpic.path)
        if img.height > 400 or img.width > 300:
            output_size = (400, 300)
            img.thumbnail(output_size)
            img.save(self.thumbpic.path)


# Rating for game by a user
class GameRating(models.Model):
    rated_for = models.ForeignKey(Game, on_delete=models.CASCADE)
    rated_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rate = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(6)], blank=False)
    review = models.TextField(blank=True)
    reviewed_on = models.DateTimeField(blank=True)

    class Meta:
        unique_together = ['rated_for', 'rated_by']

    def __str__(self):
        return f'{self.rated_by.auth_user.username} rated Game_ID {self.rated_for.pk}'


# Table for posts by users
class Post(models.Model):
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    caption = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    postimage = models.ImageField(upload_to=get_upload_path_images, blank=True)
    postdata = models.FileField(upload_to=get_upload_path_files, blank=True)
    slug = models.SlugField(max_length=50, blank=False, default='')
    posted_on = models.DateTimeField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True)

    def save(self, *args, **kwargs):
        value = f"{self.pk}-{self.caption}"
        # Create slug for urls
        slugi = slugify(value, allow_unicode=True)
        self.slug = slugi
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug


# Rating for post by a user
class PostRating(models.Model):
    rated_for = models.ForeignKey(Post, on_delete=models.CASCADE)
    rated_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rate = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(6)], blank=False)
    review = models.TextField(blank=True)

    class Meta:
        unique_together = ['rated_for', 'rated_by']

    def __str__(self):
        return f'{self.rated_by.auth_user.username} rated Post_ID {self.rated_for.pk}'


# Table for comments on a post
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    comment_on = models.DateTimeField()

    def __str__(self):
        return f'{self.post.pk}-{self.comment_by.auth_user.username}-{self.pk}'


# tables containing reports for posts
class PostReport(models.Model):
    report_desc = models.TextField(blank=False)
    reported_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reported_to = models.ForeignKey(Post, on_delete=models.CASCADE)
    report_time = models.DateTimeField()

    class Meta:
        unique_together = ['reported_by', 'reported_to']

    def __str__(self):
        return f"post({self.reported_to.pk})-{self.reported_by.auth_user.username}-{self.pk}"


# tables containing reports for users
class UserReport(models.Model):
    report_desc = models.TextField(blank=False)
    reported_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reported_to = models.ForeignKey(User, on_delete=models.CASCADE)
    report_time = models.DateTimeField()

    class Meta:
        unique_together = ['reported_by', 'reported_to']

    def __str__(self):
        return f"user({self.reported_to.username})-{self.reported_by.auth_user.username}-{self.pk}"


# tables containing reports for games
class GameReport(models.Model):
    report_desc = models.TextField(blank=False)
    reported_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reported_to = models.ForeignKey(Game, on_delete=models.CASCADE)
    report_time = models.DateTimeField()

    class Meta:
        unique_together = ['reported_by', 'reported_to']

    def __str__(self):
        return f"game({self.reported_to.pk})-{self.reported_by.auth_user.username}-{self.pk}"


# tables containing followers corresponding to the user
class Follower(models.Model):

    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    followed_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        # user and follower must be unique together
        unique_together = ['auth_user', 'followed_by']

    def __str__(self):
        return f'{self.auth_user.username} followed by {self.followed_by.auth_user.username}'

class GameFollower(models.Model):

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    followed_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        # user and follower must be unique together
        unique_together = ['game', 'followed_by']

    def __str__(self):
        return f'{self.game.name} followed by {self.followed_by.auth_user.username}'

class GameFollowing(models.Model):

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    followed_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        # user and follower must be unique together
        unique_together = ['game', 'followed_to']

    def __str__(self):
        return f'{self.game.name} followed by {self.followed_to.auth_user.username}'


# tables containing gamers which the user is following
class Following(models.Model):

    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    followed_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        # user can follow a gamer only one time
        unique_together = ['auth_user', 'followed_to']

    def __str__(self):
        return f'{self.auth_user.username} followed by {self.followed_to.auth_user.username}'


# notifications created by creators
class CreatorNotification(models.Model):
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f'{self.pk}-{self.title}'


# user will only get the notifications of only those gamers which he is following
class UserNotification(models.Model):
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(CreatorNotification, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk}-{self.content.title}'

# to get back the feedback from user

class Review(models.Model):
    name= models.CharField(max_length=30, blank=False)
    email = models.CharField(max_length=50,blank = False)
    feed = models.TextField(blank = False)

    def __str__(self):
        return self.name
