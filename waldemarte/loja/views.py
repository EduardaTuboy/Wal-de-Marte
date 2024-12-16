from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from .classes.frete import calcula_frete_produto, calcula_frete_carrinho
from .classes.db_init import initDefaultDB
from django.contrib import messages
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from django.http import JsonResponse
import json

import loja.classes.notificacoes as notif
from .produtoController import query_produtos
from .models import *


# Create your views here. -> interacao que o usuario tem no frontend vem pra ca


# Documentacao dos inputs e outputs das funcoes estao no urls.py


# TODO : index,
#        fazer autenticaçao de senha

def index(request : HttpRequest):
    if not Produto.objects.exists():
        initDefaultDB()
    query = request.GET.get("query", "")  # Obtém o termo de busca
    produtos = Produto.objects.all()  # Produtos padrão
    user = request.session.get("user", None)     # Se houver uma busca, filtra os produtos
    if query:
        produtos = produtos.filter(nome__icontains=query)

    context = {
        "produtos": produtos,
        "user" : user, # se autenticado eh o user, senao eh none,
        "query": query  # Passa o termo de busca para reutilizar no template
    }
    return render(request, "index.html", context)
    

def login(request : HttpRequest):
    if request.method == "POST":
        email = request.POST["email"]
        senha = request.POST["senha"]
         
        try:
            user = Comprador.authenticate(email, senha)
        except Comprador.DoesNotExist:
            # messages.error(request, "Login invalido")
            return render(request, "login.html")

        if user is not None:
            #login(request, user)
            context = {
                "user" : user.id
            }
            request.session["user"] = model_to_dict(user)
            return redirect("index")
        else:
            # messages.error(request, "Login invalido")
            return render(request, "login.html")
    # se a requisiçao for GET, retorna a pagina de login
    messages.error(request, "")
    return render(request, "login.html")


def register(request):
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        if password != confirm_password:
            # messages.error(request, "As senhas não coincidem.")
            return render(request, "register.html")
        try:
            c = Comprador(
                nome=request.POST.get("username"),
                email=email,
                senha=password
            )
            c.save()
            Endereco.default(c).save()
            request.session["user"] = model_to_dict(c)
            return redirect("index")
        except Exception as e:
            print(e)
    # messages.error(request, "")
    return render(request, "register.html")



def perfil(request : HttpRequest):
    user = request.session.get("user", None)
    
    if user is None:
        return redirect("login")
    
    request.session["user"] = None
    return redirect("index")


def carrinho(request : HttpRequest):
    user = request.session.get("user", None)
    if user is None:
        return redirect("login")
    return render(request, "carrinho.html", {"user" : user})


def compra(request : HttpRequest):
    user = request.session.get("user", None)
    if user is None:
        return redirect("login")
    return render(request, "compra.html", {"user" : user})

def vendaConcluida(request : HttpRequest):
    user = request.session.get("user", None)
    if user is None:
        return redirect("login")
    return render(request, "vendaConcluida.html", {"user" : user})




def return_compradores(request):
    return HttpResponse([str(c) for c in Comprador.objects.all()])

