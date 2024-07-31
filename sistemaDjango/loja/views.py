
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum, F
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from .models import Funcionario, Fabricante, Produto, Venda, ProdutoVenda
from .form import FuncionarioForm, FabricanteForm, ProdutoForm, ProdutoVendaForm, VendaForm
import plotly.express as px
import pandas as pd


def home(request):
    #Renderiza tela de menu
    return render(request, 'loja/home.html')


# Funcionarios
def listar_funcionarios(request):
    data = {}
    #Requisisão ao banco de dados
    data['funcionarios'] = Funcionario.objects.all()
    #Renderiza template
    return render(request, 'loja/funcionarios/funcionarios.html', data)


def new_funcionario(request):
    form = FuncionarioForm(request.POST or None)

    #Se for válido
    if form.is_valid():
        #Salva funcionario
        form.save()
        #Redireciona a listagem de funcionarios
        return redirect('url_funcionarios')
    #Passando form para o template pelo contexto
    context = {
        'form': form
    }
    #Renderiza template
    return render(request, 'loja/funcionarios/newFuncionario.html', context)


def update_funcionario(request, pk):
    #Requisita funcionario do banco de dados pelo id
    funcionario = Funcionario.objects.get(pk=pk)
    #Instancia formulario com os dados preenchidos do funcionario
    form = FuncionarioForm(request.POST or None, instance=funcionario)

    # Se for válido
    if form.is_valid():
        # Salva funcionario
        form.save()
        #Redireciona a listagem de funcionarios
        return redirect('url_funcionarios')

    #Passando form para o template pelo contexto
    context = {
        'form': form,
        'funcionario': funcionario
    }
    #Renderiza template
    return render(request, 'loja/funcionarios/newFuncionario.html', context)


def delete_funcionario(request, pk):
    #Requisita funcionario do banco de dados pelo id
    funcionario = Funcionario.objects.get(pk=pk)
    #Deleta funcionario
    funcionario.delete()
    # Redireciona a listagem de funcionarios
    return redirect('url_funcionarios')


#Fabricantes
def listar_fabricantes(request):
    data = {}
    data['fabricantes'] = Fabricante.objects.all()
    return render(request, 'loja/fabricantes/fabricantes.html', data)


def new_fabricante(request):
    form = FabricanteForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('url_fabricantes')

    context = {
        'form': form
    }
    return render(request, 'loja/fabricantes/newFabricante.html', context)


def update_fabricante(request, pk):
    fabricante = Fabricante.objects.get(pk=pk)
    form = FabricanteForm(request.POST or None, instance=fabricante)

    if form.is_valid():
        form.save()
        return redirect('url_fabricantes')

    context = {
        'form': form,
        'fabricante': fabricante
    }
    return render(request, 'loja/fabricantes/newFabricante.html', context)


def delete_fabricante(request, pk):
    fabricante = Fabricante.objects.get(pk=pk)
    fabricante.delete()
    return redirect('url_fabricantes')


#Produtos
def listar_produtos(request):
    data = {}
    data['produtos'] = Produto.objects.all()
    return render(request, 'loja/produtos/produtos.html', data)


def new_produto(request):
    form = ProdutoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('url_produtos')

    context = {
        'form': form
    }
    return render(request, 'loja/produtos/newProduto.html', context)


def update_produto(request, pk):
    data = {}
    produto = Produto.objects.get(pk=pk)
    form = ProdutoForm(request.POST or None, instance=produto)

    if form.is_valid():
        form.save()
        return redirect('url_produtos')

    context = {
        'form': form,
        'produto': produto
    }
    return render(request, 'loja/produtos/newProduto.html', context)


def delete_produto(request, pk):
    produto = Produto.objects.get(pk=pk)
    produto.delete()
    return redirect('url_produtos')


#Vendas
def listar_vendas(request):
    vendas = Venda.objects.all().prefetch_related('produtos_vendidos__produto')
    return render(request, 'loja/vendas/vendas.html', {'vendas': vendas})


def new_venda(request):
    #Inicializando formulario
    if request.method == 'GET':
        #formulario de venda
        form = VendaForm()
        form.fields['data'].initial = timezone.now().date() #Setando data de hoje
        form.fields['data'].widget.attrs['readonly'] = True #Editable = False

        #criando formset de produtos da venda
        form_produto_factory = inlineformset_factory(Venda, ProdutoVenda, form=ProdutoVendaForm, extra=1)
        form_produtoVenda = form_produto_factory()

        #contexto
        context = {
            'form': form,
            'form_produtos': form_produtoVenda
        }
        #renderiza a pagina
        return render(request, 'loja/vendas/newVenda.html', context)

    elif request.method == 'POST': #Se clicar no botão de salvar
        form = VendaForm(request.POST)
        form_produto_factory = inlineformset_factory(Venda, ProdutoVenda, form=ProdutoVendaForm)
        form_produtoVenda = form_produto_factory(request.POST)

        #valida os formularios
        if form.is_valid() and form_produtoVenda.is_valid():
            valorVenda = 0

            #Atualizando Quantidade vendida de produtos - Calcula valor da venda
            for produto_venda in form_produtoVenda.cleaned_data:
                produto = produto_venda['produto']
                quantidade = produto_venda['quantidade']
                produto.qtd_vendida += quantidade
                valorVenda += produto.preco_venda*quantidade #Incrementando valor total da venda
                produto.save()

            #Atribuindo valor total da venda
            venda = form.save(commit=False)
            venda.valorVenda = valorVenda

            #INSERT
            venda.save()
            form_produtoVenda.instance = venda
            form_produtoVenda.save()

            #retorna a tela da tabela
            return redirect('url_vendas')
        else:
            #se não for válido rendezina novamente a página e mostra os campos inconsistentes
            context = {
                'form': form,
                'form_produtos': form_produtoVenda
            }
        return render(request, 'loja/vendas/newVenda.html', context)


def update_venda(request, pk):
    venda = Venda.objects.get(pk=pk)
    form_produto_factory = inlineformset_factory(Venda, ProdutoVenda, form=ProdutoVendaForm, extra=1, can_delete=True)

    if request.method == 'GET':
        form = VendaForm(instance=venda)
        form.fields['data'].widget.attrs['readonly'] = True #Editable = False

        form_produto_venda = form_produto_factory(instance=venda)
        context = {
            'form': form,
            'form_produtos': form_produto_venda,
            'venda': venda
        }
        return render(request, 'loja/vendas/newVenda.html', context)

    elif request.method == 'POST':
        form = VendaForm(request.POST, instance=venda)
        form_produto_venda = form_produto_factory(request.POST, instance=venda)

        if form.is_valid() and form_produto_venda.is_valid():
            with transaction.atomic():
                # Guardando as quantidades antigas
                quantidades_antigas = {pv.produto_id: pv.quantidade for pv in venda.produtos_vendidos.all()}
                valorVenda = venda.valorVenda

                # Calcula valor da venda - Incrementa quantidade vendida dos produtos
                for pv in form_produto_venda.save(commit=False):
                    produto = pv.produto
                    valorVenda += (pv.quantidade - quantidades_antigas.get(produto.id, 0)) * produto.preco_venda
                    produto.qtd_vendida += pv.quantidade - quantidades_antigas.get(produto.id, 0)
                    produto.save()

                # Decrementa quantidade vendida dos produtos
                for pv in form_produto_venda.deleted_objects:
                    produto = pv.produto
                    produto.qtd_vendida -= pv.quantidade
                    produto.save()

                    valorVenda -= (pv.quantidade * produto.preco_venda)

                venda.valorVenda = valorVenda
                venda.save()
                form_produto_venda.instance = venda
                form_produto_venda.save()

            return redirect('url_vendas')

        else:
            context = {
                'form': form,
                'form_produtos': form_produto_venda,
                'venda': venda
            }
        return render(request, 'loja/vendas/newVenda.html', context)


def delete_venda(request, pk):
    venda = Venda.objects.get(pk=pk)
    #Atualizando quantidade vendida dos produtos da venda
    for produto_venda in venda.produtos_vendidos.all():
        produto_venda.produto.qtd_vendida -= produto_venda.quantidade
        produto_venda.produto.save()

    venda.delete()
    return redirect('url_vendas')


#Grafico
def create_dataset_qtd_produtos():
    # Requisitando dados dos produtos do banco de dados
    data_queryset = ProdutoVenda.objects.values(
        'produto__nome'
    ).annotate(
        quantidade_vendida=Sum('quantidade')
    )
    # Montando o dataset
    dataset = [{'produto': item['produto__nome'], 'quantidade_vendida': item['quantidade_vendida']} for item in data_queryset]

    return dataset


def chart_pie_produtos():
    # Criando o dataset
    dataset = create_dataset_qtd_produtos()

    # Preparando os dados para o gráfico
    produtos = [item['produto'] for item in dataset]
    quantidades_vendidas = [item['quantidade_vendida'] for item in dataset]

    # Criando gráfico de pizza
    fig = px.pie(values=quantidades_vendidas, names=produtos, title='Quantidade de Produtos Vendidos')

    return fig


def charts(request):
    # Input do ano
    ano = request.GET.get('ano', '2024')

    #Criando graficos
    fig_pieChart = chart_pie_produtos()

    #Convertendo graficos para html
    plotPie_div = fig_pieChart.to_html()

    context = {
        'plotPie_div': plotPie_div,
        'ano': ano
    }
    # rederizando template
    return render(request, 'loja/chart/charts.html', context)