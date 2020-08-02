from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.
from django.utils.timezone import now


class Link(models.Model):

    name = models.CharField(max_length=20)
    avatar = models.URLField()
    url = models.URLField()
    declaration = models.CharField(max_length=50)
    link_time = models.DateTimeField(default=now)

    class Meta:
        ordering = ('-link_time',)

    def __str__(self):
        return self.name

# 友链的留言
class LinkMessage(models.Model):
    name = models.CharField(max_length=20)
    avatar = models.URLField()
    url = models.URLField()
    declaration = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return "名称:%s\n网址:%s\n头像:%s\n宣言:%s\n" % (self.name,self.url,self.avatar,self.declaration)