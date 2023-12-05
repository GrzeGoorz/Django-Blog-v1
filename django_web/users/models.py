from django.db import models
from PIL import Image
from django.contrib.auth.models import User

 # Model Profile reprezentuje dodatkowe informacje o użytkowniku.
    # Jest powiązany z modelem User w relacji jeden do jednego.
    # Klauzula on_delete=models.CASCADE oznacza, że gdy użytkownik zostanie usunięty,
    # jego profil również zostanie usunięty.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

     # Pole image przechowuje obraz profilowy użytkownika.
    # Domyślny obraz to 'default.jpg', a nowe obrazy są przesyłane do folderu 'profile_pics'.
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        # Metoda reprezentacji obiektu jako ciąg tekstowy.
    # Zwraca nazwę użytkownika połączoną ze słowem "Profile".
        return f'{self.user.username} Profile'

# Metoda zapisu obiektu modelu UserProfile.
    def save(self, *args, **kwargs):
        # Wywołanie oryginalnej metody save() z klasy nadrzędnej (Model),
    # aby zachować standardowy proces zapisywania obiektu modelu.
        super().save(*args, **kwargs)

 # Otwarcie obrazu profilowego przy użyciu biblioteki Pillow (Image.open).
        img = Image.open(self.image.path)

# Sprawdzenie, czy wymiary obrazu przekraczają 300x300 pikseli.
        if img.height > 300 or img.width > 300:
            # Jeżeli tak, przeskalowanie obrazu do rozmiaru 300x300 pikseli.
            output_size = (300, 300)
            img.thumbnail(output_size)
            # Zapisanie przeskalowanego obrazu na dysku.
            img.save(self.image.path)