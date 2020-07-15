"""******************************** 开始
    author:惊修
    time:$
   ******************************* 结束"""

from django.urls import path
from .views import *

app_name = 'body'

urlpatterns = [
    path('index/', index, name='index'),
    path('list/', list, name='list'),
    path('read/<int:id>/', read, name='read'),
    path('create/', createArticle, name='create'),
    path('delete/<int:id>',delete, name='delete'),
    path('update/<int:id>', update, name='update'),
]