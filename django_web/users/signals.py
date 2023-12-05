from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


# Sygnał post_save oznacza, że te funkcje będą uruchamiane automatycznie po zapisaniu obiektu.
# Receiver dla tworzenia profilu użytkownika po zapisaniu obiektu użytkownika.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Tworzy nowy profil dla użytkownika, gdy obiekt użytkownika zostanie zapisany po raz pierwszy.
       Argumenty:
    - sender: Klasa modelu, która wysłała sygnał (User).
    - instance: Konkretny obiekt modelu, który został właśnie zapisany (User).
    - created: Wartość logiczna, czy obiekt został utworzony (True) czy zaktualizowany (False).
    - **kwargs: Dodatkowe, nazwane argumenty, które mogą być przekazane w ramach sygnału.
    """
    
    if created:
        Profile.objects.create(user=instance)

# Receiver dla zapisywania profilu użytkownika po zapisaniu obiektu użytkownika.
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Zapisuje profil użytkownika po każdym zapisaniu obiektu użytkownika.
    - sender: Klasa modelu, która wysłała sygnał (User).
    - instance: Konkretny obiekt modelu, który został właśnie zapisany (User).
    - **kwargs: Dodatkowe, nazwane argumenty, które mogą być przekazane w ramach sygnału.
    """
    instance.profile.save()