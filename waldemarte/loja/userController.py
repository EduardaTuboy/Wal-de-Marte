from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest


from .models import *

import json





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
        

def get_comprador(request : HttpRequest, id):
    try:
        user = Comprador.objects.get(pk=id)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()
    return HttpResponse(json.dumps(user.asdict), content_type="application/json")

def update_comprador(request : HttpRequest):
    args = json.loads(request.body)
    try:
        updated_user = Comprador.objects.get(pk=args["id"])
        for field, value in args["fields"].items():
            setattr(updated_user, field, value)
        updated_user.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest
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

def update_vendedor(request : HttpRequest):
    args = json.loads(request.body)
    try:
        updated_user = Vendedor.objects.get(pk=args["id"])
        for field, value in args["fields"].items():
            setattr(updated_user, field, value)
        updated_user.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest
    return HttpResponse()
    

def get_vendedor(request : HttpRequest, id):
    try:
        user = Vendedor.objects.get(pk=id)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()
    return HttpResponse(json.dumps(user.asdict), content_type="application/json")
