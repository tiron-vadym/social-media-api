import os
import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from django.utils.text import slugify


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


def profile_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(instance.title)}-{uuid.uuid4()}.{extension}"

    return os.path.join("uploads", "profile", filename)


class User(AbstractUser):
    username = None
    email = models.EmailField(
        _(
            "email address",
        ),
        unique=True,
    )
    picture = models.ImageField(null=True, upload_to=profile_image_file_path)
    bio = models.TextField(blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email


class UserRelation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_relations"
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following_relations",
        null=True,
        blank=True,
    )
    followers = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower_relations",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.email} : {self.following.email} {self.followers}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=profile_image_file_path, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.created_at}"
