"""******************************** 开始
    author:惊修
    time:$
   ******************************* 结束"""

from django import forms
from .models import Article

# 写文章的表单类
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'body','tags','avatar')
