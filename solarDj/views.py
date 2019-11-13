from django.shortcuts import render
# Create your views here.
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json
import os
#from solarDj.cylrealtimepy.ucd_demo import make_datalog_query

# Create your views here.
@api_view(["GET"])
def yearly87(request):
        setroot = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(setroot, r'solarDj/YearlyResult87.json'), 'r') as myfile:
                data1 = myfile.read()
                data = json.loads(data1)
        return JsonResponse(data,safe=False)
def dailymonth87(request):
        setroot = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(setroot, r'solarDj/DailyMonthResult87.json'), 'r') as myfile:
                data1 = myfile.read()
                data = json.loads(data1)
        return JsonResponse(data,safe=False)

def yearly790(request):
        setroot = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(setroot, r'solarDj/YearlyResult790.json'), 'r') as myfile:
                data1 = myfile.read()
                data = json.loads(data1)
        return JsonResponse(data,safe=False)

def dailymonth790(request):
        setroot = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(setroot, r'solarDj/DailyMonthResult790.json'), 'r') as myfile:
                data1 = myfile.read()
                data = json.loads(data1)
        return JsonResponse(data,safe=False)
    #except ValueError as e:
     #   return Response(e.args[0],status.HTTP_400_BAD_REQUEST)
