from django import template 
from article.models import ArticlePost
#创建了一个实例对象register，这个对象包含了simple_tag方法（以及另外两种）
register = template.Library()


@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()

@register.simple_tag
def author_total_articles(user):
    return user.article.count()


@register.inclusion_tag('article/list/latest_articles.html')  # 确定所渲染的模板文件
def latest_articles(n=5):
    latest_articles = ArticlePost.objects.order_by("-created")[:n]
    # 返回字典类型的数据，此数据被应用到上面所指定的模板文件中
    return {"latest_articles": latest_articles}

