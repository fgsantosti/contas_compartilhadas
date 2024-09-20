from django.db import models
from django.contrib.auth.models import User

class Grupo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    criador = models.ForeignKey(User, on_delete=models.CASCADE)
    membros = models.ManyToManyField(User, related_name='grupos', blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome

class Renda(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=255)
    data = models.DateField()

    def __str__(self):
        return f'{self.usuario} - {self.valor}'

class Gasto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=255)
    fixo = models.BooleanField(default=False)
    data = models.DateField()

    def __str__(self):
        return f'{self.usuario} - {self.valor}'
