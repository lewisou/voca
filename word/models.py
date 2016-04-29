from django.db import models
# from datetime import date, datetime, time
# from django.utils import timezone
from django.conf import settings

from datetime import datetime, timedelta
from pytz import timezone
import django.utils
import pytz
import os

from .downloader import download

MEMORY_CURVE_C = settings.MEMORY_CURVE_C
MEMORY_CURVE_END = settings.MEMORY_CURVE_END

class Word(models.Model):
	code = models.CharField(max_length=50, unique=True)
	word = models.CharField(max_length=50)
	pronounce_url = models.TextField()
	pronounce = models.CharField(max_length=50)
	explainatin = models.TextField()
	example = models.TextField()

	next_review_at = models.DateTimeField(default=django.utils.timezone.now)
	graduated = models.BooleanField(default=False)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def calculate_next_review_date(self):
		_c = self.review_set.count()
		delta = MEMORY_CURVE_C * _c * _c
		if delta <= MEMORY_CURVE_END + 1:
			start = self.review_set.order_by('-created_at').first().created_at
			self.next_review_at = start + timedelta(days=delta)
			return self.save()
		else:
			return None

	def downloadPronounceFile(self):
		download(self.pronounce_url, os.path.join("word", self.code + ".mp3"))

	def getDateTuple(self):
		return (self.next_review_at.year, self.next_review_at.month, self.next_review_at.day)

	def __str__(self):
		return self.word

class Review(models.Model):
	word = models.ForeignKey(Word, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.word.word + ' at '+ str(self.created_at)

