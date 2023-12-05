from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        # Jeśli żądanie jest typu POST (np. formularz został przesłany)
        #form = UserCreationForm(request.POST)

        # Dziedziczenie formularza po UserRegisterForm - jest w pliku forms.py (Dodaj dodatkowe pole email do formularza)
        form = UserRegisterForm(request.POST)
        
        
        # Sprawdź, czy przesłane dane formularza są poprawne
        if form.is_valid():
            # Jeśli dane są poprawne, zapisz nowego użytkownika
            form.save()
            
            # Pobierz nazwę użytkownika z danych formularza
            username = form.cleaned_data.get('username')
            
            # Wyślij komunikat o sukcesie do użytkownika
            messages.success(request, f'Account created for {username}!')
            
            # Przekieruj użytkownika na stronę o nazwie 'DPM'
            return redirect('DPM')
    else:
        # Jeśli żądanie nie jest typu POST (np. pierwsze wejście na stronę rejestracji)
        # Utwórz pusty formularz rejestracji
        #form = UserCreationForm()
        form = UserRegisterForm()
    
    # Renderuj szablon rejestracji, przekazując formularz do szablonu
    return render(request, 'users/register.html', {'form': form})


# Dekorator @login_required sprawdza, czy użytkownik jest zalogowany.
# Jeśli nie, przekierowuje go do strony logowania przed wykonaniem widoku.
@login_required
def profile(request):
    # Sprawdzenie, czy żądanie przesłane do widoku jest metodą POST.
    if request.method == 'POST':
        # Utworzenie formularza aktualizacji użytkownika, przekazując dane z żądania (request.POST)
        # i ustawienie instancji formularza na aktualnie zalogowanego użytkownika.
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # Utworzenie formularza aktualizacji profilu, przekazując dane z żądania (request.POST)
        # oraz przekazanie danych plików (request.FILES), a także ustawienie instancji formularza na profilu aktualnego użytkownika.
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        
        # Utworzenie formularza aktualizacji profilu, przekazując dane z żądania (request.POST)
        # oraz przekazanie danych plików (request.FILES), a także ustawienie instancji formularza na profilu aktualnego użytkownika.
        # Sprawdzenie, czy oba formularze są poprawne (walidacja).
        if u_form.is_valid() and p_form.is_valid():
            # Zapisanie danych użytkownika i profilu, jeśli oba formularze są poprawne.
            u_form.save()
            p_form.save()
            # Wyświetlenie komunikatu o sukcesie, który będzie dostępny w kontekście szablonu.
            messages.success(request, f'Your account has been updated!')
             # Przekierowanie użytkownika na stronę profilu.
            return redirect('profile')

 # Jeśli żądanie nie jest metodą POST, utworzenie pustych formularzy z aktualnymi danymi użytkownika.
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
 
 #Utworzenie kontekstu zawierającego formularze, które będą dostępne w szablonie.
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

 # Wyrenderowanie szablonu 'users/profile.html' z przekazanym kontekstem.
    return render(request, 'users/profile.html', context)