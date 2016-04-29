from django.db.models import Count
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.conf import settings

from datetime import datetime, timedelta
from pytz import timezone
import pytz
import os

from .forms import AddWordForm
from .models import Word

SETTING_TIME_ZONE = timezone(settings.TIME_ZONE)

def _get_next_day_midnight():
	now = datetime.now()
	midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
	midnight = SETTING_TIME_ZONE.localize(midnight) + timedelta(days=1)
	return midnight

def _get_next_midnight(year, month, day):
	now = datetime.now()
	midnight = now.replace(year=year, month=month, day=day, hour=0, minute=0, second=0, microsecond=0)
	midnight = SETTING_TIME_ZONE.localize(midnight) + timedelta(days=1)
	return midnight

def _get_midnight(year, month, day):
	now = datetime.now()
	midnight = now.replace(year=year, month=month, day=day, hour=0, minute=0, second=0, microsecond=0)
	midnight = SETTING_TIME_ZONE.localize(midnight)
	return midnight


def index(request):
	midnight = _get_next_day_midnight()

	counts = Word.objects.filter(graduated=False).extra({'next_review_date' : 'date(next_review_at)'})\
					.values('next_review_date').annotate(count=Count('id'))\
					.order_by('next_review_date')

	onProgress = Word.objects.filter(graduated=False).count()
	graduates = Word.objects.filter(graduated=True).count()

	return render(request, 'word/index.html', {'counts': counts, 
											'onProgress': onProgress, 
											'graduates': graduates,
											'midnight': midnight,})

def list(request, year, month, day):
	year = int(year)
	month = int(month)
	day = int(day)
	midnight = _get_midnight(year, month, day)
	next_midnight = _get_next_midnight(year, month, day)

	word_list = Word.objects.filter(graduated=False)\
				.filter(next_review_at__gte=midnight)\
				.filter(next_review_at__lt=next_midnight)\
				.annotate(rc=Count('review'))\
				.order_by('-created_at')
	total = word_list.count()

	return render(request, 'word/list.html', 
					{'word_list': word_list,
					'total': total,})

def check(request, id):
	word = Word.objects.get(pk=id)
	year, month, day = word.getDateTuple()

	return render(request, 'word/check.html', 
							{'word': word, 'year': year, 'month': month, 'day': day})

def done(request, id):
	word = Word.objects.get(pk=id)

	if word.next_review_at > _get_next_day_midnight():
		return HttpResponse("The review date has not reached.")
	else:
		year, month, day = word.getDateTuple()
		word.review_set.create()
		word.calculate_next_review_date()
		return redirect(reverse('word:list', kwargs={'year': year, 'month': month, 'day': day}))

def new(request):
	form = AddWordForm()
	return render(request, 'word/new.html', {'form': form})

def create(request):
	f = AddWordForm(request.POST)
	if f.is_valid():
		e = f.save()
		year, month, day = e.getDateTuple()
		return redirect(reverse('word:list', kwargs={'year': year, 'month': month, 'day': day}))
	else:
		return HttpResponse("Create Failed.")

def downloadVoice(request, id):
	word = Word.objects.get(pk=id)
	word.downloadPronounceFile()
	year, month, day = word.getDateTuple()
	return redirect(reverse('word:list', kwargs={'year': year, 'month': month, 'day': day}))

