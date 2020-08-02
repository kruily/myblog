"""******************************** 开始
    author:惊修
    time:$
   ******************************* 结束"""
from django import forms
from link.models import LinkMessage
class LinkForm(forms.ModelForm):
    class Meta:
        model = LinkMessage
        fields = ('name','avatar','url','declaration')