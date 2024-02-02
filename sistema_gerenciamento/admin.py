from django.contrib import admin

from .models import Veiculo, Manutencao, Checklist, User, Motorista, Combustivel, Rota

# Register your models here.
admin.site.register(User)
admin.site.register(Veiculo)
admin.site.register(Manutencao)
admin.site.register(Checklist)
admin.site.register(Motorista)
admin.site.register(Combustivel)
admin.site.register(Rota)