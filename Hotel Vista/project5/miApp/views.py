from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone




def registrarse(request):
    if request.method == 'GET':
        return render(request, 'registrarse.html', {'form': UserCreationForm()})
    else:
        # Verifica que las contraseñas coincidan
        if request.POST["password1"] == request.POST["password2"]:
            try:
                # Crear usuario con username, first_name y last_name
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                    first_name=request.POST["first_name"],  # Guardar primer nombre
                    last_name=request.POST["last_name"]     # Guardar apellido
                )
                user.save()  # Guardar usuario en la base de datos
                login(request, user)  # Loguear al usuario automáticamente
                return redirect('index')  # Redirigir al índice o a otra página
            except IntegrityError:
                # Capturar error de nombre de usuario duplicado
                return render(request, 'registrarse.html', {
                    "form": UserCreationForm(), 
                    "error": "El nombre de usuario ya existe."
                })
        else:
            # Error si las contraseñas no coinciden
            return render(request, 'registrarse.html', {
                "form": UserCreationForm(), 
                "error": "Las contraseñas no coinciden."
            })
        




@login_required
def signout(request):
    logout(request)
    return redirect('index')



   
def inicio_sesionjg(request):
    if request.method == 'GET':
        return render(request, 'inicio_sesionjg.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'inicio_sesionjg.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('index')
    
def micuenta(request):
    user = request.user  # Obtener el usuario actual

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)  # Pasar el usuario actual al formulario
        if form.is_valid():
            # Actualizar el correo electrónico solo si se proporciona en el formulario
            if 'email' in form.cleaned_data:
                user.email = form.cleaned_data['email']
                user.save()  # Guardar los cambios en el usuario
            return redirect(to="index")
    else:
        form = CustomUserChangeForm(instance=user)  # Pasar el usuario actual al formulario en caso de GET request
    
    return render(request, 'micuenta.html', {'form': form, 'user': user})





def informes_creados(request):
    informes_creados = informe.objects.all()
    return render(request, 'informes_creados.html', {"informes_creados": informes_creados})



def aboutus(request):
      aboutus = habitacion.objects.all() 
      return render(request, 'aboutus.html', {'aboutus': aboutus})

def habitaciones(request):
    today = timezone.now().date()
    habitaciones_list = habitacion.objects.all()

    for hab in habitaciones_list:
        # Obtener todas las reservas de la habitación
        reservas = reserva.objects.filter(habitacion=hab)

        # Marcar como reservada si hay reservas que incluyen la fecha de hoy
        hab.reservada_hoy = any(
            res.fecha_inicio <= today <= res.fecha_fin for res in reservas
        )

    return render(request, 'habitaciones.html', {'habitaciones': habitaciones_list, 'today': today})

def contacto(request):
      contacto = habitacion.objects.all()
      return render(request, 'contacto.html', {'contacto': contacto})







def index(request):
    return render(request, 'index.html')






def recuperarcontra(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Si el usuario y el correo electrónico son correctos, redireccionar a la página de cambio de contraseña
                return redirect('cambiar_contra', user_id=user.id)
            except User.DoesNotExist:
                # Si el usuario o el correo electrónico no son correctos, se muestra un mensaje de error
                messages.error(request, "El usuario o correo electrónico no son correctos.")
    else:
        form = PasswordResetForm()
    
    return render(request, 'recuperarcontra.html', {'form': form})

def cambiar_contra(request, user_id):
    user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            messages.success(request, "Contraseña cambiada correctamente. Ahora puedes iniciar sesión.")
            return redirect('index')  # Redireccionar al usuario a la página de inicio
    else:
        form = ChangePasswordForm()
    
    return render(request, 'cambiar_contra.html', {'form': form})

def reservacion(request):
    context = {"carro":request.session.get("carro", [])}
    user = request.user
    return render(request, 'miApp/reservacion.html',  context)

def dropitem(request, codigo):
    carro = request.session.get("carro", [])
    nuevo_carro = []  # Crear una nueva lista para almacenar los elementos que quedan

    for item in carro:
        if item[0] == codigo:
            # Si el ítem que se quiere eliminar es encontrado
            if item[4] > 1:
                # Reducir la cantidad y recalcular el subtotal
                item[4] -= 1
                item[5] = item[3] * item[4]
                nuevo_carro.append(item)  # Agregar el item modificado
            # No agregar el item si es que se elimina completamente
        else:
            nuevo_carro.append(item)  # Agregar ítems que no se están eliminando

    request.session["carro"] = nuevo_carro
    return redirect(to="reservacion")

def addtocar(request, codigo):
    producto = habitacion.objects.get(codigo=codigo)
    carro = request.session.get("carro", [])

    tipo_vista_mapping = {
        1: 'accion',
        2: 'habitaciones',
        3: 'contacto',
        4: 'aboutus',
    }

    if request.method == 'POST':
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        fecha_inicio = timezone.datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        fecha_fin = timezone.datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        
        # Verificar si hay una reserva existente para el rango de fechas
        if reserva.objects.filter(
            habitacion=producto,
            fecha_inicio__lt=fecha_fin,
            fecha_fin__gt=fecha_inicio
        ).exists():
            messages.error(request, 'Ya existe una reserva para estas fechas.')
            return redirect('habitaciones')
        
        # Calcular la duración de la estancia
        num_dias = (fecha_fin - fecha_inicio).days
        total_precio = num_dias * producto.precio

        

        # Agregar al carro
        carro.append([codigo, producto.detalle, producto.imagen, producto.precio, num_dias, total_precio])
        request.session["carro"] = carro
        
        if producto.tipo in tipo_vista_mapping:
            return redirect(to=tipo_vista_mapping[producto.tipo])

    return redirect('habitaciones')


def agendar(request):
    if request.method == 'POST':
        carro = request.session.get("carro", [])
        today = timezone.now().date()

        for item in carro:
            codigo = item[0]
            producto = habitacion.objects.get(codigo=codigo)

            # Obtener las fechas de inicio y fin desde el formulario
            fecha_inicio = request.POST.get(f'fecha_inicio_{codigo}')
            fecha_fin = request.POST.get(f'fecha_fin_{codigo}')

            # Validar que las fechas no sean nulas
            if fecha_inicio and fecha_fin:
                fecha_inicio = timezone.datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
                fecha_fin = timezone.datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            else:
                messages.error(request, f'Las fechas para la habitación {producto.detalle} son obligatorias.')
                return redirect('reservacion')

            # Validar las fechas antes de crear la reserva
            if fecha_fin <= fecha_inicio:
                messages.error(request, 'La fecha de fin debe ser posterior a la fecha de inicio.')
                return redirect('reservacion')

            # Verificar si hay una reserva existente para el rango de fechas
            if reserva.objects.filter(
                habitacion=producto,
                fecha_inicio__lt=fecha_fin,
                fecha_fin__gt=fecha_inicio
            ).exists():
                messages.error(request, f'Ya existe una reserva para la habitación {producto.detalle} en esas fechas.')
                return redirect('reservacion')

            # Crear una nueva reserva
            nueva_reserva = reserva(habitacion=producto, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
            nueva_reserva.save()

            carro.remove(item)

        # Actualizar el carro en la sesión
        request.session["carro"] = carro

        messages.success(request, 'Reserva Exitosa. Te enviamos un comprobante a tu correo.')
        return redirect('reservacion')

    return redirect('reservacion')