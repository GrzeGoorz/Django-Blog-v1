from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views import View
import json
from django.views.decorators.http import require_POST
from .models import Post

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


# ----------------------------------------------------------

from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer
from .forms import ItemForm

# ----------------------------------------------------------
# DLA WYKRESU:
from matplotlib import pyplot as plt
from io import BytesIO
import base64
import plotly.express as px
#-----------


# Widok dla strony domowej
def home(request):
    # Pobieranie wszystkich postów z bazy danych
    context = {
        'posts': Post.objects.all()
    }
    # Renderowanie strony domowej z listą postów
    return render(request,'blog/home.html', context)


# Widok dla strony "About"
def about(request):
     # Renderowanie strony "About" z tytułem
    return render(request,'blog/about.html', {'title': 'About'})


# Widok dla strony "Skrypty"
def skrypty(request):
    # Renderowanie strony z tytułem
    return render(request,'blog/skrypty.html', {'title': 'skrypty'})


# Klasa widoku listy postów
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 4


# Klasa widoku listy postów użytkownika
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 4
    
# Pobierz posty dla danego użytkownika
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# Klasa widoku szczegółowego posta
class PostDetailView(DetailView):
    model = Post



# Klasa widoku tworzenia nowego posta
# - Klasa PostCreateView dziedziczy zarówno po LoginRequiredMixin (zabezpieczenie przed niezalogowanymi użytkownikami),
#   jak i po CreateView (widok generyczny do tworzenia obiektów).
# - Używa modelu Post, który jest modelem używanym do przechowywania informacji o postach na stronie.
# - Określa pola formularza, które mają być uwzględnione w formularzu do tworzenia posta (tytuł i treść).
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']  # Pola formularza do tworzenia posta
 # Metoda wywoływana po poprawnej walidacji formularza
 # - Metoda form_valid() jest wywoływana, gdy formularz jest poprawnie zwalidowany.
# - W tym przypadku, przypisuje autora posta do aktualnie zalogowanego użytkownika przed zapisaniem obiektu.
# - Super().form_valid(form) wywołuje form_valid() z klasy nadrzędnej (CreateView), co pozwala na
#   standardowe zachowanie widoku generycznego do tworzenia obiektów.
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)





# Klasa widoku aktualizacji posta
#   UserPassesTestMixin (zabezpieczenie przed użytkownikami bez uprawnień) oraz DeleteView (widok generyczny do usuwania obiektów).
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content'] # Pola formularza do aktualizacji posta
# Metoda wywoływana po poprawnej walidacji formularza
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
# - Metoda testująca, czy użytkownik ma uprawnienia do aktualizacji posta.
# - Sprawdza, czy aktualnie zalogowany użytkownik jest autorem posta.
# - Jeśli tak, zwraca True, co oznacza, że użytkownik ma uprawnienia do aktualizacji posta.
# - W przeciwnym razie zwraca False, co uniemożliwia użytkownikowi aktualizację posta.
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



# Klasa widoku usuwania posta
#   UserPassesTestMixin (zabezpieczenie przed użytkownikami bez uprawnień) oraz DeleteView (widok generyczny do usuwania obiektów).
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'  # Po usunięciu posta, przekieruj na stronę domową
 # Metoda testująca, czy użytkownik ma uprawnienia do usunięcia posta
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    # Funkcja widoku dla strony "About"
    def about(request):
        # Renderowanie strony "About" z tytułem
        return render(request, 'blog/about.html', {'title': 'About'})




##### DLA MODUŁU PRACE_IT_HTML
class WymianaUrządzeniaView(View):
    template_name = 'blog/prace_it.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        data_wymiany = request.POST.get('data_wymiany')
        ilosc_wymienionych = int(request.POST.get('ilosc_wymienionych'))

        # Tutaj zapisz dane do modelu
        # ...

        response_data = {
            'success': True,
            'message': 'Dane zapisane pomyślnie.'
        }
        return JsonResponse(response_data)
    
# ----------------------------------------------------------
# ----------------------------------------------------------
# ----------------------------------------------------------
def prace_view(request):
    
    dane = {}
    labels = list(dane.keys())
    data = list(dane.values())
    return render(request, 'blog/prace_it.html', {'labels': labels, 'data': data})



# ----------------------------------------------------------
# ----------------------------------------------------------
# ----------------------------------------------------------
# LISTA PRZEDMIOTÓW:

def item_list(request):
    items = Item.objects.all()
    return render(request, 'blog/item_list.html', {'items': items})

def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'blog/item_form.html', {'form': form})

def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'blog/item_form.html', {'form': form})

def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'blog/item_confirm_delete.html', {'item': item})

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer



# ---------- WYKRES - LISTA PRZEDMIOTÓW:
def generate_pie_chart():
    # Dane dla wykresu kołowego
    items = Item.objects.all()
    product_names = [item.product_name for item in items]
    quantities = [item.quantity for item in items]

    # Utwórz interaktywny wykres kołowy za pomocą Plotly
    fig = px.pie(names=product_names, values=quantities, title='PRODUKTY I ILOŚĆ W PROCENTACH')

    # Zwiększ rozmiar czcionki
    fig.update_layout(
        font=dict(size=52), 
        width=1600,  
        height=1200, 
    )

    # Zapisz wykres do formatu obrazu
    image_stream = BytesIO()
    fig.write_image(image_stream, format='png')
    image_stream.seek(0)
    image_data = base64.b64encode(image_stream.read()).decode('utf-8')

    return {
        'chart_image': f"data:image/png;base64,{image_data}",
        'items': items,
    }

def item_list(request):
    chart_data = generate_pie_chart()

    context = {
        'chart_image': chart_data['chart_image'],
        'items': chart_data['items'],  # Przekaż dane produktów do szablonu
    }

    return render(request, 'blog/item_list.html', context)
