from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Article, ArticleColumn,Article_delete
import markdown
from .form import ArticleForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from comment.models import Comment
from comment.forms import CommentForm

# Create your views here.


def index(request):
    return render(request, 'body/index.html', context=None)


def list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    # 初始化查询集
    article_list = Article.objects.all()
    # 用户搜索逻辑
    if search:
        if order == 'views_total':
            # 用Q对象进联合搜索
            article_list = Article.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
        else:
            article_list = Article.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        search = ''
        if order == 'views_total':
            article_list = Article.objects.all().order_by('-views_total')
        else:
            article_list = Article.objects.all()

    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {'articles': articles,
               'order': order,
               'search': search,
               'column': column,
               'tag': tag}
    return render(request, 'body/list.html', context=context)


def read(request, id):
    article = Article.objects.get(id=id)
    article.views_total += 1
    article.save(update_fields=['views_total'])
    # 取出文章评论
    comments = Comment.objects.filter(article=id)
    # 修改 Markdown 语法渲染
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)
    comment_form = CommentForm()
    context = {'article': article,
               'toc': md.toc,
               'comments': comments,
               'comment_form':comment_form,
               }
    return render(request, 'body/read.html', context=context)


# 写文章的视图
@login_required(login_url='/userprofile/login')
def createArticle(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_form = ArticleForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_form.is_valid():
            # 保存数据,但暂时不提交到数据库中
            new_article = article_form.save(commit=False)
            # 指定数据库中作者为id = 1
            # 如果你进行过阐述数据表的操作,可能会找不到id=1的用户
            # 此时请重新创建用户,并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)
            # 将新文章保存到数据库中
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            new_article.save()
            article_form.save_m2m()
            # 完成后返回到文章列表
            return redirect('body:list')
        # 如果数据不合法,返回错误信息
        else:
            return HttpResponse("表单内容有误,请重新填写")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_form = ArticleForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = {'article_form': article_form, 'columns': columns}
        # 返回模板
        return render(request, 'body/create.html', context)


# 删文章
def delete(request, id):
    if request.method == 'POST':
        article = Article.objects.get(id=id)
        article.delete()
        return redirect("body:list")
    else:
        return HttpResponse("仅允许post请求")


# 修改文章
@login_required(login_url='/userprofile/login')
def update(request, id):
    """
           更新文章的视图函数
           通过POST方法提交表单，更新titile、body字段
           GET方法进入初始表单页面
           id： 文章的 id
    """
    # 获取到需要修改的文章
    article = Article.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse('抱歉,你无权修改别人的文章')
    # 判断用户是否是post提交表单数据
    if request.method == 'POST':
        # 将提交的数据赋值到表达实例中
        article_form = ArticleForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')
            article.tags.set(*request.POST.get('tags').split(','), clear=True)
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            article.save()
            # 完成后返回到修改后的文章中,需传入文章的id
            return redirect('body:read', id=id)
        # 如果数据不合法,返回错误信息
        else:
            return HttpResponse('表单内容有误,请重新填写')
    # 如果用户get请求
    else:
        # 创建表单实例
        article_form = ArticleForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文,将article文章对象也传递过去,以便提取旧的文章
        context = {'article': article,
                   'article_form': article_form,
                   'columns': columns,
                   'tags': ','.join([x for x in article.tags.names()]),
                   }
        return render(request, 'body/update.html', context=context)
