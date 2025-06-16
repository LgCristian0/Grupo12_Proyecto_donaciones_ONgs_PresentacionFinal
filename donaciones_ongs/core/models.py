from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class ONG(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username

class Donante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Campaña(models.Model):
    ong = models.ForeignKey('ONG', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    monto_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    meta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]  # mínimo 0.01
    )
    descripcion = models.TextField(default='')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre

class Donacion(models.Model):
    donante = models.ForeignKey(Donante, on_delete=models.CASCADE)
    campaña = models.ForeignKey(Campaña, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.donante.user.username} donó {self.monto} Bs"

    
