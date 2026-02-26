from django.shortcuts import render
from .forms import BookForm  
from .models import Book
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy


def home(request):
    books = Book.objects.all()
    return render(request, 'myapp/home.html', {'books': books})


class edit_book(UpdateView):
    model = Book
    fields = ["title", "description", "author"]
    template_name = "myapp/edit_book.html"
    success_url = reverse_lazy('home')


class create_book(CreateView):
    model = Book
    fields = ["title", "author", "description"]
    template_name = "myapp/create_book.html"
    success_url = reverse_lazy('home')