from django.db.models import Sum, F
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from .models import Funcionario, Fabricante, Produto, Venda, ProdutoVenda
from .form import FuncionarioForm, FabricanteForm, ProdutoForm, ProdutoVendaForm, VendaForm
import plotly.express as px
import pandas as pd


def home(request):
    return render(request, 'loja/home.html')


# Funcionarios
def listar_funcionarios(request):
    data = {}
    data['funcionarios'] = Funcionario.objects.all()
    return render(request, 'loja/funcionarios/funcionarios.html', data)


def new_funcionario(request):
    data = {}
    form = FuncionarioForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('url_funcionarios')
    data['form'] = form
    return render(request, 'loja/funcionarios/newFuncionario.html', data)


def update_funcionario(request, pk):
    data = {}
    funcionario = Funcionario.objects.get(pk=pk)
    form = FuncionarioForm(request.POST or None, instance=funcionario)

    if form.is_valid():
        form.save()
        return redirect('url_funcionarios')

    data['form'] = form
    data['funcionario'] = funcionario
    return render(request, 'loja/funcionarios/newFuncionario.html', data)


def delete_funcionario(request, pk):
    funcionario = Funcionario.objects.get(pk=pk)
    funcionario.delete()
    return redirect('url_funcionarios')


#Fabricantes
def listar_fabricantes(request):
    data = {}
    data['fabricantes'] = Fabricante.objects.all()
    return render(request, 'loja/fabricantes/fabricantes.html', data)


def new_fabricante(request):
    data = {}
    form = FabricanteForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('url_fabricantes')

    data['form'] = form
    return render(request, 'loja/fabricantes/newFabricante.html', data)


def update_fabricante(request, pk):
    data = {}
    fabricante = Fabricante.objects.get(pk=pk)
    form = FabricanteForm(request.POST or None, instance=fabricante)

    if form.is_valid():
        form.save()
        return redirect('url_fabricantes')

    data['form'] = form
    data['fabricante'] = fabricante
    return render(request, 'loja/fabricantes/newFabricante.html', data)


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
    data = {}
    form = ProdutoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('url_produtos')

    data['form'] = form
    return render(request, 'loja/produtos/newProduto.html', data)


def update_produto(request, pk):
    data = {}
    produto = Produto.objects.get(pk=pk)
    form = ProdutoForm(request.POST or None, instance=produto)

    if form.is_valid():
        form.save()
        return redirect('url_produtos')

    data['form'] = form
    data['produto'] = produto
    return render(request, 'loja/produtos/newProduto.html', data)


def delete_produto(request, pk):
    produto = Produto.objects.get(pk=pk)
    produto.delete()
    return redirect('url_produtos')


#Vendas
def listar_vendas(request):
    vendas = Venda.objects.all().prefetch_related('produtos_vendidos__produto')
    return render(request, 'loja/vendas/vendas.html', {'vendas': vendas})


def new_venda(request):
    if request.method == 'GET':
        #formulario de venda
        form = VendaForm()
        #formset de produtos da venda
        form_produto_factory = inlineformset_factory(Venda, ProdutoVenda, form=ProdutoVendaForm, extra=1)
        form_produtoVenda = form_produto_factory()
        context = {
            'form': form,
            'form_produtos': form_produtoVenda
        }
        #renderiza a pagina
        return render(request, 'loja/vendas/newVenda.html', context)
    elif request.method == 'POST':
        #cria formulario com os dados
        form = VendaForm(request.POST)
        form_produto_factory = inlineformset_factory(Venda, ProdutoVenda, form=ProdutoVendaForm)
        form_produtoVenda = form_produto_factory(request.POST)

        #valida os formularios
        if form.is_valid() and form_produtoVenda.is_valid():
            #INSERT
            valorVenda = 0

            #Atualizando Quantidade vendida de produtos
            for produto_venda in form_produtoVenda.cleaned_data:
                produto = produto_venda['produto']
                quantidade = produto_venda['quantidade']
                produto.qtd_vendida += quantidade
                valorVenda += produto.preco_venda*quantidade #Incrementando valor total da venda
                produto.save()

            #Atribuindo valor total da venda
            venda = form.save(commit=False)
            venda.valorVenda = valorVenda
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
    if request.method == 'GET':
        #obtem venda
        venda = Venda.objects.get(pk=pk)
        #cria formulario com os dados de venda preenchidos
        form = VendaForm(instance=venda)
        #cria o formulario com os dados de produtos preenchidos
        form_produto_factory = inlineformset_factory(Venda, ProdutoVenda, form=ProdutoVendaForm, extra=1)
        form_produtoVenda = form_produto_factory(instance=venda)
        context = {
            'form': form,
            'form_produtos': form_produtoVenda,
            'venda': venda
        }
        #renderiza a pagina
        return render(request, 'loja/vendas/newVenda.html', context)
    elif request.method == 'POST':
        #obtem venda
        venda = Venda.objects.get(pk=pk)
        #cria um formulario com venda exitente e os novos dados
        form = VendaForm(request.POST, instance=venda)
        form_produto_factory = inlineformset_factory(Venda, ProdutoVenda, form=ProdutoVendaForm)
        form_produtoVenda = form_produto_factory(request.POST, instance=venda)

        #validação dos formularios
        if form.is_valid() and form_produtoVenda.is_valid():
            #UPDATE
            #Guardando as quantidades antigas
            quantidades_antigas = {pv.produto_id: pv.quantidade for pv in venda.produtos_vendidos.all()}
            quantidades_novas = {}
            valorVenda = venda.valorVenda

            #Atualizado quantidade vendida de produtos
            for pv in form_produtoVenda.save(commit=False):
                produto = pv.produto
                quantidade_nova = pv.quantidade
                quantidade_antiga = quantidades_antigas.get(produto.id, 0)

                valorVenda += (produto.preco_venda*quantidade_nova) - (produto.preco_venda*quantidade_antiga)

                produto.qtd_vendida = produto.qtd_vendida + quantidade_nova - quantidade_antiga
                produto.save()

                quantidades_novas[produto.id] = quantidade_nova

            # Deleta os objetos removidos
            for pv in form_produtoVenda.deleted_objects:
                produto = pv.produto
                produto.qtd_vendida -= pv.quantidade

                valorVenda -= produto.preco_venda*pv.quantidade

                produto.save()
                pv.delete()

            venda = form.save(commit=False)
            venda.valorVenda = valorVenda
            venda.save()
            form_produtoVenda.instance = venda
            form_produtoVenda.save()


            #Retorna para a tela da tabela
            return redirect('url_vendas')
        else:
            # se não for válido rendezina novamente a página e mostra os campos inconsistentes
            context = {
                'form': form,
                'form_produtos': form_produtoVenda,
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
def chart_top3(ano):
    # Requisitando dados dos produtos do banco de dados
    data_queryset = ProdutoVenda.objects.filter(
        venda__data__year=ano
    ).values(
        'produto__nome'
    ).annotate(
        mes=F('venda__data__month'),
        valor=Sum(F('quantidade') * F('produto__preco_venda'))
    ).order_by('-valor')[:3]

    # Montando base de dados
    data = [{'nome': item['produto__nome'], 'mes': str(item['mes']).zfill(2), 'valor': item['valor']} for item in
            data_queryset]

    # Preparando dados
    labels = [f"{item['nome']} - Mês {item['mes']}" for item in data]
    values = [item['valor'] for item in data]

    # Criando gráfico
    fig = px.pie(values=values, names=labels, title=f'Produtos mais vendidos, em valor mensal no ano {ano}')

    return fig


def line_chart(ano):
    # Obter dados de custos e vendas usando o ORM do Django
    custos = ProdutoVenda.objects.filter(venda__data__year=ano).values( #WHERE year(data) = ano
        mes=F('venda__data__month')                                     #SELECT month(data)
    ).annotate(
        preco_custo=Sum(F('produto__preco_custo') * F('quantidade'))
    ).values('mes', 'preco_custo')

    vendas = Venda.objects.filter(data__year=ano).values(
        mes=F('data__month')
    ).annotate(
        valor_venda=Sum('valorVenda')
    ).values('mes', 'valor_venda')

    # Criar um dicionário para armazenar os dados agregados
    data = {str(i).zfill(2): {'preco_custo': 0, 'valor_venda': 0} for i in range(1, 13)}

    # Atualizar o dicionário com os dados de custos
    for custo in custos:
        mes = str(custo['mes']).zfill(2)
        data[mes]['preco_custo'] = custo['preco_custo']

    # Atualizar o dicionário com os dados de vendas
    for venda in vendas:
        mes = str(venda['mes']).zfill(2)
        data[mes]['valor_venda'] = venda['valor_venda']

    # Converter o dicionário em uma lista de dicionários para criar o DataFrame
    data_list = [{'mes': mes, 'preco_custo': valores['preco_custo'], 'valor_venda': valores['valor_venda']} for
                 mes, valores in data.items()]

    # Criar o DataFrame
    df = pd.DataFrame(data_list)

    # Criar o gráfico de linha usando Plotly
    fig = px.line(df, x='mes', y=['preco_custo', 'valor_venda'], title=f'Valor custo e venda dos produtos vendidos mensalmente no ano {ano}')

    return fig


def charts(request):
    # Input do ano
    ano = request.GET.get('ano', '2024')

    #Criando graficos
    fig_pieChart = chart_top3(ano)
    fig_lineChart = line_chart(ano)

    #Convertendo graficos para html
    plotPie_div = fig_pieChart.to_html()
    plotLine_div = fig_lineChart.to_html()

    context = {
        'plotPie_div': plotPie_div,
        'plotLine_div': plotLine_div,
        'ano': ano
    }
    # rederizando template
    return render(request, 'loja/chart/charts.html', context)


def teste(request):
    return render(request, 'loja/chart/plotly.html')