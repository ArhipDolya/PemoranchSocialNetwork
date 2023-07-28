from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_protect

from .models import Pemoran
from .forms import PemoranForm
import random


@csrf_protect
def pemoran_create_view(request):
    if request.method == 'POST':
        form = PemoranForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            if request.is_ajax():
                return JsonResponse(obj.serialize(), status=201)

            return render(request, 'homepage.html')
        
        if form.errors:
            if request.is_ajax():
                return JsonResponse(form.errors, status=400)

    else:
        form = PemoranForm()

    return render(request, 'components/form.html', {'form': form})

def pemoran_list_view(request):
    
    query = Pemoran.objects.all()
    pemoranchees_list = [obj.serialize() for obj in query]

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