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

SETTING_TIME_ZONE = timezone(settings.TIME_ZONE)
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
		_c = self.review_set.filter(good=True).count()
		delta = MEMORY_CURVE_C * _c * _c
		if delta <= MEMORY_CURVE_END + 1:
			start = self.review_set.order_by('-created_at').first().created_at
			self.next_review_at = start + timedelta(days=delta)
			return self.save()
		else:
			self.graduated = True
			self.save()
			return None

	def downloadPronounceFile(self):
		download(self.pronounce_url, os.path.join("word", self.code + ".mp3"))

	def getDateTuple(self):
		date = self.next_review_at.astimezone(SETTING_TIME_ZONE)
		return (date.year, date.month, date.day)

	def markLastReviewAsBad(self):
		review = self.review_set.order_by('-created_at').first()
		if review != None and review.good:
			review.good = False
			review.save()
			return True
		return False

	def alreadyMarkedBad(self):
		review = self.review_set.order_by('-created_at').first()
		return not review.good

	def goodReviewCount(self):
		return self.review_set.filter(good=True).count()

	def __str__(self):
		return self.word

class Review(models.Model):
	word = models.ForeignKey(Word, on_delete=models.CASCADE)
	good = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.word.word + ' at '+ str(self.created_at)

