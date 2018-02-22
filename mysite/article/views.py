from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from .models import ArticleColumn, ArticlePost
from .forms import ArticleColumnForm, ArticlePostForm

# Create your views here.

@login_required(login_url='/account/login/')
@csrf_exempt
def article_column(request):
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request, 
                      "article/column/article_column.html", 
                      {"columns": columns, 'column_form':column_form})
    if request.method == "POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name)
        if columns:
            return HttpResponse('2')
        else:
            # 新增栏目并返回创建成功的响应
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse("1")
    
@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def rename_article_column(request):  # 重命名只接收post请求处理数据，不考虑get请求渲染表单的情况
    column_name = request.POST["column_name"]
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")

@login_required(login_url='/account/login')
@require_POST
@csrf_exempt
def del_article_column(request):  # 删除只接收post请求处理数据，不考虑get请求渲染表单的情况
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url='/account/login')
@csrf_exempt
def article_post(request):
    if request.method=="POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()  # 在页面中渲染表单
        article_columns = request.user.article_column.all()  # 在页面中渲染所有栏目
        return render(request, 
                      "article/column/article_post.html", 
                      {"article_post_form":article_post_form, "article_columns":article_columns})


@login_required(login_url='/account/login')
def article_list(request):
    # articles = ArticlePost.objects.all()
    articles = ArticlePost.objects.filter(author=request.user)
    return render(request, "article/column/article_list.html", {"articles":articles})

@login_required(login_url='/account/login')
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, "article/column/article_detail.html", {"article":article})

