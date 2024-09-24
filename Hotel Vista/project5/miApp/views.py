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
    habitaciones = habitacion.objects.all()
    return render(request, 'habitaciones.html', {'habitaciones': habitaciones})

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