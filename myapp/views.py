from django.shortcuts import render
from .forms import BookForm  
from .models import Book
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages



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
            messages.error(request, "The email or password is invalid")
            return redirect('login')


@login_required(login_url="/book/login/")
def logout_user(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == "GET":
        return redirect('register')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        username_exist = User.objects.filter(username=username).exists()
        email_exist = User.objects.filter(email=email).exists()

        if username_exist:
            messages.error(request, "This username already exists", extra_tags="username_alert")
            return redirect('register')
        
        elif email_exist:
            messages.error(request, "This e-mail already exists", extra_tags="email_alert")
            return redirect('register')

        elif password1 != password2:
            messages.error(request, "The password one is different of password2", extra_tags="password_alert")
            return redirect('register')
        else:
            new_user = User.objects.create_user(username=username, email=email, password=password1)
            new_user.save()
            return redirect('login')
