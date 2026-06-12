from django.contrib import admin

from .models import CarritoItem, Seleccion


@admin.register(Seleccion)
class SeleccionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio')
    search_fields = ('nombre',)


@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'seleccion', 'cantidad', 'agregado')
    list_filter = ('usuario',)
