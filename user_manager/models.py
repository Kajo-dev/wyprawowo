from django.db import models
from Wyprawowo import settings
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('has_payment', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, first_name, last_name,  **extra_fields)


    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('has_payment', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password, first_name, last_name, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    has_payment = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(blank=True)
    avatar = models.URLField(blank=False, null=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            full_name = f"{self.user.first_name} {self.user.last_name}"
            self.slug = slugify(full_name)
            unique_slug = self.slug
            num = 1
            while Profile.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user)

    def like(self, user):
        like, created = Like.objects.get_or_create(user=user, profile=self)
        return created

    def unlike(self, user):
        Like.objects.filter(user=user, profile=self).delete()

    def likes_count(self):
        return Like.objects.filter(profile=self).count()

    def is_liked_by(self, user):
        return Like.objects.filter(user=user, profile=self).exists()


def profile_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


class Question(models.Model):
    text = models.CharField(max_length=200)
    is_multiple_answer = models.BooleanField(default=False)
    is_profile = models.BooleanField(default=False)
    requires_text_input = models.BooleanField(default=False)  # New field

    def __str__(self):
        return str(self.text)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=200)

    def __str__(self):
        return str(self.text)


class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, blank=True)
    text_answer = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(f'{self.user}: {self.question.text} - {self.answer.text}' )

# post_save.connect(profile_create, sender=settings.AUTH_USER_MODEL)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'profile')

    def __str__(self):
        return f"{self.user} likes {self.profile}"


class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('text', 'Text'),
        ('event', 'Event'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=5, choices=POST_TYPE_CHOICES, default='text')
    content = models.TextField(blank=True, null=True)
    hashtags = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content if self.post_type == 'text' else f"{self.event.title}"



class EventPostType(models.Model):
    text = models.CharField(default='Nieznany', max_length=255)

    def __str__(self):
        return self.text


class EventPost(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='event')
    event_type = models.ForeignKey(EventPostType, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    event_type = models.CharField(max_length=255)
    when = models.DateTimeField(default=timezone.now)
    date_end = models.DateTimeField(blank=True, null=True)
    where = models.CharField(max_length=255)
    number_of_people = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.first_name} likes {self.post}"


class SharedPost(models.Model):
    original_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shared_posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} shared {self.original_post.content[:20]}"


class PostAttachment(models.Model):
    Attachment_TYPE_CHOICES = [
        ('photo', 'photo'),
        ('video', 'video'),
        ('file', 'file'),
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachments')
    type = models.CharField(choices=Attachment_TYPE_CHOICES, max_length=6)
    attachment_url = models.URLField()

    def __str__(self):
        return self.attachment_url