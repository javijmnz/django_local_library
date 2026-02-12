from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views import generic

from .models import Author, Book, BookInstance, Genre


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # TEST SEGUNDA SEMANA
    # All genres of books
    genres = Genre.objects.values_list("name", flat=True)

    # Genres and books with a specific word
    genres_word = "Fiction"
    num_genres_word = Genre.objects.filter(name__icontains=genres_word).count()

    # PONER 'a' PARA LOS TESTS SEGUNDA SEMANA
    books_word = "a"
    num_books_word = Book.objects.filter(title__icontains=books_word).count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get("num_visits", 0)
    num_visits += 1
    request.session["num_visits"] = num_visits

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "genres": genres,
        "genres_word": genres_word,
        "num_genres_word": num_genres_word,
        "books_word": books_word,
        "num_books_word": num_books_word,
        "num_visits": num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "index.html", context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = "book_list"
    paginate_by = 2


class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = "book"


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = "author_list"
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author
    context_object_name = "author"


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""

    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )


class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-basaed view listing all books on loan."""

    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed.html"
    paginate_by = 10

    permission_required = "catalog.can_mark_returned"

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact="o").order_by("due_back")
