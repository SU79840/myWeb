from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Post, Category
from comment.forms import CommentForm
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
#分页效果
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import markdown

def index(request):
    post_list = Post.objects.all()
    #return render(request, 'blogApp/index.html', context={
    #                           'title': '首页',
    #                           'welcome': '欢迎'
    #                })

    #分页效果
    pageiantor = Paginator(post_list, 6)
    page = request.GET.get('page')

    try:
        post_list = pageiantor.page(page)
    except PageNotAnInteger:
        post_list = pageiantor.page(1)
    except EmptyPage:
        post_list = pageiantor.page(pageiantor.num_pages)

    return render(request, 'blog/index.html', context={'post_list': post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    #post.body = markdown.markdown(post.body,
    #                              extensions =[
    #                                 'markdown.extensions.extra',
    #                                 'markdown.extensions.codehilite',
    #                                 'markdown.extensions.toc',
    #                              ])


    #更新阅读量
    post.increase_readnums()
    md = markdown.Markdown(extensions =[
                            'markdown.extensions.extra',
                            'markdown.extensions.codehilite',
                            #代替'markdown.extensions.toc',
                            #优化点击目录后的url的样式
                            TocExtension(slugify=slugify),
                        ])
    #更新评论
    post.body = md.convert(post.body)
    form = CommentForm()

    comment_list = post.comment_set.all()
    context = {'post': post,
               'toc': md.toc,
                    'form': form,
                    'comment_list': comment_list
                    }

    return render(request,'blog/detail.html', context=context)

#按月归档
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


#按类型
def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

#search
def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键字'
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(title__icontains=q)
    return render(request, 'blog/index.html', {'error_msg':error_msg,
                                               'post_list':post_list})