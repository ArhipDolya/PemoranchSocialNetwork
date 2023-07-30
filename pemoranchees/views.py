from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import PemoranSerializer, PemoranActionSerializer

from .models import Pemoran
from .forms import PemoranForm
import random


def my_is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pemoran_create_view(request):
    serializer = PemoranSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def pemoran_list_view(request):
    query = Pemoran.objects.all()
    serializer = PemoranSerializer(query, many=True)
    pemoranchees_list = [obj.serialize() for obj in query]

    return Response(serializer.data, status=200)

@api_view(['GET'])
def pemoran_details_view(request, pemoran_id):
    query = Pemoran.objects.filter(id=pemoran_id)
    if not query.exists:
        return Response({}, status=404)
    obj = query.first()
    serializer = PemoranSerializer(obj)

    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def pemoran_delete_view(request, pemoran_id):
    try:
        pemoran = Pemoran.objects.get(id=pemoran_id)
    except Pemoran.DoesNotExist:
        return Response({'message': 'Pemoran not found'}, status=status.HTTP_404_NOT_FOUND)
    
    pemoran.delete()
    return Response({'message': 'Pemoran deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pemoran_action_view(request):
    serializer = PemoranActionSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        pemoran_id = data.get('id') 
        action = data.get('action')

        query = Pemoran.objects.filter(id=pemoran_id)

        if not query.exists:
            return Response({"message": "Pemoran not found"}, status=404)
        
        obj = query.first()

        if action == 'like':
            obj.likes.add(request.user)
            serializer = PemoranSerializer(obj)
            return Response(serializer.data, status=200)    
        elif action == 'unlike':
            obj.likes.remove(request.user)
        elif action == 'repemo':
            pass

        return Response({}, status=200)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_protect
def pemoran_create_view_django(request):
    if request.method == 'POST':
        form = PemoranForm(request.post)
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



def pemoran_list_view_django(request):
    
    query = Pemoran.objects.all()
    pemoranchees_list = [obj.serialize() for obj in query]

    data = {
        'isUser': False,
        'responce': pemoranchees_list,
    }

    return JsonResponse(data)


def pemoran_details_view_django(request, pemoran_id):

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