from django.forms import ModelForm, forms, inlineformset_factory, \
    ModelChoiceField, IntegerField, ComboField
from .models import Funcionario, Fabricante, Produto, Venda, ProdutoVenda


class FuncionarioForm(ModelForm):
    class Meta:
        model = Funcionario
        fields = ['login', 'nome', 'email']


class FabricanteForm(ModelForm):
    class Meta:
        model = Fabricante
        fields = ['cnpj', 'nome_fantasia', 'razao_social', 'endereco', 'telefone', 'email', 'vendedor']


class ProdutoForm(ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descrissao', 'preco_custo', 'preco_venda', 'peso', 'qtd_comprada', 'grupo', 'subgrupo', 'fabricante']


class VendaForm(ModelForm):
    class Meta:
        model = Venda
        fields = ['data']


class ProdutoVendaForm(ModelForm):
    class Meta:
        model = ProdutoVenda
        fields = '__all__'
