from django.shortcuts import render
from .forms import BookForm  
from .models import Book
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required(login_url="/book/login/")
def home(request):
    books = Book.objects.all()

    books_paginator = Paginator(books, 10)
    page_number = request.GET.get("page")
    page_obj = books_paginator.get_page(page_number)
    return render(request, 'myapp/home.html', {'page_obj': page_obj})


class edit_book(LoginRequiredMixin, UpdateView):
    login_url = '/book/login/'
    model = Book
    fields = ["title", "author", "description"]
    template_name = "myapp/edit_book.html"
    success_url = reverse_lazy('home')


class create_book(LoginRequiredMixin, CreateView):
    login_url = '/book/login/'
    model = Book
    fields = ["title", "author", "description"]
    template_name = "myapp/create_book.html"
    success_url = reverse_lazy('home')


class delete_book(LoginRequiredMixin, DeleteView):
    login_url = '/book/login/'
    model = Book
    template_name = "myapp/delete_book.html"
    success_url = reverse_lazy('home')


def register_user(request):
    if request.method == "GET":
        return render(request, 'myapp/register.html')

    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.filter(username=username).first()
    
        if user:
            return HttpResponse('This user already exists')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        return HttpResponse('usuário cadastrado')
    

def login_user(request):
    if request.method == "GET":
        return render(request, 'myapp/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('The email or password is invalid')
