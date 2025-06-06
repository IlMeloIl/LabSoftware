from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import AtividadeSistema, User, Fornecedor

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

@receiver(pre_save, sender=Fornecedor)
def store_old_fornecedor_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_ativo = Fornecedor.objects.get(pk=instance.pk).ativo
        except Fornecedor.DoesNotExist:
            instance._old_ativo = None

@receiver(post_save, sender=Fornecedor)
def atualizar_status_produtos_do_fornecedor(sender, instance, created, **kwargs):   
    if not created and hasattr(instance, '_old_ativo') and instance._old_ativo is not None:
        if instance._old_ativo and not instance.ativo:
            instance.produtos.filter(ativo=True).update(ativo=False)
        elif not instance._old_ativo and instance.ativo:
            instance.produtos.filter(ativo=False).update(ativo=True)