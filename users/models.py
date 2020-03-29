import os
from django.db import models
from django.contrib.auth.models import AbstractUser


def user_upload_path(instance, filename):
    _, ext = os.path.splitext(filename)
    return 'users/{0}/avatar{1}'.format(instance.id, ext)


class User(AbstractUser):
    avatar = models.ImageField(upload_to=user_upload_path)
    about = models.TextField(max_length=500, default='')

    def save(self, *args, **kwargs):
        if self.id is None:
            saved = []
            for f in User._meta.get_fields():
                if isinstance(f, models.FileField):
                    saved.append((f.name, getattr(self, f.name)))
                    setattr(self, f.name, None)
            super(User, self).save(*args, **kwargs)
            for name, val in saved:
                setattr(self, name, val)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
