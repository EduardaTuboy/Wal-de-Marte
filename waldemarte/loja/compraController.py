from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from .classes.frete import calcula_frete_carrinho, calcula_frete_produto
import loja.classes.notificacoes as notif
from .models import *

import json




def compra_carrinho(request: HttpRequest):
    if request.method == "POST":
        try:
            # Verifica se o usuário está logado
            session_user = request.session.get("user", None)
            if session_user is None:
                return redirect("login")
            
            # Obtém os IDs dos produtos do formulário
            produtos_ids = request.POST.getlist("produtos_ids")
            produtos = Produto.objects.filter(pk__in=produtos_ids)

            # Verifica se os produtos existem
            if not produtos.exists():
                return HttpResponseBadRequest("Produtos não encontrados.")

            # Calcula o total dos produtos
            total = sum(produto.preco for produto in produtos)

            # Renderiza a página de compra com os produtos e o total
            return render(request, "compra.html", {"produtos": produtos, "total": total})

        except Exception as e:
            print(e)
            return HttpResponseBadRequest("Erro ao processar a compra.")
    else:
        return redirect("index")


def comprar_produto(request: HttpRequest, produto_id):
    try:
        produto = Produto.objects.get(pk=produto_id)
        session_user = request.session.get("user", None)
        if session_user is None:
            return redirect("login")
        
        # Passa o produto para a página de compra
        total = produto.preco
        return render(request, "compra.html", {"produtos": [produto], "total": total})


    except Produto.DoesNotExist:
        return HttpResponseBadRequest("Produto não encontrado.")
    except Exception as e:
        print(e)
        return HttpResponseBadRequest("Erro ao acessar página de compra.")

def realizar_compra(request: HttpRequest):
    if request.method == "POST":
        try:
            # Verifica se o usuário está logado
            session_user = request.session.get("user", None)
            if session_user is None:
                return redirect("login")

            # Obtém os IDs dos produtos do formulário
            produtos_ids = request.POST.getlist("produtos_ids")  # Lista de IDs enviada
            
            # Log para depuração
            print("Produtos enviados (lista):", produtos_ids)

            # Verifica se a lista de IDs está vazia
            if not produtos_ids:
                return HttpResponseBadRequest("Nenhum produto foi selecionado para compra.")

            # Filtra os produtos com base nos IDs
            produtos = Produto.objects.filter(pk__in=produtos_ids)
            
            # Verifica se os produtos foram encontrados
            if not produtos.exists():
                return HttpResponseBadRequest("Nenhum produto correspondente encontrado no banco de dados.")

            # Obtém o comprador
            user = Comprador.objects.get(pk=session_user["id"])

            # Registra transações para cada produto
            for produto in produtos:
                print(f"Processando produto: {produto.nome} (ID: {produto.id})")
                try:
                    transacao = Transacao.registrar_produto(user, produto)
                    print("Transação registrada com sucesso.")
                except Exception as e:
                    print(f"Erro ao registrar transação para o produto {produto.id}: {e}")
                    raise e
                try:
                    notif.notificarCompraComprador(transacao)
                    notif.notificarCompraVendedor(transacao)
                    print("Notificações enviadas com sucesso.")
                except Exception as e:
                    print(f"Erro ao enviar notificações para o produto {produto.id}: {e}")
                    raise e

            # Redireciona para a página de venda concluída
            return redirect("vendaConcluida")

        except Comprador.DoesNotExist:
            return redirect("login")
        except Exception as e:
            print("Erro durante a compra:", e)
            return HttpResponseBadRequest("Erro ao realizar a compra.")
    else:
        return redirect("index")
