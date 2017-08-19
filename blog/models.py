from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
#数据库 分类表
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

#数据库 标签表
class Tag(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

#数据库 文章
class Post(models.Model):

    #标题
    title = models.CharField(max_length=70)
    #正文
    body = models.TextField()

    #创建时间 和 最后一次的修改时间
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    #文章摘要
    excerpt = models.CharField(max_length=300, blank=True)

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank= True)

    #关联作者
    author = models.ForeignKey(User)

    #记录阅读量
    readnums = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})

    #阅读量
    def increase_readnums(self):
        self.readnums += 1
        self.save(update_fields=['readnums'])

    #内部类 让post 自动排序
    #-created_time 前面的-表示按照逆序排列
    class Meta:
        ordering = ['-created_time']