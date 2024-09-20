from django.contrib import admin
from .models import Grupo, Renda, Gasto


admin.site.register(Grupo)
admin.site.register(Renda)
admin.site.register(Gasto)