from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, RegisterForm
from .models import CarritoItem, Seleccion


def home(request):
    q = request.GET.get('q', '').strip()
    login_form = LoginForm(request, data=request.POST if request.POST.get('action') == 'login' else None, prefix='login')
    register_form = RegisterForm(request.POST if request.POST.get('action') == 'register' else None, prefix='register')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'login' and login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home')
        if action == 'register' and register_form.is_valid():
            user = register_form.save(commit=False)
            user.set_password(register_form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Registro completado. Bienvenido.')
            return redirect('home')

    selecciones = Seleccion.objects.all()
    if q:
        selecciones = selecciones.filter(
            Q(nombre__icontains=q) | Q(descripcion__icontains=q)
        )

    items = []
    total = 0
    if request.user.is_authenticated:
        items = CarritoItem.objects.filter(usuario=request.user)
        total = sum(item.subtotal() for item in items)

    return render(request, 'shop/home.html', {
        'selecciones': selecciones,
        'q': q,
        'login_form': login_form,
        'register_form': register_form,
        'cart_items': items,
        'cart_total': total,
    })


def user_login(request):
    return redirect('home')


def user_logout(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'shop/register.html', {'form': form})


@login_required
def carrito(request):
    items = CarritoItem.objects.filter(usuario=request.user)
    total = sum(item.subtotal() for item in items)
    return render(request, 'shop/carrito.html', {
        'items': items,
        'total': total,
    })


@login_required
def agregar_carrito(request, seleccion_id):
    seleccion = get_object_or_404(Seleccion, id=seleccion_id)
    item, created = CarritoItem.objects.get_or_create(usuario=request.user, seleccion=seleccion)
    if not created:
        item.cantidad += 1
        item.save()
    messages.success(request, f'Agregaste {seleccion.nombre} al carrito.')
    return redirect('home')


@login_required
def eliminar_item(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, usuario=request.user)
    item.delete()
    messages.success(request, 'Item eliminado del carrito.')
    return redirect('carrito')
