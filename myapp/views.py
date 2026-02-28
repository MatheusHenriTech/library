from django.shortcuts import render
from .forms import BookForm  
from .models import Book
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator


def home(request):
    books = Book.objects.all()

    books_paginator = Paginator(books, 10)
    page_number = request.GET.get("page")
    page_obj = books_paginator.get_page(page_number)
    return render(request, 'myapp/home.html', {'page_obj': page_obj})


class edit_book(UpdateView):
    model = Book
    fields = ["title", "author", "description"]
    template_name = "myapp/edit_book.html"
    success_url = reverse_lazy('home')


class create_book(CreateView):
    model = Book
    fields = ["title", "author", "description"]
    template_name = "myapp/create_book.html"
    success_url = reverse_lazy('home')


class delete_book(DeleteView):
    model = Book
    template_name = "myapp/delete_book.html"
    success_url = reverse_lazy('home')