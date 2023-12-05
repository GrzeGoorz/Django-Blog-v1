from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

# ready() jest wywoływane, gdy aplikacja Django jest gotowa do użycia.
        # W tym przypadku, importujemy moduł signals z aplikacji users.
    def ready(self):
        import users.signals