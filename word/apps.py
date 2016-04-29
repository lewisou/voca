from django.apps import AppConfig


class WordConfig(AppConfig):
	name = 'word'

	def ready(self):
		from . import signals