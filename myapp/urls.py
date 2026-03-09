from django.urls import path
from .views import edit_book, home, create_book, delete_book, login_user, logout_user, register, delete_user

urlpatterns = [
    path('', home, name='home'),
    path('book/edit/<int:pk>/', edit_book.as_view(), name="edit_book"),
    path('book/create/', create_book.as_view(), name="create_book"),
    path('book/delete/<int:pk>/', delete_book.as_view(), name="delete_book"),
    path('book/register/', register, name='register'),
    path('book/login/', login_user, name='login'),
    path('book/logout/', logout_user, name='logout'),
    path('book/deleteuser/', delete_user.as_view(), name="deleteuser"),
]
