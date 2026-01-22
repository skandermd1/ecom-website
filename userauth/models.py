from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    title = models.CharField(max_length=10, blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)

    # avoid reverse accessor name clashes with default auth.User
    groups = models.ManyToManyField(
        Group,
        related_name='userauth_users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='userauth_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email