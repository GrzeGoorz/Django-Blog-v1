from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse



# Model Post reprezentujący posty na blogu
class Post(models.Model):
     # Pole tytułu posta o maksymalnej długości 100 znaków
    title = models.CharField(max_length=100)
     # Pole treści posta, obsługujące dłuższe teksty
    content = models.TextField()
    # Pole daty publikacji posta, domyślnie ustawiane na aktualny czas
    date_posted = models.DateTimeField(default=timezone.now)
     # Pole autora posta, korzystające z relacji ForeignKey do modelu User
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # Metoda zwracająca reprezentację tekstową obiektu Post
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
     

     # Metoda reverse tworzy URL na podstawie nazwy widoku ('post-detail') i argumentów przekazanych jako kwargs.
    # W tym przypadku, używamy 'post-detail' jako nazwy widoku do wygenerowania URL.
    # Argument 'kwargs={'pk': self.pk}' określa, że przekazujemy parametr 'pk' (klucz główny) z wartością self.pk.
    # self.pk to identyfikator główny (primary key) obiektu Post, co pozwala na unikalne zidentyfikowanie konkretnego posta.
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    

    # ----------------------------------------------------------
    # ----------------------------------------------------------
    # ----------------------------------------------------------


class Item(models.Model):
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    location_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product_name} - {self.quantity} - {self.location_name}"