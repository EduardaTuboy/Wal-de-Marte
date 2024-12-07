# Modulo para realizar calculo de frete, nao implementada ainda, mas possivelmente usaremos alguma api
from ..models import *






def calcula_frete(cart ):
    user_cep = cart.comprador.endereco_set.all()[0].cep
    total = 0.0
    for produto in cart.produtos.all():
        # Chamada magica de api dos correios
        total += 5.0
    return total




    
