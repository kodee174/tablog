# Generated by Django 3.0.3 on 2020-02-22 08:55

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('content', models.TextField(max_length=500)),
                ('heart', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to=blog.models.tag_upload_path)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('highlights', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(default='', max_length=500)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('image', models.ImageField(upload_to=blog.models.post_upload_path)),
                ('content', models.TextField(default='', max_length=65535)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('highlights', models.IntegerField(default=0)),
                ('heart', models.IntegerField(default=0)),
                ('tag', models.ManyToManyField(related_name='posts', to='blog.Tag')),
            ],
        ),
    ]