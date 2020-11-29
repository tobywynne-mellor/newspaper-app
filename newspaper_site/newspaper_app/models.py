from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
# Create your models here.

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


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
    
    profile_pic = models.ImageField(blank=True, null=True)

    pref_cate = models.ManyToManyField(Category)
    dob = models.DateField(default=datetime.date.today, null=True, max_length=8)
    email = models.EmailField(max_length=254)

    def save(self):
        super(Profile,self).save()
        if self.profile_pic:
            resized_pic = Image.open(self.profile_pic)
            output = BytesIO()
            resized_pic = resized_pic.resize((200,200))
            resized_pic.save(output, format='PNG')
            output.seek(0)
            self.profile_pic = InMemoryUploadedFile(output,'ImageField', "%s.png" %self.profile_pic.name.split('.')[0], 'image/png', sys.getsizeof(output), None)
            super(Profile,self).save()

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
