# Modulo para realizar calculo de frete, nao implementada ainda, mas possivelmente usaremos alguma api
from ..models import *
import random




def calcula_frete_produto(user, produto):
    cep = user.endereco_set.first().cep
    return int(cep) % 10 + random.uniform(0, 1)



def calcula_frete_carrinho(cart):
    user = cart.comprador
    total = 0.0
    for produto in cart.produtos.all():
        # Chamada magica de api dos correios
        total += calcula_frete_produto(user, produto)
    return total




    
