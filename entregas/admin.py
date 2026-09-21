from django.contrib import admin

from entregas.models import Motorista, Caminhao, Pacote


# Register your models here.
# importa os modelos/classes criadas para o db

admin.site.register(Motorista)
admin.site.register(Caminhao)
admin.site.register(Pacote)
