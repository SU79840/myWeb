from ..models import Post, Category
from django import template
from django.db.models.aggregates import Count

register = template.Library()

@register.simple_tag
def get_recent_posts(num=8):
    #return Post.objects.all().order_by('-created_time')[:num]
    return Post.objects.all()[:num]

@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')

@register.simple_tag
def get_categories():
    # 别忘了在顶部引入 Category 类

    category_list = Category.objects.annotate(num_posts=Count('post'))
    return category_list
    #return Category.objects.all()

