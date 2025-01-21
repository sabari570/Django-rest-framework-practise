from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.


@api_view(['GET'])
def api_home(request, *args, **kwargs):
    '''
    DRF API View
    '''
    return Response({'message': 'This is the api home route'})
