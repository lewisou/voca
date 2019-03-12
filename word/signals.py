from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Word

@receiver(pre_save, sender=Word)
def gene_code(sender, instance, **kwargs):
	if not instance.code:
		instance.code = instance.word.replace(" ", "").replace("/", "-").lower()


