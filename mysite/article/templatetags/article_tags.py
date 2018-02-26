from django import template 
from article.models import ArticlePost

register = template.Library()


@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()

@register.simple_tag
def author_total_articles(user):
    return user.article.count()