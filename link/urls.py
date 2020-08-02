"""******************************** 开始
    author:惊修
    time:$
   ******************************* 结束"""

from django.urls import path
from .views import *

app_name = 'link'

urlpatterns = [
    path('', link, name='link'),
]