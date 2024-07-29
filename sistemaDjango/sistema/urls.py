from django.contrib import admin
from django.urls import path
from loja import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    #Funcionarios
    path('funcionarios', views.listar_funcionarios, name='url_funcionarios'),
    path('novoFuncionario', views.new_funcionario, name='url_novoFuncionario'),
    path('updateFuncionario/<int:pk>/', views.update_funcionario, name='url_updateFuncionario'),
    path('deleteFuncionario/<int:pk>/', views.delete_funcionario, name='url_deleteFuncionario'),

    #Fabricantes
    path('fabricantes', views.listar_fabricantes, name='url_fabricantes'),
    path('novoFabricante', views.new_fabricante, name='url_novoFabricante'),
    path('updateFabricante/<int:pk>/', views.update_fabricante, name='url_updateFabricante'),
    path('deleteFabricante/<int:pk>/', views.delete_fabricante, name='url_deleteFabricante'),

    #Produtos
    path('produtos', views.listar_produtos, name='url_produtos'),
    path('novoProduto', views.new_produto, name='url_novoProduto'),
    path('updateProduto/<int:pk>/', views.update_produto, name='url_updateProduto'),
    path('deleteProduto/<int:pk>/', views.delete_produto, name='url_deleteProduto'),

    #Vendas
    path('vendas', views.listar_vendas, name='url_vendas'),
    path('novaVenda', views.new_venda, name='url_novaVenda'),
    path('updateVenda/<int:pk>/', views.update_venda, name='url_updateVenda'),
    path('deleteVenda/<int:pk>/', views.delete_venda, name='url_deleteVenda'),

    #Graficos
    path('plotly', views.charts, name='url_graficos')
]
