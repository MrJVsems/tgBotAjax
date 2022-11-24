from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from ugc.models import Profile, Message
from django.core import serializers
import json


def index(request):
    users_cnt_messages = Message.objects.values('profile__name').annotate(
        qs_count=Count('text'),
    )
    list_of_message = []

    for i in list(users_cnt_messages):
        list_of_message.append([i['profile__name'], i['qs_count']])
    context = {
        'message': list_of_message,
    }
    return render(request, 'index.html', context)


def get(request, *args, **kwargs):
    users_cnt_messages = Message.objects.values('profile__name').annotate(
        qs_count=Count('text'),
    )

    if is_ajax(request):
        msg_json = json.dumps(list(users_cnt_messages))
        return JsonResponse(msg_json, safe=False)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'