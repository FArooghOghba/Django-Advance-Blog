from django.db import models
from django.contrib.auth import get_user_model


# Getting user model
# User = get_user_model()


# Create your models here.

class Post(models.Model):
    """
    This is a model class to define posts for blog app.
    """

    title = models.CharField(max_length=255)
    author = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    content = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False)
    published_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_snippet(self):
        return f'{self.content[:15]}...'

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
