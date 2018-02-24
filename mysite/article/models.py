from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from slugify import slugify
# Create your models here.

class ArticleColumn(models.Model):
    user    = models.ForeignKey(User, related_name='article_column')
    column  = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column


class ArticlePost(models.Model):
    author = models.ForeignKey(User, related_name="article")
    column = models.ForeignKey(ArticleColumn, related_name="article_column")
    users_like = models.ManyToManyField(User, related_name="articles_like", blank=True)

    title   = models.CharField(max_length=200)
    slug    = models.SlugField(max_length=200)
    body    = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated",)
        index_together = (('id', 'slug'),)  # 给这两个字段添加索引

    def __str__(self):
        return self.title

    # 覆盖默认的save方法
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("article:article_detail", args=[self.id, self.slug])

    def get_url_path(self):
        return reverse("article:list_article_detail", args=[self.id, self.slug])