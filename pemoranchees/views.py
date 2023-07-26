from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse

from .models import Pemoran
import random


def pemoran_list_view(request):
    query = Pemoran.objects.all()
    pemoranchees_list = [{'id': obj.id, 'content': obj.content, 'likes': random.randint(0, 100)} for obj in query]

    data = {
        'isUser': False,
        'responce': pemoranchees_list,
    }

    return JsonResponse(data)


def pemoran_details_view(request, pemoran_id):

    data = {
        'id': pemoran_id,
    }
    status = 200

    try:
        obj = Pemoran.objects.get(id=pemoran_id)
        data['content'] = obj.content
    except:
        status = 404
        data['message'] = 'Not found'

    return JsonResponse(data, status=status)