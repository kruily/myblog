from django.db import models
from PIL import Image
# Create your models here.
from django.utils.timezone import now


class Link(models.Model):

    name = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='link/')
    url = models.URLField()
    link_time = models.DateTimeField(default=now)

    # 保存图片时处理
    def save(self,*args,**kwargs):
        link = super(Link, self).save(*args,**kwargs)
        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_file'):
            image = Image.open((self.avatar))
            new_x = 64
            new_y = 64
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return link
    class Meta:
        ordering = ('-link_time',)

    def __str__(self):
        return self.name