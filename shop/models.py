from django.contrib.auth.models import User
from django.db import models


class Seleccion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imagen = models.URLField(blank=True)

    def __str__(self):
        return self.nombre


class CarritoItem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    seleccion = models.ForeignKey(Seleccion, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    agregado = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.seleccion.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.seleccion.nombre}"
