from slugify import slugify

from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    user     = models.ForeignKey(User, related_name='courses_user')

    title    = models.CharField(max_length=200)
    slug     = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kargs):
        self.slug = slugify(self.title)
        super().save(*args, **kargs)

    def __str__(self):
        return self.title