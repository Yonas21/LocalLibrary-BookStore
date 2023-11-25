from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.http import request, response
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def index(request):
    """View function for home page of site."""
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    filtered_book = Book.objects.filter(title__exact="the Art of War").count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()

    genre_fiction = Genre.objects.filter(name__exact="Fiction").count()

    num_authors = Author.objects.all().count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "filtered_book": filtered_book,
        "genre": genre_fiction,
        "num_visits": num_visits,
    }

    return render(request, "index.html", context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

    def get_queryset(self) -> QuerySet[Any]:
        return Book.objects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(BookListView, self).get_context_data(**kwargs)
        context["some_data"] = "Default Data"
        return context

    object_name = "book_list"

    queryset = Book.objects.filter(title__icontains="war")[:5]
    template_name = "books/book_list.html"


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = "/login/"
    redirect_field_name = "/books/"
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 3

    def get_queryset(self) -> QuerySet[Any]:
        return Author.objects.all()


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
