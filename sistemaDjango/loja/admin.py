from django.contrib import admin
from .models import Funcionario, Fabricante, Produto, Venda


admin.site.register(Funcionario)
admin.site.register(Fabricante)
admin.site.register(Produto)
admin.site.register(Venda)
