# Generated by Django 3.1.1 on 2020-11-11 16:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pref_cate', models.ManyToManyField(to='newspaper_app.Category')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('author', models.CharField(max_length=50)),
                ('date', models.DateField(default=datetime.date.today)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newspaper_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newspaper_app.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newspaper_app.profile')),
            ],
            options={
                'unique_together': {('article', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('like_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='newspaper_app.like')),
                ('content', models.TextField(default='')),
                ('date', models.DateField(default=datetime.date.today)),
                ('replyToComment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='newspaper_app.comment')),
            ],
            bases=('newspaper_app.like',),
        ),
    ]
