from django.db import models
from django.dispatch import receiver

from .models import User


# TODO: add signals (maybe to other apps)
# @receiver(models.signals.post_save, sender=User)
# def _update_password(sender, instance, created, **kwargs):
#     if created:
#         instance.set_password(instance.password)
#         instance.save()
