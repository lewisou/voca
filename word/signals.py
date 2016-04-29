from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Word

@receiver(pre_save, sender=Word)
def gene_code(sender, instance, **kwargs):
	instance.code = instance.word.replace(" ", "").lower()

