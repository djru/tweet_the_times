from __future__ import print_function

import requests
from bs4 import BeautifulSoup
import tweepy
import datetime

URL = 'http://www.newseum.org/todaysfrontpages/?tfp_show=all&tfp_id=NY_NYT'
SELECTOR = '.tfp-thumbnail img'
CONSUMER_KEY = '6U0m0uYAAVRWud3fQ6luuaCmj'
CONSUMER_SECRET = 'SF1D6OpB7kmHxFFKi5cUvBZKpaL7jAtmnj8xgIdnSGPWIjM8VZ'
TOKEN = '772651361196531712-YkibPRfWHwKg9h5XnvWSPrNXKRful14'
TOKEN_SECRET = 'ASGUKMBW2DQt6cDfGtnLChdDUAw8ytEl8KxCsAKfyXTuM'
FILENAME = '/tmp/temp.jpg'

def lambda_handler(event, context):
	page = requests.get(URL)
	soup = BeautifulSoup(page.text)
	image_el= soup.select(SELECTOR)[0]

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(TOKEN, TOKEN_SECRET)
	api = tweepy.API(auth)

	img = requests.get(image_el['src'], stream=True)
	with open(FILENAME, "wb") as i:
		i.write(img.raw.read())
	api.update_with_media(FILENAME, status=datetime.date.today().strftime('%A %B %e, %Y'))
	return True
