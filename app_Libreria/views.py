# app_Libreria/views.py - REEMPLAZAR COMPLETAMENTE

from django.shortcuts import render, redirect, get_object_or_404
from .models import Autor, Editorial, Libro, Cliente, Venta, DetalleVenta
from django.utils import timezone

# ==========================================
# VISTAS PARA PÁGINA PRINCIPAL
# ==========================================

def inicio_libreria(request):
    contexto = {
        'titulo': 'Sistema de Administración Libreria AJMG 1194',
        'now': timezone.now()
    }
    return render(request, 'inicio.html', contexto)

# ==========================================
# VISTAS PARA MODELO AUTOR
# ==========================================

def agregar_autor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        nacionalidad = request.POST.get('nacionalidad')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        fecha_fallecimiento = request.POST.get('fecha_fallecimiento') or None
        biografia = request.POST.get('biografia')
        email = request.POST.get('email')
        activo = True if request.POST.get('activo') == 'on' else False

        Autor.objects.create(
            nombre=nombre,
            nacionalidad=nacionalidad,
            fecha_nacimiento=fecha_nacimiento,
            fecha_fallecimiento=fecha_fallecimiento,
            biografia=biografia,
            email=email,
            activo=activo,
        )
        return redirect('ver_autores')

    return render(request, 'autor/agregar_autor.html')

def ver_autores(request):
    autores = Autor.objects.all()
    return render(request, 'autor/ver_autores.html', {'autores': autores})

def actualizar_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    return render(request, 'autor/actualizar_autor.html', {'autor': autor})

def realizar_actualizacion_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    if request.method == 'POST':
        autor.nombre = request.POST.get('nombre')
        autor.nacionalidad = request.POST.get('nacionalidad')
        autor.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        fecha_fallecimiento = request.POST.get('fecha_fallecimiento') or None
        autor.fecha_fallecimiento = fecha_fallecimiento
        autor.biografia = request.POST.get('biografia')
        autor.email = request.POST.get('email')
        autor.activo = True if request.POST.get('activo') == 'on' else False
        autor.save()
        return redirect('ver_autores')
    return redirect('actualizar_autor', autor_id=autor_id)

def borrar_autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    if request.method == 'POST':
        autor.delete()
        return redirect('ver_autores')
    return render(request, 'autor/borrar_autor.html', {'autor': autor})

# ==========================================
# VISTAS PARA MODELO EDITORIAL
# ==========================================

def agregar_editorial(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        pais = request.POST.get('pais')
        fundacion = request.POST.get('fundacion') or None
        sitio_web = request.POST.get('sitio_web')
        email = request.POST.get('email')
        activo = True if request.POST.get('activo') == 'on' else False

        Editorial.objects.create(
            nombre=nombre,
            pais=pais,
            fundacion=fundacion,
            sitio_web=sitio_web,
            email=email,
            activo=activo,
        )
        return redirect('ver_editoriales')

    return render(request, 'editorial/agregar_editorial.html')

def ver_editoriales(request):
    editoriales = Editorial.objects.all()
    return render(request, 'editorial/ver_editoriales.html', {'editoriales': editoriales})

def actualizar_editorial(request, editorial_id):
    editorial = get_object_or_404(Editorial, id=editorial_id)
    return render(request, 'editorial/actualizar_editorial.html', {'editorial': editorial})

def realizar_actualizacion_editorial(request, editorial_id):
    editorial = get_object_or_404(Editorial, id=editorial_id)
    if request.method == 'POST':
        editorial.nombre = request.POST.get('nombre')
        editorial.pais = request.POST.get('pais')
        editorial.fundacion = request.POST.get('fundacion') or None
        editorial.sitio_web = request.POST.get('sitio_web')
        editorial.email = request.POST.get('email')
        editorial.activo = True if request.POST.get('activo') == 'on' else False
        editorial.save()
        return redirect('ver_editoriales')
    return redirect('actualizar_editorial', editorial_id=editorial_id)

def borrar_editorial(request, editorial_id):
    editorial = get_object_or_404(Editorial, id=editorial_id)
    if request.method == 'POST':
        editorial.delete()
        return redirect('ver_editoriales')
    return render(request, 'editorial/borrar_editorial.html', {'editorial': editorial})

# ==========================================
# VISTAS PARA MODELO LIBRO (ACTUALIZADAS PARA 1:M)
# ==========================================

def agregar_libro(request):
    if request.method == 'POST':
        try:
            titulo = request.POST.get('titulo')
            isbn = request.POST.get('isbn')
            genero = request.POST.get('genero')
            fecha_publicacion = request.POST.get('fecha_publicacion')
            precio = request.POST.get('precio')
            stock = request.POST.get('stock')
            descripcion = request.POST.get('descripcion')
            editorial_id = request.POST.get('editorial')
            autor_id = request.POST.get('autor')  # Ahora es solo UN autor (1:M)
            
            editorial = Editorial.objects.get(id=editorial_id)
            autor = Autor.objects.get(id=autor_id)
            
            libro = Libro.objects.create(
                titulo=titulo,
                isbn=isbn,
                genero=genero,
                fecha_publicacion=fecha_publicacion,
                precio=precio,
                stock=stock,
                descripcion=descripcion,
                editorial=editorial,
                autor=autor
            )
            
            return redirect('ver_libros')
            
        except Exception as e:
            autores = Autor.objects.filter(activo=True)
            editoriales = Editorial.objects.filter(activo=True)
            generos = Libro.GENEROS
            return render(request, 'libro/agregar_libro.html', {
                'autores': autores,
                'editoriales': editoriales,
                'generos': generos,
                'error': f'Error al crear el libro: {str(e)}'
            })
    
    # GET request - mostrar formulario
    autores = Autor.objects.filter(activo=True)
    editoriales = Editorial.objects.filter(activo=True)
    generos = Libro.GENEROS
    return render(request, 'libro/agregar_libro.html', {
        'autores': autores,
        'editoriales': editoriales,
        'generos': generos
    })

def ver_libros(request):
    libros = Libro.objects.all().select_related('autor', 'editorial')  # Optimizado para 1:M
    return render(request, 'libro/ver_libros.html', {'libros': libros})

def actualizar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    autores = Autor.objects.filter(activo=True)
    editoriales = Editorial.objects.filter(activo=True)
    generos = Libro.GENEROS
    
    return render(request, 'libro/actualizar_libro.html', {
        'libro': libro,
        'autores': autores,
        'editoriales': editoriales,
        'generos': generos
    })

def realizar_actualizacion_libro(request, libro_id):
    if request.method == 'POST':
        try:
            libro = get_object_or_404(Libro, id=libro_id)
            
            # Actualizar campos básicos
            libro.titulo = request.POST.get('titulo')
            libro.isbn = request.POST.get('isbn')
            libro.genero = request.POST.get('genero')
            libro.fecha_publicacion = request.POST.get('fecha_publicacion')
            libro.precio = request.POST.get('precio')
            libro.stock = request.POST.get('stock')
            libro.descripcion = request.POST.get('descripcion')
            
            # Actualizar relaciones 1:M
            editorial_id = request.POST.get('editorial')
            autor_id = request.POST.get('autor')
            
            libro.editorial = Editorial.objects.get(id=editorial_id)
            libro.autor = Autor.objects.get(id=autor_id)
            
            libro.save()
            
            return redirect('ver_libros')
            
        except Exception as e:
            libro = get_object_or_404(Libro, id=libro_id)
            autores = Autor.objects.filter(activo=True)
            editoriales = Editorial.objects.filter(activo=True)
            generos = Libro.GENEROS
            return render(request, 'libro/actualizar_libro.html', {
                'libro': libro,
                'autores': autores,
                'editoriales': editoriales,
                'generos': generos,
                'error': f'Error al actualizar: {str(e)}'
            })
    
    return redirect('actualizar_libro', libro_id=libro_id)

def borrar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    
    if request.method == 'POST':
        libro.delete()
        return redirect('ver_libros')
    
    return render(request, 'libro/borrar_libro.html', {'libro': libro})

# ==========================================
# VISTAS PARA MODELO CLIENTE
# ==========================================

def agregar_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        tipo_cliente = request.POST.get('tipo_cliente')
        activo = True if request.POST.get('activo') == 'on' else False

        Cliente.objects.create(
            nombre=nombre,
            email=email,
            telefono=telefono,
            direccion=direccion,
            tipo_cliente=tipo_cliente,
            activo=activo,
        )
        return redirect('ver_clientes')

    return render(request, 'cliente/agregar_cliente.html')

def ver_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/ver_clientes.html', {'clientes': clientes})

def actualizar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'cliente/actualizar_cliente.html', {'cliente': cliente})

def realizar_actualizacion_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre')
        cliente.email = request.POST.get('email')
        cliente.telefono = request.POST.get('telefono')
        cliente.direccion = request.POST.get('direccion')
        cliente.tipo_cliente = request.POST.get('tipo_cliente')
        cliente.activo = True if request.POST.get('activo') == 'on' else False
        cliente.save()
        return redirect('ver_clientes')
    return redirect('actualizar_cliente', cliente_id=cliente_id)

def borrar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('ver_clientes')
    return render(request, 'cliente/borrar_cliente.html', {'cliente': cliente})

# ==========================================
# VISTAS PARA MODELO VENTA (ACTUALIZADAS PARA 1:M)
# ==========================================

def agregar_venta(request):
    if request.method == 'POST':
        try:
            cliente_id = request.POST.get('cliente')
            estado = request.POST.get('estado')
            
            cliente = Cliente.objects.get(id=cliente_id)
            
            # Crear la venta (1:M con Cliente)
            venta = Venta.objects.create(
                cliente=cliente,
                estado=estado
            )
            
            return redirect('ver_ventas')
            
        except Exception as e:
            clientes = Cliente.objects.filter(activo=True)
            return render(request, 'venta/agregar_venta.html', {
                'clientes': clientes,
                'error': f'Error al crear la venta: {str(e)}'
            })
    
    # GET request
    clientes = Cliente.objects.filter(activo=True)
    return render(request, 'venta/agregar_venta.html', {
        'clientes': clientes
    })

def ver_ventas(request):
    ventas = Venta.objects.all().select_related('cliente')  # Optimizado para 1:M
    return render(request, 'venta/ver_ventas.html', {'ventas': ventas})

def actualizar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    clientes = Cliente.objects.filter(activo=True)
    
    return render(request, 'venta/actualizar_venta.html', {
        'venta': venta,
        'clientes': clientes
    })

def realizar_actualizacion_venta(request, venta_id):
    if request.method == 'POST':
        try:
            venta = get_object_or_404(Venta, id=venta_id)
            
            cliente_id = request.POST.get('cliente')
            estado = request.POST.get('estado')
            
            cliente = Cliente.objects.get(id=cliente_id)
            
            # Actualizar venta (1:M con Cliente)
            venta.cliente = cliente
            venta.estado = estado
            venta.save()
            
            return redirect('ver_ventas')
            
        except Exception as e:
            venta = get_object_or_404(Venta, id=venta_id)
            clientes = Cliente.objects.filter(activo=True)
            return render(request, 'venta/actualizar_venta.html', {
                'venta': venta,
                'clientes': clientes,
                'error': f'Error al actualizar la venta: {str(e)}'
            })
    
    return redirect('actualizar_venta', venta_id=venta_id)

def borrar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    
    if request.method == 'POST':
        venta.delete()
        return redirect('ver_ventas')
    
    return render(request, 'venta/borrar_venta.html', {'venta': venta})

# ==========================================
# VISTAS PARA DETALLES VENTA (1:M con Venta y Libro)
# ==========================================

def ver_detalles_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = venta.detalles.all().select_related('libro')  # Optimizado para 1:M
    return render(request, 'detalle_venta/ver_detalles.html', {
        'venta': venta,
        'detalles': detalles
    })
# app_Libreria/views.py - AGREGAR ESTAS FUNCIONES AL FINAL

# ==========================================
# VISTAS PARA DETALLES VENTA (COMPLETAS)
# ==========================================

def agregar_detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    
    if request.method == 'POST':
        try:
            libro_id = request.POST.get('libro')
            cantidad = int(request.POST.get('cantidad'))
            precio_unitario = float(request.POST.get('precio_unitario'))
            
            libro = Libro.objects.get(id=libro_id)
            
            # Verificar stock disponible
            if libro.stock < cantidad:
                libros = Libro.objects.filter(stock__gt=0)
                return render(request, 'detalle_venta/agregar_detalle.html', {
                    'venta': venta,
                    'libros': libros,
                    'error': f'Stock insuficiente. Solo hay {libro.stock} unidades disponibles.'
                })
            
            # Crear el detalle de venta
            detalle = DetalleVenta.objects.create(
                venta=venta,
                libro=libro,
                cantidad=cantidad,
                precio_unitario=precio_unitario
            )
            
            # Actualizar stock del libro
            libro.stock -= cantidad
            libro.save()
            
            # Recalcular total de la venta
            venta.calcular_total()
            
            return redirect('ver_detalles_venta', venta_id=venta.id)
            
        except Exception as e:
            libros = Libro.objects.filter(stock__gt=0)
            return render(request, 'detalle_venta/agregar_detalle.html', {
                'venta': venta,
                'libros': libros,
                'error': f'Error al agregar detalle: {str(e)}'
            })
    
    # GET request
    libros = Libro.objects.filter(stock__gt=0)
    return render(request, 'detalle_venta/agregar_detalle.html', {
        'venta': venta,
        'libros': libros
    })

def actualizar_detalle_venta(request, detalle_id):
    detalle = get_object_or_404(DetalleVenta, id=detalle_id)
    libros = Libro.objects.all()
    
    return render(request, 'detalle_venta/actualizar_detalle.html', {
        'detalle': detalle,
        'libros': libros
    })

def realizar_actualizacion_detalle_venta(request, detalle_id):
    if request.method == 'POST':
        try:
            detalle = get_object_or_404(DetalleVenta, id=detalle_id)
            libro_anterior = detalle.libro
            cantidad_anterior = detalle.cantidad
            
            # Obtener nuevos valores
            libro_id = request.POST.get('libro')
            cantidad = int(request.POST.get('cantidad'))
            precio_unitario = float(request.POST.get('precio_unitario'))
            
            libro_nuevo = Libro.objects.get(id=libro_id)
            
            # Manejar cambios en libro y cantidad
            if libro_anterior != libro_nuevo or cantidad != cantidad_anterior:
                # Restaurar stock del libro anterior
                libro_anterior.stock += cantidad_anterior
                libro_anterior.save()
                
                # Verificar stock del nuevo libro
                if libro_nuevo.stock < cantidad:
                    libros = Libro.objects.all()
                    return render(request, 'detalle_venta/actualizar_detalle.html', {
                        'detalle': detalle,
                        'libros': libros,
                        'error': f'Stock insuficiente. Solo hay {libro_nuevo.stock} unidades disponibles.'
                    })
                
                # Actualizar stock del nuevo libro
                libro_nuevo.stock -= cantidad
                libro_nuevo.save()
            
            # Actualizar el detalle
            detalle.libro = libro_nuevo
            detalle.cantidad = cantidad
            detalle.precio_unitario = precio_unitario
            detalle.save()  # Esto actualiza automáticamente el subtotal
            
            # Recalcular total de la venta
            detalle.venta.calcular_total()
            
            return redirect('ver_detalles_venta', venta_id=detalle.venta.id)
            
        except Exception as e:
            detalle = get_object_or_404(DetalleVenta, id=detalle_id)
            libros = Libro.objects.all()
            return render(request, 'detalle_venta/actualizar_detalle.html', {
                'detalle': detalle,
                'libros': libros,
                'error': f'Error al actualizar detalle: {str(e)}'
            })
    
    return redirect('actualizar_detalle_venta', detalle_id=detalle_id)

def borrar_detalle_venta(request, detalle_id):
    detalle = get_object_or_404(DetalleVenta, id=detalle_id)
    venta_id = detalle.venta.id
    
    if request.method == 'POST':
        # Restaurar stock antes de eliminar
        libro = detalle.libro
        libro.stock += detalle.cantidad
        libro.save()
        
        # Eliminar detalle
        detalle.delete()
        
        # Recalcular total de la venta
        detalle.venta.calcular_total()
        
        return redirect('ver_detalles_venta', venta_id=venta_id)
    
    return render(request, 'detalle_venta/borrar_detalle.html', {'detalle': detalle})