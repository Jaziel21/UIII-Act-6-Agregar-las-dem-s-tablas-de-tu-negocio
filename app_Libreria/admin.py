# app_Libreria/admin.py - REEMPLAZAR COMPLETAMENTE

from django.contrib import admin
from .models import Autor, Editorial, Libro, Cliente, Venta, DetalleVenta

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nacionalidad', 'fecha_nacimiento', 'email', 'activo', 'created_at']
    list_filter = ['activo', 'nacionalidad', 'created_at']
    search_fields = ['nombre', 'email', 'nacionalidad']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'pais', 'fundacion', 'email', 'activo', 'created_at']
    list_filter = ['activo', 'pais']
    search_fields = ['nombre', 'email']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'isbn', 'autor', 'editorial', 'genero', 'precio', 'stock', 'disponible']
    list_filter = ['genero', 'editorial', 'autor', 'fecha_publicacion']
    search_fields = ['titulo', 'isbn', 'autor__nombre', 'editorial__nombre']
    # ELIMINAR filter_horizontal porque ya no tenemos ManyToMany

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono', 'tipo_cliente', 'activo', 'fecha_registro']
    list_filter = ['activo', 'tipo_cliente', 'fecha_registro']
    search_fields = ['nombre', 'email']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'fecha_venta', 'total', 'estado']
    list_filter = ['estado', 'fecha_venta', 'cliente']
    search_fields = ['cliente__nombre', 'id']

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'venta', 'libro', 'cantidad', 'precio_unitario', 'subtotal']
    list_filter = ['venta__estado', 'libro']
    search_fields = ['libro__titulo', 'venta__id']