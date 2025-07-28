import os
import uuid
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

def get_random_filename(instance, filename):
    ext = filename.split('.')[-1]
    random_name = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('photos', random_name)

class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    categories = models.ManyToManyField(Category, related_name='posts')
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to=get_random_filename, null=True, blank=True)

    def __str__(self):
        return f"Post {self.pk} by {self.author.username}"

    class Meta:
        ordering = ['-date']
