# Generated by Django 3.1.2 on 2020-11-09 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newspaper_app', '0002_article'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='authour',
            new_name='author',
        ),
    ]