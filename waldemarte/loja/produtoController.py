from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest


from .models import *

import json





def add_produto(request : HttpRequest):
    args = json.loads(request.body)
    try:
        owner = Vendedor.objects.get(pk=args["id"])
        produto = Produto(vendedor = owner, **args["produto"])
        produto.save()
        opcoes = [Opcao(opcao=op, produto=produto) for op in args["opcoes"]]
        imagens = [ImagemProduto(img_url=i, produto=produto) for i in args["imagens"]]
        for op in opcoes:
            op.save()
        for i in imagens:
            i.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()
    return HttpResponse()

def delete_produto(request, p_id):
    Produto.objects.get(pk=p_id).delete()
    return HttpResponse()

def get_produto(request: HttpRequest, id):
    try:
        prod = Produto.objects.get(pk=id)
        if request.headers.get("Content-Type") == "application/json":
            # Retorna o produto como JSON se for chamado via API
            return HttpResponse(json.dumps(prod.asdict()), content_type="application/json")

        # Se não for JSON, renderiza um template HTML
        user = request.session.get("user", None)
        if user is not None:
            user = Comprador.objects.get(pk=user["id"])
            try:
                return render(request, "produto.html", {"produto": prod, "frete": calcula_frete_produto(user, prod)})
            except Exception as inner_e:
                return render(request, "produto.html", {"produto": prod, "frete": "Cadastre endereço para ver seu frete."})
        return render(request, "produto.html", {"produto": prod, "frete": "Login para ver seu frete."})

    except Exception as e:
        # Substitua  por apenas imprimir ou lidar com a exceção
        print(e)  # Você pode registrar o erro no console
        return HttpResponseBadRequest("Erro ao buscar produto")



def update_produto(request : HttpRequest):
    args = json.loads(request.body)
    try:
        updated_produto = Produto.objects.get(pk=args["id"])
        for field, value in args["fields"].items():
            if field != "opcoes":
                setattr(updated_produto, field, value)
        for op in args["fields"]["opcoes"]:
            updated_produto.opcao_set.add(Opcao(opcao=op))
        updated_produto.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest
    return HttpResponse()
    



def query_produtos(request: HttpRequest):
    args = json.loads(request.body) if request.method == "POST" else {}
    produtos = []
    try:
        # Se argumentos existirem, faz a busca
        produtos = Produto.objects.filter(
            nome__icontains=args.get("query", ""), 
            preco__gte=args.get("preco_lim_inf", 0),
            preco__lte=args.get("preco_lim_sup", 999999)
        )
    except Exception as e:
        print(e)
        if request.method == "POST":
            return HttpResponseBadRequest("Invalid input")
    if request.method == "POST":
        produtos_json = [p.to_json() for p in produtos]
        return HttpResponse(json.dumps(produtos_json), content_type="application/json")
    return produtos  # Retorna os objetos diretamente se chamado internamente

