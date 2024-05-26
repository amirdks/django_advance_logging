from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from core.libs.logging import LogInfo


# Create your views here.
def rais_exception():
    raise Exception('Na')


class HomeView(View):
    def get(self, request: HttpRequest):
        try:
            rais_exception()
        except Exception as e:
            LogInfo.error(e, logger_name=__name__, extra={'phone': '09123456789'})
        return HttpResponse("salam")
