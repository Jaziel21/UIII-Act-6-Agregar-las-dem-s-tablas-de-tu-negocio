# app_Libreria/models.py - REEMPLAZAR COMPLETAMENTE

from django.db import models
from django.utils import timezone

# ==========================================
# MODELO: EDITORIAL (1:M con Libro)
# ==========================================
class Editorial(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la editorial")
    pais = models.CharField(max_length=50, verbose_name="País de origen")
    fundacion = models.PositiveIntegerField(verbose_name="Año de fundación", null=True, blank=True)
    sitio_web = models.URLField(verbose_name="Sitio web", blank=True)
    email = models.EmailField(verbose_name="Email de contacto", blank=True)
    activo = models.BooleanField(default=True, verbose_name="Editorial activa")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Editorial"
        verbose_name_plural = "Editoriales"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

# ==========================================
# MODELO: AUTOR (1:M con Libro)
# ==========================================
class Autor(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    nacionalidad = models.CharField(max_length=50, verbose_name="Nacionalidad")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    fecha_fallecimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de fallecimiento")
    biografia = models.TextField(verbose_name="Biografía", help_text="Breve biografía del autor")
    email = models.EmailField(verbose_name="Email de contacto", blank=True)
    activo = models.BooleanField(default=True, verbose_name="Autor activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

# ==========================================
# MODELO: LIBRO (Muchos:1 con Editorial y Autor)
# ==========================================
class Libro(models.Model):
    GENEROS = [
        ('FIC', 'Ficción'),
        ('ROM', 'Romance'),
        ('TER', 'Terror'),
        ('CIE', 'Ciencia Ficción'),
        ('FAN', 'Fantasía'),
        ('HIS', 'Histórico'),
        ('BIO', 'Biografía'),
        ('INF', 'Infantil'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título del libro")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    genero = models.CharField(max_length=3, choices=GENEROS, verbose_name="Género")
    fecha_publicacion = models.DateField(verbose_name="Fecha de publicación")
    precio = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Precio")
    stock = models.PositiveIntegerField(default=0, verbose_name="Cantidad en stock")
    descripcion = models.TextField(verbose_name="Descripción", blank=True)
    
    # RELACIONES 1:MUCHOS
    editorial = models.ForeignKey(
        Editorial, 
        on_delete=models.CASCADE,  # Si se elimina la editorial, se eliminan sus libros
        related_name='libros',
        verbose_name="Editorial"
    )
    
    autor = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE,  # Si se elimina el autor, se eliminan sus libros
        related_name='libros', 
        verbose_name="Autor"
    )
    
    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ['titulo']
    
    def __str__(self):
        return self.titulo
    
    def disponible(self):
        return self.stock > 0

# ==========================================
# MODELO: CLIENTE (1:M con Venta)
# ==========================================
class Cliente(models.Model):
    TIPOS_CLIENTE = [
        ('REG', 'Regular'),
        ('VIP', 'VIP'),
        ('EMP', 'Empresarial'),
    ]
    
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    email = models.EmailField(verbose_name="Email", unique=True)
    telefono = models.CharField(max_length=15, verbose_name="Teléfono", blank=True)
    direccion = models.TextField(verbose_name="Dirección", blank=True)
    tipo_cliente = models.CharField(max_length=3, choices=TIPOS_CLIENTE, default='REG', verbose_name="Tipo de cliente")
    fecha_registro = models.DateField(auto_now_add=True, verbose_name="Fecha de registro")
    activo = models.BooleanField(default=True, verbose_name="Cliente activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

# ==========================================
# MODELO: VENTA (Muchos:1 con Cliente, 1:M con DetalleVenta)
# ==========================================
class Venta(models.Model):
    ESTADOS = [
        ('PEN', 'Pendiente'),
        ('COM', 'Completada'),
        ('CAN', 'Cancelada'),
        ('DEV', 'Devuelta'),
    ]
    
    fecha_venta = models.DateTimeField(default=timezone.now, verbose_name="Fecha de venta")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total de la venta", default=0)
    estado = models.CharField(max_length=3, choices=ESTADOS, default='PEN', verbose_name="Estado de la venta")
    
    # RELACIÓN 1:MUCHOS con Cliente
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,  # Si se elimina el cliente, se eliminan sus ventas
        related_name='ventas',
        verbose_name="Cliente"
    )
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha_venta']
    
    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.nombre}"
    
    def calcular_total(self):
        total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.total = total
        self.save()
        return total

# ==========================================
# MODELO: DETALLE VENTA (Muchos:1 con Venta y Libro)
# ==========================================
class DetalleVenta(models.Model):
    # RELACIÓN 1:MUCHOS con Venta
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,  # Si se elimina la venta, se eliminan sus detalles
        related_name='detalles',
        verbose_name="Venta"
    )
    
    # RELACIÓN 1:MUCHOS con Libro
    libro = models.ForeignKey(
        Libro,
        on_delete=models.PROTECT,  # Proteger el libro si tiene ventas
        related_name='detalles_venta',
        verbose_name="Libro"
    )
    
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Precio unitario")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")

    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Venta"

    def __str__(self):
        return f"Detalle #{self.id} - {self.libro.titulo}"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        # Actualizar el total de la venta
        self.venta.calcular_total()