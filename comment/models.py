from django.db import models
from django.contrib.auth.models import User
from body.models import Article
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel,TreeForeignKey
# Create your models here.

# 文章的评论
class Comment(MPTTModel):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return self.body[:20]

    def save(self,*args,**kwargs):
       Comment.objects.rebuild()
       return super(Comment,self).save(*args,**kwargs)
