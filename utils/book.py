from myapp.models import Book

def create_books(n):
    for i in range(1, n+1):
        Book.objects.create(
            title=f'Book {i}',
            author=f'Author {i}',
            description=f'Description {i}'
        )

    