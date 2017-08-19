from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm

def post_comment(request, post_pk):
    post= get_object_or_404(Post, pk=post_pk)

    #http 提交请求有两种方法 post和get 如果是post提交才接收处理
    if request.method == 'POST':
        #用户提交的数据在POST中 是一个字典对象
        form = CommentForm(request.POST)
        #数据是否合法
        if form.is_valid():
            #commit=False 只生成实例 数据还不保存到数据库
            comment= form.save(commit=False)
            #关联评论与文章
            comment.post = post
            #保存
            comment.save()

            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，
            # 它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(post)
        #不合法
        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 因此我们传了三个模板变量给 detail.html，
            # 一个是文章（Post），一个是评论列表，一个是表单 form
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            # 具体请看下面的讲解。
            comment_list = post.comment_set.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'blog/detail.html', context=context)
    #不是post请求
    return redirect(post)
