# app_Libreria/urls.py - AGREGAR NUEVAS RUTAS

from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_libreria, name='inicio_libreria'),
    
    # Rutas para Autores (existentes)
    path('autores/agregar/', views.agregar_autor, name='agregar_autor'),
    path('autores/', views.ver_autores, name='ver_autores'),
    path('autores/editar/<int:autor_id>/', views.actualizar_autor, name='actualizar_autor'),
    path('autores/editar/guardar/<int:autor_id>/', views.realizar_actualizacion_autor, name='realizar_actualizacion_autor'),
    path('autores/borrar/<int:autor_id>/', views.borrar_autor, name='borrar_autor'),
    
    # Rutas para Editoriales (nuevas)
    path('editoriales/agregar/', views.agregar_editorial, name='agregar_editorial'),
    path('editoriales/', views.ver_editoriales, name='ver_editoriales'),
    path('editoriales/editar/<int:editorial_id>/', views.actualizar_editorial, name='actualizar_editorial'),
    path('editoriales/editar/guardar/<int:editorial_id>/', views.realizar_actualizacion_editorial, name='realizar_actualizacion_editorial'),
    path('editoriales/borrar/<int:editorial_id>/', views.borrar_editorial, name='borrar_editorial'),
    
    # Rutas para Libros (actualizadas)
    path('libros/agregar/', views.agregar_libro, name='agregar_libro'),
    path('libros/', views.ver_libros, name='ver_libros'),
    path('libros/editar/<int:libro_id>/', views.actualizar_libro, name='actualizar_libro'),
    path('libros/editar/guardar/<int:libro_id>/', views.realizar_actualizacion_libro, name='realizar_actualizacion_libro'),
    path('libros/borrar/<int:libro_id>/', views.borrar_libro, name='borrar_libro'),
    
    # Rutas para Clientes (nuevas)
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/', views.ver_clientes, name='ver_clientes'),
    path('clientes/editar/<int:cliente_id>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/editar/guardar/<int:cliente_id>/', views.realizar_actualizacion_cliente, name='realizar_actualizacion_cliente'),
    path('clientes/borrar/<int:cliente_id>/', views.borrar_cliente, name='borrar_cliente'),
    
    # Rutas para Ventas (actualizadas)
    path('ventas/agregar/', views.agregar_venta, name='agregar_venta'),
    path('ventas/', views.ver_ventas, name='ver_ventas'),
    path('ventas/editar/<int:venta_id>/', views.actualizar_venta, name='actualizar_venta'),
    path('ventas/editar/guardar/<int:venta_id>/', views.realizar_actualizacion_venta, name='realizar_actualizacion_venta'),
    path('ventas/borrar/<int:venta_id>/', views.borrar_venta, name='borrar_venta'),
    path('ventas/detalles/<int:venta_id>/', views.ver_detalles_venta, name='ver_detalles_venta'),
    # Rutas para Detalles de Venta
    path('ventas/detalles/<int:venta_id>/', views.ver_detalles_venta, name='ver_detalles_venta'),
    path('ventas/detalles/<int:venta_id>/agregar/', views.agregar_detalle_venta, name='agregar_detalle_venta'),
    path('ventas/detalles/editar/<int:detalle_id>/', views.actualizar_detalle_venta, name='actualizar_detalle_venta'),
    path('ventas/detalles/editar/guardar/<int:detalle_id>/', views.realizar_actualizacion_detalle_venta, name='realizar_actualizacion_detalle_venta'),
    path('ventas/detalles/borrar/<int:detalle_id>/', views.borrar_detalle_venta, name='borrar_detalle_venta'),
]