from django.contrib import admin
from .models import UserProfile, Review ,UserRating, Game, GameRating,Post,PostRating,Comment,PostReport,UserReport,GameReport,Follower,Following,CreatorNotification,UserNotification
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(UserRating)
admin.site.register(Game)
admin.site.register(GameReport)
admin.site.register(GameRating)
admin.site.register(Post)
admin.site.register(PostRating)
admin.site.register(PostReport)
admin.site.register(UserReport)
admin.site.register(Comment)
admin.site.register(Follower)
admin.site.register(Following)
admin.site.register(CreatorNotification)
admin.site.register(UserNotification)
admin.site.register(Review)
