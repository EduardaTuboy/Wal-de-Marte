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

def add_produto(request : HttpRequest):
    args = json.loads(request.body)
    try:
        owner = Vendedor.objects.get(pk=args["id"])
        produto = Produto(vendedor = owner, **args["produto"])
        produto.save()
        opcoes = [Opcao(opcao=op, produto=produto) for op in args["opcoes"]]
        for op in opcoes:
            op.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()
    return HttpResponse()


def query_produtos(request : HttpRequest):
    args = json.loads(request.body)
    produtos = []
    try:
        produtos = Produto.objects.filter(
            nome__icontains=args["query"], 
            preco__gte=args["preco_lim_inf"],
            preco__lte=args["preco_lim_sup"]                
            )
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()
    produtos_json = [p.to_json() for p in produtos]
    return HttpResponse(produtos_json, content_type="application/json")
    


def return_compradores(request):
    return HttpResponse([str(c) for c in Comprador.objects.all()])