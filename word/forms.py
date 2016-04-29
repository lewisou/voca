from django.forms import ModelForm
from word.models import Word

class AddWordForm(ModelForm):
	class Meta:
		model = Word
		fields = ['word', 'pronounce', 'pronounce_url', 'explainatin', 'example']

