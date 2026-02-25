from django.shortcuts import render
from .forms import BookForm  
from .models import Book

def home(request):
    books = Book.objects.all()
    return render(request, 'myapp/home.html', {'books': books})

def register(request):
    form = BookForm() 
    return render(request, 'myapp/register.html', {'form': form})

