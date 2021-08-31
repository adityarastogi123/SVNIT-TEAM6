from django.shortcuts import render
import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
from .serializers import HistorySerializer
from .models import History

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file=open(os.path.join(BASE_DIR,'Stock List.json'),'r')
res=file.read() 
res=json.loads(res)
# Create your views here.
@api_view(['GET'])
def dateFilter(request):
    data=request.data
    if ('from' not in data) or ('to' not in data) or ('symbol' not in data):
        return Response({
            'status':'error',
            'message':'MISSING ONE OR MORE FIELDS'
        })
    # print("2021-01-14">"2021-01-15")
    info=[]
    for i in res:
        if data['from']!='null' and data['to']!='null':
            if i['date']>=data['from'] and i['date']<=data['to']:
                if data['symbol']!='null':
                    if i['symbol']==data['symbol']:
                        info.append(i)
                else:
                    info.append(i)
        else:
            if data['symbol']!='null':
                if i['symbol']==data['symbol']:
                    info.append(i)
            else:
                info.append(i)
            
    return Response({
            'status':'success',
            'data':info
        })

@api_view(['GET'])
def getHistory(request):
    hist=History.objects.all()
    serializer=HistorySerializer(hist,many=True)
    # print(hist)
    return Response({
        'status':'success',
        'info':serializer.data
    })

@api_view(["POST"])
def addHistory(request):
    serializer=HistorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status':'success',
            'message':serializer.data
        })
    return Response({
        'status':'error',
        'message':serializer.errors
    })