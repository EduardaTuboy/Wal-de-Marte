from django.urls import path

from . import views

urlpatterns = [
    # TODO: index
    path("", views.index),

    # Salva um comprador na base de dados
    # Body do request em json -> 
    # {
    #   "nome" : <nome>,
    #   "email" : <email>,
    #   "telefone" : <telefone>,
    #   "cpf" : <cpf>,
    #   "senha" : <senha>
    #}
    path("comprador/salvar", views.criar_comprador),

    # Retorna compradores em uma string, apenas para debug
    path("comprador/all", views.return_compradores)
]