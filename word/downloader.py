from django.conf import settings

import urllib.request
import os

ROOT_PATH = settings.DOWNLOAD_DIR

def download(url, filePath):
	fileToWrite = os.path.join(ROOT_PATH, filePath)
	urllib.request.urlretrieve(url, fileToWrite)

