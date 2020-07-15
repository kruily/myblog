"""******************************** 开始
    author:惊修
    time:$
   ******************************* 结束"""
from django.urls import path
from .views import *
app_name = 'comment'

urlpatterns = [
    path('post_comment/<int:article_id>/', post_comment, name='post_comment'),
    path('post-comment/<int:article_id>/<int:parent_comment_id>', post_comment, name='comment_reply'),
    
]