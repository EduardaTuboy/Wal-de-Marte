from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from .classes.frete import calcula_frete_carrinho, calcula_frete_produto

from .models import *

import json




def get_cart(request: HttpRequest):
    user = request.session.get("user", None)
    if user is None:
        return redirect("login")

    try:
        cart = CarrinhoDeCompras.objects.get(comprador_id=user["id"])
        produtos = cart.produtos.all()
    except CarrinhoDeCompras.DoesNotExist:
        produtos = []

    try:
        context = {
            "user": user,
            "produtos": produtos,
            "preco_final": cart.preco_final if produtos else 0,
            "frete": calcula_frete_carrinho(cart) if produtos else 0
        }
    except:
        context = {
            "user": user,
            "produtos": produtos,
            "preco_final": cart.preco_final if produtos else 0,
            "frete": "Registre endereco para ver frete"
        }
    return render(request, "carrinho.html", context)

def add_to_cart(request: HttpRequest):
    if request.method == "POST":
        try:
            # Verifica se o usuário está logado
            session_user = request.session.get("user", None)
            if session_user is None:
                return redirect("login")
            
            # Obtém o comprador logado
            user = Comprador.objects.get(pk=session_user["id"])
            
            # Obtém o produto pelo ID do formulário
            produto_id = request.POST.get("produto_id")
            produto = Produto.objects.get(pk=produto_id)
            
            # Tenta obter ou criar o carrinho do usuário
            cart, created = CarrinhoDeCompras.objects.get_or_create(comprador=user)
            
            # Adiciona o produto ao carrinho
            cart.produtos.add(produto)
            cart.preco_final += produto.preco
            cart.save()

            # Mensagem de sucesso
            # messages.success(request, f"Produto '{produto.nome}' foi adicionado ao carrinho!")
            return redirect("get_cart")  # Redireciona para a página do carrinho

        except Produto.DoesNotExist:
            return HttpResponseBadRequest("Produto não encontrado.")
        except Exception as e:
            print(e)
            return HttpResponseBadRequest("Erro ao adicionar produto ao carrinho.")
    else:
        return HttpResponseBadRequest("Método não permitido.")


def remove_from_cart(request: HttpRequest):
    if request.method == "POST":
        try:
            # Obtém o usuário logado
            session_user = request.session.get("user", None)
            if session_user is None:
                return redirect("login")
            
            # Obtém o comprador
            user = Comprador.objects.get(pk=session_user["id"])
            
            # Obtém o carrinho do comprador
            cart = CarrinhoDeCompras.objects.get(comprador=user)
            
            # Obtém o produto a ser removido
            produto_id = request.POST.get("produto_id")
            produto = Produto.objects.get(pk=produto_id)
            
            # Remove o produto do carrinho
            cart.produtos.remove(produto)
            cart.preco_final -= produto.preco
            cart.save()

            # messages.success(request, f"Produto '{produto.nome}' removido do carrinho.")
            return redirect("get_cart")  # Redireciona de volta para o carrinho

        except (Produto.DoesNotExist, CarrinhoDeCompras.DoesNotExist):
            return HttpResponseBadRequest("Produto ou carrinho não encontrado.")
        except Exception as e:
            print(e)
            return HttpResponseBadRequest("Erro ao remover produto do carrinho.")
    else:
        return HttpResponseBadRequest("Método não permitido.")
