from django.urls import path
from .views import edit_book, home, create_book, delete_book, register_user, login_user

urlpatterns = [
    path('', home, name='home'),
    path('book/edit/<int:pk>/', edit_book.as_view(), name="edit_book"),
    path('book/create/', create_book.as_view(), name="create_book"),
    path('book/delete/<int:pk>/', delete_book.as_view(), name="delete_book"),
    path('book/register/', register_user, name='register'),
    path('book/login/', login_user, name='login'),
]
