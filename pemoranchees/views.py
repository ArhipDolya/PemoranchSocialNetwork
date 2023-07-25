from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse

from .models import Pemoran

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