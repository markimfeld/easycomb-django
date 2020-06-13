from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.TextChoices):
    PREPARE = 'P', _('Preparar')
    READY = 'R', _('Listo')
    DELIVERED = 'D', _('Entregado')