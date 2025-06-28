from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .services import BreadService
from .forms import BreadForm


# Create your views here.
def get_all_bread(request):
    """ return all bread from database """
    bread = BreadService.get_all_bread()
    return render(request, 'get_all_bread.html', {'bread': bread})