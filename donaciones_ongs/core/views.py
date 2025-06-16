
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ONGForm, DonanteForm, CampañaForm, DonacionForm
from .models import Campaña, Donacion, Donante
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden

# Página de inicio

def home(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    return render(request, 'core/mostrar_campañas.html')

def salir(request):
    logout(request)
    return redirect('home')

# Registro de ONGs
def registrar_ong(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        ong_form = ONGForm(request.POST)
        if user_form.is_valid() and ong_form.is_valid():
            # Crear usuario
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            # Crear ONG
            ong = ong_form.save(commit=False)
            ong.user = user
            ong.save()
            # Iniciar sesión automáticamente
            login(request, user)
            return redirect('mostrar_campañas')
    else:
        user_form = UserForm()
        ong_form = ONGForm()
    return render(request, 'core/registro_ong.html', {
        'user_form': user_form,
        'extra_form': ong_form
    })

# Registro de Donantes
def registrar_donante(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        donante_form = DonanteForm(request.POST)
        if user_form.is_valid() and donante_form.is_valid():
            # Crear usuario
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            # Crear Donante
            donante = donante_form.save(commit=False)
            donante.user = user
            donante.save()
            # Iniciar sesión automáticamente
            login(request, user)
            return redirect('mostrar_campañas')
    else:
        user_form = UserForm()
        donante_form = DonanteForm()
    return render(request, 'core/registro_donante.html', {
        'user_form': user_form,
        'extra_form': donante_form
    })

@login_required
def mostrar_campañas(request):
    campañas = Campaña.objects.all()
    return render(request, 'core/mostrar_campañas.html', {'campañas': campañas})


@login_required
def crear_campaña(request):
    if request.method == 'POST':
        form = CampañaForm(request.POST, user=request.user)
        if form.is_valid():
            campaña = form.save(commit=False)
            if hasattr(request.user, 'ong'):
                campaña.ong = request.user.ong
            campaña.save()
            return redirect('mostrar_campañas')
    else:
        form = CampañaForm(user=request.user)

    return render(request, 'core/crear_campaña.html', {'form': form})






@login_required
def crear_donacion(request):
    user = request.user

    if user.is_superuser:
        donante, _ = Donante.objects.get_or_create(user=user)
    else:
        donante = user.donante 
    if request.method == 'POST':
        form = DonacionForm(request.POST, initial={'donante': donante})
        if form.is_valid():
            donacion = form.save(commit=False)
            donacion.donante = donante
            donacion.save()
            donacion.campaña.monto_actual += donacion.monto
            donacion.campaña.save()
            return redirect('listar_donaciones')
    else:
        form = DonacionForm(initial={'donante': donante})

    return render(request, 'core/crear_donacion.html', {'form': form})

@login_required
def historial_donaciones(request):
    hoy = timezone.now().date()

    if request.user.is_superuser:
        donaciones = Donacion.objects.all()
    elif hasattr(request.user, 'ong'):
        donaciones = Donacion.objects.filter(
            campaña__ong=request.user.ong,
            campaña__fecha_fin__gte=hoy
        )
    elif hasattr(request.user, 'donante'):
        donaciones = Donacion.objects.filter(
            donante=request.user.donante,
            campaña__fecha_fin__gte=hoy
        )
    else:
        donaciones = Donacion.objects.none()

    return render(request, 'core/historial_donaciones.html', {'donaciones': donaciones})

def eliminar_donacion(request, id):
    donacion = get_object_or_404(Donacion, id=id)

    if request.method == 'POST':
        donacion.delete()
        return redirect('historial_donaciones')  

    return render(request, 'core/confirmar_eliminacion.html', {'objeto': donacion})


@login_required
def editar_campaña(request, campaña_id):
    campaña = get_object_or_404(Campaña, id=campaña_id)
    # Si no es superusuario y la campaña no pertenece a su ONG, denegar acceso
    if not request.user.is_superuser and campaña.ong != request.user.ong:
        return HttpResponseForbidden("No tienes permiso para editar esta campaña")

    if request.method == 'POST':
        form = CampañaForm(request.POST, instance=campaña)
        if form.is_valid():
            form.save()
            return redirect('mostrar_campañas')
    else:
        form = CampañaForm(instance=campaña)
        if not request.user.is_superuser:
            form.fields['ong'].disabled = True

    return render(request, 'core/editar_campaña.html', {'form': form, 'campaña': campaña})


@login_required
def eliminar_campaña(request, campaña_id):
    campaña = get_object_or_404(Campaña, id=campaña_id)

    if not request.user.is_superuser and campaña.ong != request.user.ong:
        return HttpResponseForbidden("No tienes permiso para eliminar esta campaña")

    if request.method == 'POST':
        campaña.delete()
        return redirect('mostrar_campañas')

    return render(request, 'core/confirmar_eliminar.html', {'campaña': campaña})



def es_ong(user):
    return hasattr(user, 'ong')

def es_donante(user):
    return hasattr(user, 'donante')

