from django.shortcuts import render
from .forms import DateForm


# Create your views here.
def index(request):
    form = DateForm(request.POST)
    return render(request, 'generator/index.html', {'form':form})
