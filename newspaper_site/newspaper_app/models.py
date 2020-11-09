from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Category(models.Model):
    name = models.CharField(default="", max_length=50)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(default="No information", max_length=50)
    content = models.TextField(default="No information")
    authour = models.CharField(default="No information", max_length=50)
    date = models.DateField(default=timezone.now)
    category = models.OneToOneField(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pref_cate = models.ManyToManyField(Category)

    def __str__(self):
        return self.user.username
