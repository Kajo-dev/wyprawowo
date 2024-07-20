from django.db import models
from Wyprawowo import settings
from django.db.models.signals import post_save
from django.utils.text import slugify


from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


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
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, first_name, last_name,  **extra_fields)

      
    def create_superuser(self, email, password, first_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password, first_name, create_user, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
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
    avatar = models.URLField(blank=True, null=True)
    slug = models.SlugField(blank=False)

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


def profile_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


class Question(models.Model):
    text = models.CharField(max_length=200)
    multiple_answer = models.BooleanField(default=False)

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
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return str(f'{self.user}: {self.question.text} - {self.answer.text}' )

post_save.connect(profile_create, sender=settings.AUTH_USER_MODEL)
