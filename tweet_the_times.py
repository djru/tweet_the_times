from __future__ import print_function

import requests
from bs4 import BeautifulSoup
import tweepy
import datetime

# this is the URL we will visit to pull the image
URL = 'http://www.newseum.org/todaysfrontpages/?tfp_show=all&tfp_id=NY_NYT'
# a css selector that matches the images
SELECTOR = '.tfp-thumbnail img'
# twitter API keys
CONSUMER_KEY = '6U0m0uYAAVRWud3fQ6luuaCmj'
CONSUMER_SECRET = '**SECRET**'
TOKEN = '772651361196531712-YkibPRfWHwKg9h5XnvWSPrNXKRful14'
TOKEN_SECRET = '**SECRET**'
# location to store file before tweeting (must be in /tmp)
FILENAME = '/tmp/temp.jpg'

def lambda_handler(event, context):
	# load the page html and parse it with beutifulsoup
	page = requests.get(URL)
	soup = BeautifulSoup(page.text)
	# select the image tag from the html
	image_el= soup.select(SELECTOR)[0]

	# create a twitter api object with our keys
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(TOKEN, TOKEN_SECRET)
	api = tweepy.API(auth)

	# fetch the raw image using the src attribute on the image tag
	img = requests.get(image_el['src'], stream=True)
	# load the image file and save it to FILENAME
	with open(FILENAME, "wb") as i:
		i.write(img.raw.read())
	# tweet the image with todays date as text
	api.update_with_media(FILENAME, status=datetime.date.today().strftime('%A %B %e, %Y'))
	return True
