from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import PemoranSerializer

from .models import Pemoran
from .forms import PemoranForm
import random


def my_is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pemoran_create_view(request):
    if request.method == 'POST':
        form = PemoranForm(request.POST, user=request.user)
        serializer = PemoranSerializer(data=request.data)

        if form.is_valid() and serializer.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

            if my_is_ajax(request):
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return render(request, 'homepage.html')

        if form.errors or serializer.errors:
            errors = {**form.errors, **serializer.errors}
            if my_is_ajax(request):
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        form = PemoranForm()

    return render(request, 'components/form.html', {'form': form})


@csrf_protect
def pemoran_create_view_django(request):
    if request.method == 'POST':
        form = PemoranForm(request.POST)
        user = request.user

        if not request.user.is_authenticated:
            user = None

            if my_is_ajax(request=request):
                return JsonResponse({}, status=401)
            
            return redirect(settings.LOGIN_URL)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.save()

            if my_is_ajax(request=request):
                return JsonResponse(obj.serialize(), status=201)

            return render(request, 'homepage.html')
        
        if form.errors:
            if my_is_ajax(request=request):
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