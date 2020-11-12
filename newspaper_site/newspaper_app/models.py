from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.CharField(max_length=50)
    date = models.DateField(default=datetime.date.today, max_length=8)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pref_cate = models.ManyToManyField(Category)
    dob = models.DateField(default=datetime.date.today, max_length=8)

    def __str__(self):
        return self.user.username


class Like(models.Model):

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, unique=False)
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, unique=False)

    def __str__(self):
        return (self.user.user.username + " likes " + self.article.title)


class Comment(Like):
    content = models.TextField(default="", null=False)
    date = models.DateField(default=datetime.date.today, max_length=8)
    replyToComment = models.ForeignKey(
        "self", related_name="reply", blank=True, null=True, unique=False, on_delete=models.CASCADE)

    def __str__(self):
        return (self.content)
