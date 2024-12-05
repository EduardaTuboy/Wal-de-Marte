from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
import json

from .models import *


# Create your views here. -> interacao que o usuario tem no frontend vem pra ca

# TODO : index
def index(request):
    pass

# TODO : verificacao mais robusta nas funcoes de criacao
def criar_comprador(request : HttpRequest):
    args = json.loads(request.body) 
    try:
        user = Comprador(**args)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest("Incorrect json formatting")
    user.save()
    return HttpResponse()

def comprador_set_endereco(request : HttpRequest):
    args = json.loads(request.body)
    try:
        addr = Endereco(comprador = Comprador.objects.get(id=args["id"]),**args["endereco"])
        addr.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest("Incorrect json formatting")
    return HttpResponse()

def comprador_add_cartao(request : HttpRequest):
    args = json.loads(request.body)
    try:
        cartao = Cartao(comprador = Comprador.objects.get(id=args["id"]), **args["cartao"])
        cartao.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest("Incorrect json formatting")
    return HttpResponse()
        

def criar_vendedor(request : HttpRequest):
    args = json.loads(request.body)
    try:
        user = Vendedor(**args)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest("Incorrect json formatting")
    user.save()
    return HttpResponse()


def return_compradores(request):
    return HttpResponse([str(c) for c in Comprador.objects.all()])