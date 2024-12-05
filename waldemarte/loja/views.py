from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
import json

from .models import Comprador


# Create your views here. -> interacao que o usuario tem no frontend vem pra ca

# TODO : index
def index(request):
    pass


def criar_comprador(request : HttpRequest):
    args = json.loads(request.body) 
    try:
        user = Comprador(**args)
    except Exception as e:
        return HttpResponseBadRequest("Incorrect json formatting")
    user.save()
    return HttpResponse("Sucess")

 



def return_compradores(request):
    return HttpResponse([str(c) for c in Comprador.objects.all()])