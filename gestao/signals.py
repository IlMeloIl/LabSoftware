from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import AtividadeSistema, User

@receiver(user_logged_in)
def registrar_login(sender, request, user, **kwargs):
    if isinstance(user, User):
        AtividadeSistema.objects.create(
            usuario=user,
            acao='LOGIN',
            descricao=f"Usuário '{user.username}' realizou login.",
        )

@receiver(user_logged_out)
def registrar_logout(sender, request, user, **kwargs):
    if user and isinstance(user, User):
        AtividadeSistema.objects.create(
            usuario=user,
            acao='LOGOUT',
            descricao=f"Usuário '{user.username}' realizou logout."
        )