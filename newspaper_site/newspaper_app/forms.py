from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["pref_cate"]
