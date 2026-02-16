from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from catalog.models import Author, Book, BookInstance, Genre, Language
from catalog.tests.test_views import User


# Extra tests for models.py
class ModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        genre = Genre.objects.create(name="Test Genre")
        book = Book.objects.create(
            title="Test Book",
            summary="Test Summary",
            isbn="1234567890123",
        )

        book.genre.add(genre)
        book.save()

        BookInstance.objects.create(
            book=book,
            imprint="Test Imprint",
            status="a",
        )

        Language.objects.create(name="Test Language")

    def test_genre_get_absolute_url(self):
        genre = Genre.objects.first()
        self.assertEqual(genre.get_absolute_url(), "/catalog/genre/" + str(genre.id))

    def test_book_display_genre(self):
        genre = Genre.objects.first()
        book = Book.objects.first()
        self.assertEqual(book.display_genre(), genre.name)

    def test_bookinstance_str(self):
        book_instance = BookInstance.objects.first()
        expected_str = f"{book_instance.id} ({book_instance.book.title})"
        self.assertEqual(str(book_instance), expected_str)

    def test_language_get_absolute_url(self):
        language = Language.objects.first()
        self.assertEqual(
            language.get_absolute_url(), "/catalog/language/" + str(language.id)
        )


class ViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="testuser", password="testpassword")
        Author.objects.create(first_name="Big", last_name="Bob")
        Book.objects.create(
            title="Test Book",
            summary="Test Summary",
            isbn="1234567890123",
        )

        content_typeAuthor = ContentType.objects.get_for_model(Author)
        permDeleteAuthor = Permission.objects.get(
            codename="delete_author",
            content_type=content_typeAuthor,
        )

        content_typeBook = ContentType.objects.get_for_model(Book)
        permDeleteBook = Permission.objects.get(
            codename="delete_book",
            content_type=content_typeBook,
        )

        user.user_permissions.add(permDeleteAuthor)
        user.user_permissions.add(permDeleteBook)

    def test_author_delete_form_valid(self):
        login = self.client.login(username="testuser", password="testpassword")
        author = Author.objects.first()
        response = self.client.post(f"/catalog/author/{author.id}/delete/")
        self.assertRedirects(response, "/catalog/authors/")
        self.assertFalse(Author.objects.filter(id=author.id).exists())

    def test_book_delete_form_valid(self):
        login = self.client.login(username="testuser", password="testpassword")
        book = Book.objects.first()
        response = self.client.post(f"/catalog/book/{book.id}/delete/")
        self.assertRedirects(response, "/catalog/books/")
        self.assertFalse(Book.objects.filter(id=book.id).exists())
