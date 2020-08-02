from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Link
from .forms import LinkForm
from .models import LinkMessage
from notifications.signals import notify
from django.contrib.auth.models import User
# Create your views here.


def link(request):
        if request.method == 'POST':
                link_form = LinkForm(request.POST)
                # print(link_form)
                if link_form.is_valid():
                        link_message = link_form.save(commit=False)
                        link_message.save()
                        print(link_message)
                        if not request.user.is_superuser:
                                notify.send(
                                        request.user,
                                        recipient=User.objects.filter(is_superuser=1),
                                        verb='申请友链',
                                        action_object=link_message,
                                )
                return redirect('links:link')
        elif request.method == 'GET':
                links = Link.objects.all()
                context = {'links': links, 'message': '欢迎友友ヽ(￣ω￣(￣ω￣〃)ゝ'}
                return render(request, 'link/list.html', context=context)
        else:
                pass

