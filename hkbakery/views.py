from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .services import BreadService
from .forms import BreadForm
from .models import Bread


# Create your views here.
def get_all_bread(request):
    
    if request.method == 'POST':
        form = BreadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = BreadForm()
        """ return all bread from database """
        bread = BreadService.get_all_bread()
        return render(request, 'get_all_bread.html', {'bread': bread, 'form': form})


def edit_bread(request, bread_id):

    bread = get_object_or_404(Bread, id=bread_id)

    if request.method == 'POST':
        form = BreadForm(request.POST, instance=bread)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = BreadForm(instance=bread)
        return render(request, 'edit_bread.html', {'bread': bread, 'form': form})


# take id of bread item and delete from db
def delete_bread(request, bread_id):

    item = get_object_or_404(Bread, id=bread_id)
    if (request.method == 'POST'):
        item.delete()
        return redirect('/')
    return redirect('/')
