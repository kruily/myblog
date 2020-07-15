from PIL import Image
from django.db import models
from django.contrib.auth.models import User
# # 引入内置信号
# from django.db.models.signals import post_save
# # 引入信号接收器的装饰器
# from django.dispatch import receiver
# # Create your models here.

# 用户扩展信息
class Profile (models.Model):
    # 与User模型构成1对1的党关系
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='profile')
    # 电话号码字段
    phone = models.CharField(max_length=20,blank=True)
    # 头像
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    # 个人简介
    slogan = models.TextField(max_length=500, blank=True)

    # 保存图片时处理
    def save(self, *args, **kwargs):
        profile = super(Profile, self).save(*args, **kwargs)
        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_file'):
            image = Image.open((self.avatar))
            new_x = 64
            new_y = 64
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return profile

    def __str__(self):
        return 'user {}'.format(self.user.username)



# # 信号接受函数,每当新建User实例是自动调用
# @receiver(post_save, sender=User)
# def createUserProfile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
# # 信号接受函数,每当更新User实例是自动调用
# @receiver(post_save, sender=User)
# def saveUserProfile(sender, instance, **kwargs):
#     # instance.profile.save()
#     pass