from django.urls import path

from . import views

urlpatterns = [
    # TODO: index
    path("", views.index),
    path("comprador/salvar/<nome>/<email>/<telefone>/<cpf>/<senha>", views.save_comprador),
    path("comprador/all", views.return_compradores)
]