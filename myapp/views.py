from django.shortcuts import render
from .forms import BookForm  
from .models import Book
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q



@login_required(login_url="/book/login/")
def home(request):
    """Show a paginated list of books. Login required."""
    query = request.GET.get('q', '').strip()

    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        books = Book.objects.all()
    books.order_by('title')
    username = request.user.username
    books_paginator = Paginator(books, 10)
    page_number = request.GET.get("page")
    page_obj = books_paginator.get_page(page_number)
    return render(request, 'myapp/home.html', {'page_obj': page_obj, 'username': username, 'books': books, 'query': query})


class edit_book(LoginRequiredMixin, UpdateView):
    """Edit a book. Login required."""
    login_url = '/book/login/'
    model = Book
    fields = ["title", "author", "description"]
    template_name = "myapp/edit_book.html"
    success_url = reverse_lazy('home')


class create_book(LoginRequiredMixin, CreateView):
    """Create a new book. Login required."""
    login_url = '/book/login/'
    model = Book
    fields = ["title", "author", "description"]
    template_name = "myapp/create_book.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    


class delete_book(LoginRequiredMixin, DeleteView):
    """Delete a book. Login required."""
    login_url = '/book/login/'
    model = Book
    template_name = "myapp/delete_book.html"
    success_url = reverse_lazy('my_books')

    

def login_user(request):
    """Handle user login: display form and authenticate credentials."""
    if request.method == "GET":
        return render(request, 'myapp/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        context = {'username': username}
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "The email or password is invalid")
            return redirect('login')


@login_required(login_url="/book/login/")
def logout_user(request):
    """Log out the current user and redirect to home."""
    logout(request)
    return redirect('home')


def register(request):
    """Handle user registration: display form and create new users."""
    if request.method == "GET":
        return render(request, 'myapp/register.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        names = {'username': username, 'email': email, 'password': password1}
        errors = {}
        if User.objects.filter(username=username).exists():
            errors['username_error'] = 'This username already exists'
        
        if User.objects.filter(email=email).exists():
            errors['email_error'] = 'This e-mail already exists'

        if password1 != password2:
            errors['password_error'] = 'Both passwords must be equals'
        
        if errors:
            return render(request, 'myapp/register.html', context={**names, **errors})
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            return render(request, 'myapp/login.html')
        

class delete_user(LoginRequiredMixin, DeleteView):
    login_url = '/book/login/'
    model = User
    template_name = "home.html"
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user


@login_required(login_url="/book/login/")
def my_books(request):
    """Show a paginated list of your books. Login required."""
    query = request.GET.get('q', '').strip()

    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )
    
    else:
        books = Book.objects.filter(owner=request.user)
    books.order_by('title')
    username = request.user.username
    books_paginator = Paginator(books, 10)
    page_number = request.GET.get("page")
    page_obj = books_paginator.get_page(page_number)
    return render(request, 'myapp/mybooks.html', {'page_obj': page_obj, 'username': username, 'books': books, 'query': query})


class UserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=False,
        help_text='',        
    )
    password = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.PasswordInput
    
    )
    password2 = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        a = cleaned_data.get("password")
        b = cleaned_data.get("password2")
        c = cleaned_data.get("username")
        d = cleaned_data.get("email")
        if a or b:
            if a != b:
                self.add_error("password", "The both passwords must be equal")
                self.add_error("password2", "The both passwords must be equal")

        if User.objects.filter(username=c).exclude(pk=self.instance.pk).exists():
           self.add_error("username", "This username already exists")

        if User.objects.filter(email=d).exclude(pk=self.instance.pk).exists():
            self.add_error("email","This email already exists")

        return cleaned_data
    

    class Meta:
        model = User
        fields = ["username", "email"]


class my_user(LoginRequiredMixin, UpdateView):
    login_url = '/book/login/'
    model = User
    template_name = "myapp/myaccount.html"
    success_url = reverse_lazy('home')
    form_class = UserForm

    def form_valid(self, form):
        new_password = form.cleaned_data.get("password")
        if new_password:
            self.object.set_password(new_password)
        self.object.save()
        update_session_auth_hash(self.request, self.object)
        return super().form_valid(form)
    

    def get_object(self, queryset=None):
        return self.request.user
    


class detail_book(LoginRequiredMixin, DetailView):
    login_url = '/book/login/'
    model = Book
    template_name = "myapp/detail_book.html"
    context_object_name = 'book'

    



    
    



