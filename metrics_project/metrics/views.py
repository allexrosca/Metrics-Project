from django.shortcuts import render

from django.http import HttpResponse

from django.template import loader
from metrics.models import *
from rest_framework.views import APIView
from django.views.generic import View
from rest_framework.response import Response
from django.http import JsonResponse



class DashboardHome(View):
    def get(self, request, *args, **kwargs):
        context=dict()
        return render(request, 'metrics/dashboard.html', context)


