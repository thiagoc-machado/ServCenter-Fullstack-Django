from django.shortcuts import render, redirect
from .forms import ConfigForm
from .models import Config
from django.contrib.auth.decorators import user_passes_test
from finance.models import Categoria_in, Categoria_out

@user_passes_test(lambda u: u.is_superuser)
def config(request):
    categoriaIn = Categoria_in.objects.all()
    categoriaOut = Categoria_out.objects.all()
    configs = Config.objects.all()
    return render(request, 'config.html', {'configs': configs, 'categorias_in': categoriaIn, 'categorias_out': categoriaOut})


@user_passes_test(lambda u: u.is_superuser)
def new_config(request):
    form = ConfigForm()
    if request.method == 'POST':
        form = ConfigForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return render(request, 'new_config.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def edit_config(request):
    config = Config.objects.get(pk=2)
    form = ConfigForm(instance=config)
    if request.method == 'POST':
        form = ConfigForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
    return render(request, 'edit_config.html', {'form': form})

def categoria_in(request):
    if request.method == 'POST':
        if request.POST.get('categoriasIn') != '':
            categoria = request.POST.get('categoriasIn')
            cat = Categoria_in(categoria=categoria)
            cat.save()
            return redirect('config')
        
def del_categoria_in(request, id):
    categoria = Categoria_in.objects.get(pk=id)
    categoria.delete()
    return redirect('config')
    

def categoria_out(request):
    if request.method == 'POST':
        if request.POST.get('categoriasOut') != '':
            categoria = request.POST.get('categoriasOut')
            cat = Categoria_out(categoria=categoria)
            cat.save()
            return redirect('config')

def del_categoria_out(request, id):
    categoria = Categoria_out.objects.get(pk=id)
    categoria.delete()
    return redirect('config')
    
    

    

