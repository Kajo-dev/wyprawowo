from django.contrib import admin
from .models import User, Profile, Question, Answer, UserResponse, Post, EventPost, Comment, PostLike, Like, PostAttachment, EventPostType


admin.site.register(User)
admin.site.register(Profile)

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserResponse)
admin.site.register(Post)
admin.site.register(PostAttachment)
admin.site.register(EventPost)
admin.site.register(EventPostType)
admin.site.register(Comment)
admin.site.register(PostLike)
admin.site.register(Like)
