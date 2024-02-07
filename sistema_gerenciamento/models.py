import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Veiculo(models.Model):
    id = models.BigAutoField(primary_key=True)
    modelo = models.CharField(max_length=40, null=False)
    fabricante = models.CharField(max_length=40, null=False)
    ano = models.IntegerField(null=False)
    placa = models.CharField(max_length=10, null=False)
    data_cadastro = models.DateField(null=False)
    estado_funcionamento = models.CharField(max_length=16, null=False)

    def __str__(self):
        return f"{self.modelo}"


def validate_image_file(value):
    validator = FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
    validator(value.file)


class Manutencao(models.Model):
    id = models.BigAutoField(primary_key=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data = models.DateField(null=False)
    descricao_manutencao = models.TextField(max_length=100, null=False)
    comprovante_manutencao = models.ImageField(upload_to='comprovantes/manutenções/', null=False)

    def __str__(self):
        return f"{self.veiculo} - Data: {self.data}"

    def validate_image(self):
        validator = FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        validator(self.comprovante_manutencao.file)

    def save(self, *args, **kwargs):
        self.validate_image()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.comprovante_manutencao:
            if os.path.isfile(self.comprovante_manutencao.path):
                os.remove(self.comprovante_manutencao.path)
        super().delete(*args, **kwargs)


class Checklist(models.Model):
    id = models.BigAutoField(primary_key=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data = models.DateField(null=False)
    comprovante_checklist = models.ImageField(upload_to='comprovantes/checklists/', null=False)
    
    def __str__(self):
        return f"{self.veiculo} - Data: {self.data}"
    
    def validate_image(self):
        validator = FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        validator(self.comprovante_checklist.file)
        
    def save(self, *args, **kwargs):
        self.validate_image()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.comprovante_checklist:
            if os.path.isfile(self.comprovante_checklist.path):
                os.remove(self.comprovante_checklist.path)
        super().delete(*args, **kwargs)


class Motorista(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=40, null=False)
    telefone = models.CharField(max_length=15, null=False)
    data_cadastro = models.DateField(null=False)
    documentos = models.FileField(upload_to='motoristas/documentos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nome}"

    def delete(self, *args, **kwargs):
        if self.documentos:
            if os.path.isfile(self.documentos.path):
                os.remove(self.documentos.path)
        super().delete(*args, **kwargs)


class Rota(models.Model):
    nome = models.CharField(max_length=100)
    turnos = (
        ('Manhã', 'Manhã'),
        ('Tarde', 'Tarde'),
        ('Noite', 'Noite'),
    )
    turno = models.CharField(max_length=5, choices=turnos)
    horario_saida = models.TimeField()
    horario_retorno = models.TimeField()
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    paradas = models.TextField(help_text="Digite as paradas separadas por vírgula")

    def get_paradas_list(self):
        return [parada.strip() for parada in self.paradas.split(',')]

    def __str__(self):
        return self.nome


class Combustivel(models.Model):
    id = models.BigAutoField(primary_key=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data_cadastro = models.DateField(null=False)
    quantidade_abastecida = models.IntegerField(null=False)
    custo = models.IntegerField(null=False)
    comprovante_abastecimento = models.ImageField(upload_to="comprovantes/abastecimentos/", null=False)

    def __str__(self):
        return f"{self.veiculo} - Data: {self.data_cadastro}"

    def validate_image(self):
        validator = FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        validator(self.comprovante_abastecimento.file)

    def save(self, *args, **kwargs):
        self.validate_image()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.comprovante_abastecimento:
            if os.path.isfile(self.comprovante_abastecimento.path):
                os.remove(self.comprovante_abastecimento.path)
        super().delete(*args, **kwargs)


class Demanda(models.Model):
    id = models.BigAutoField(primary_key=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE)
    data = models.DateField(null=True)
    horario_saida = models.TimeField(null=True)
    horario_retorno = models.TimeField(null=True)
    descricao = models.TextField(max_length=100, null=True)

    def __str__(self):
        return f"{self.veiculo} - {self.data}"


class Viagem(models.Model):
    id = models.BigAutoField(primary_key=True)
    destino = models.CharField(max_length=40, null=False)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE)
    data_saida = models.DateField(null=False)
    data_retorno = models.DateField(null=False)
    solicitante = models.CharField(max_length=40, null=False, default="")
    descricao = models.TextField(max_length=100, null=False)

    def __str__(self):
        return f"{self.destino}"
