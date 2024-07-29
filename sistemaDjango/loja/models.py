from django.db import models


class Funcionario(models.Model):
    login = models.CharField(max_length=250, unique=True)
    nome = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)

    def __str__(self):
        return self.nome


class Fabricante(models.Model):
    cnpj = models.CharField(max_length=19)
    nome_fantasia = models.CharField(max_length=250)
    razao_social = models.CharField(max_length=250)
    endereco = models.CharField(max_length=250)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(max_length=250)
    vendedor = models.CharField(max_length=250)

    def __str__(self):
        return self.nome_fantasia


class Produto(models.Model):
    nome = models.CharField(max_length=250)
    descrissao = models.TextField(max_length=250, null=True)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    qtd_comprada = models.IntegerField(default=0)
    qtd_vendida = models.IntegerField(default=0)
    grupo = models.CharField(max_length=250, null=True)
    subgrupo = models.CharField(max_length=250, null=True)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Venda(models.Model):
    data = models.DateField()
    valorVenda = models.DecimalField(max_digits=20, decimal_places=2, default=0)

class ProdutoVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='produtos_vendidos')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='produto')
    quantidade = models.PositiveIntegerField()

