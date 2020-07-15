from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from ckeditor.fields import RichTextField
import os

# Create your models here.

# 分类的模型
class ArticleColumn(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=now)

    def __str__(self):
        return self.title


# 博客文章数据模型
class Article(models.Model):
    # 文章作者。参数 on_delete 用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)

    # 文章分类
    column = models.ForeignKey(ArticleColumn,null=True,blank=True,on_delete=models.CASCADE,related_name='article')

    # 文章标签
    tags = TaggableManager(blank=True)

    # 文章正文。保存大量文本使用 TextField
    body = RichTextField()

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)
    views_total = models.PositiveIntegerField(default=0)

    avatar = models.ImageField(upload_to='article/%Y/%m/%d/',blank=True)

    #保存时处理图片
    def save(self, *args,**kwargs):
        article = super(Article,self).save(*args,**kwargs)
        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_file'):
            image = Image.open((self.avatar))
            (x,y) = image.size
            new_x = 300
            new_y = 250
            resized_image = image.resize((new_x,new_y),Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
            image.close()
        return article




    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('body:read', args=[self.id])


#删除文件
@receiver(pre_delete, sender=Article)
def Article_delete(instance, **kwargs):
    instance.avatar.delete()

