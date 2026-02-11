from django.shortcuts import render
from django.views import generic

from .models import Author, Book, BookInstance, Genre


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # TEST SEGUNDA SEMANA
    # All genres of books
    genres = Genre.objects.values_list('name', flat=True)

    # Genres and books with a specific word
    genres_word = 'Fiction'
    num_genres_word = Genre.objects.filter(name__icontains=genres_word).count()

    # PONER 'a' PARA LOS TESTS SEGUNDA SEMANA
    books_word = 'a'
    num_books_word = Book.objects.filter(title__icontains=books_word).count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'genres': genres,
        'genres_word': genres_word,
        'num_genres_word': num_genres_word,
        'books_word': books_word,
        'num_books_word': num_books_word,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
 

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book'

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author
    context_object_name = 'author'

