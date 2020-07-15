"""******************************** 开始
    author:惊修
    time:$
   ******************************* 结束"""

from django.urls import path
from .views import *

app_name = 'notice'

urlpatterns = [
    # 通知列表
    path('list/', CommentNoticeListView.as_view(),name='list'),
    path('update/', CommentNoticeUpdateView.as_view(), name='update'),
]