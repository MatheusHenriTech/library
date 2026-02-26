from django.urls import path
from .views import edit_book, home, create_book

urlpatterns = [
    path('', home, name='home'),
    path('book/edit/<int:pk>/', edit_book.as_view(), name="edit_book"),
    path('book/create/', create_book.as_view(), name="create_book"),
]
