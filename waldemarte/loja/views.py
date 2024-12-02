from django.shortcuts import render
from django.http import HttpResponse


from .models import Comprador


# Create your views here. -> interacao que o usuario tem no frontend vem pra ca

# TODO : index
def index(request):
    pass

# TODO : implementar de forma mais elegante, talvez de com json
def save_comprador(request, nome, email, telefone, cpf, senha):
    user = Comprador(nome=nome, email=email, telefone=telefone, cpf=cpf, senha=senha)
    user.save()
    return HttpResponse("Sucess")


def return_compradores(request):
    return HttpResponse([str(c) for c in Comprador.objects.all()])