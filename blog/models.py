import os
from django.db import models
from users.models import User


def tag_upload_path(instance, filename):
    _, ext = os.path.splitext(filename)
    return 'blog/tags/{0}/{1}{2}'.format(instance.id, instance.slug, ext)


def post_upload_path(instance, filename):
    _, ext = os.path.splitext(filename)
    return 'blog/posts/{0}/{1}{2}'.format(instance.id, instance.slug, ext)


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    image = models.ImageField(upload_to=tag_upload_path)
    slug = models.SlugField(max_length=150, unique=True)
    highlights = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.id is None:
            saved = []
            for f in Tag._meta.get_fields():
                if isinstance(f, models.FileField):
                    saved.append((f.name, getattr(self, f.name)))
                    setattr(self, f.name, None)
            super(Tag, self).save(*args, **kwargs)
            for name, val in saved:
                setattr(self, name, val)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=150, blank=False, null=False)
    description = models.TextField(max_length=500, default='')
    slug = models.SlugField(max_length=150, unique=True)
    image = models.ImageField(upload_to=post_upload_path)
    content = models.TextField(max_length=65535, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    highlights = models.IntegerField(default=0)
    heart = models.IntegerField(default=0)
    tag = models.ManyToManyField(Tag, related_name='posts')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='posts')

    def save(self, *args, **kwargs):
        if self.id is None:
            saved = []
            for f in Post._meta.get_fields():
                if isinstance(f, models.FileField):
                    saved.append((f.name, getattr(self, f.name)))
                    setattr(self, f.name, None)
            super(Post, self).save(*args, **kwargs)
            for name, val in saved:
                setattr(self, name, val)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=35, blank=False, null=False)
    content = models.TextField(max_length=500, blank=False, null=False)
    heart = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL, related_name='comments')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='comments')

    def save(self, *args, **kwargs):
        if self.id is None:
            saved = []
            for f in Comment._meta.get_fields():
                if isinstance(f, models.FileField):
                    saved.append((f.name, getattr(self, f.name)))
                    setattr(self, f.name, None)
            super(Comment, self).save(*args, **kwargs)
            for name, val in saved:
                setattr(self, name, val)
        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return self.content
