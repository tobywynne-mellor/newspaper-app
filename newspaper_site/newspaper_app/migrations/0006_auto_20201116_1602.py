# Generated by Django 3.1.2 on 2020-11-16 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newspaper_app', '0005_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='', upload_to=''),
            preserve_default=False,
        ),
    ]