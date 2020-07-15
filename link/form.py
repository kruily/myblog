"""******************************** 开始
    author:惊修
    time:$
   ******************************* 结束"""

from django import forms
from .models import Link


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('avatar','name','url')