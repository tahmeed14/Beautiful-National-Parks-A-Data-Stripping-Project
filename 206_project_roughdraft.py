## Your name: Tahmeed Tureen
## The option you've chosen: Project #1: BeautifulSoup and National Parks

# Put import statements you expect to need here!
import unittest
import codecs
import json
import requests
import sqlite3
from bs4 import BeautifulSoup
import collections

# Open Cache File or Strip Data from internet into cache file

CACHE_FILENAME = "si206final_project_cache.json" 

try:
	f = open(CACHE_FILENAME,'r')
	cache_data = f.read()
	f.close()
	CACHE_DICTION = json.loads(cache_data) #Dump data into Cache Dictionary

except:
	CACHE_DICTION = {} #Create Cache Dictionary

# Get data from the National Parks website using BeautifulSoup, which has a lot of hierarchy of links inside it. 
# The root page is: https://www.nps.gov/index.htm 
# Write a function to get and cache HTML data about each national park/monument from every state. 
# I recommend storing the data in a big list, so you can return a list of HTML strings which each represent a park/site/monument from a function. 
# Each HTML string should contain all the data you need, like what state(s) the park is in, the park's name, etc… so you could pass each HTML string 
# straight into a class constructor!

def get_parks_data():
	parks_identifier = "natty_parks_data"
	natty_park_site = "https://www.nps.gov/index.htm"
	
	if parks_identifier in CACHE_DICTION:
		print("Accessing Cached Data for National Parks")
		nattyparks_str_lst = CACHE_DICTION[parks_identifier]
	else:
		nattyparks_str_lst = [] #Initialize List

		request_park_data = requests.get(natty_park_site)
		
		parks_html = request_park_data.text # .text let's us put html in string format
		nattyparks_str_list.append(parks_html)

		CACHE_DICTION[parks_identifier] = nattyparks_str_list

		f = open(CACHE_FILE, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	return nattyparks_str_lst


# Write a function to get and cache HTML data from each of the articles on the front page of the main NPS website. An example of an article can be found 
# at https://home.nps.gov/ever/wilderness.htm -- which you get to by clicking on this displayed link on the front page of NPS.gov, for example:

# def get_articles_data():
# 	articles_identifier = "articles_data"
# 	article_stripped_site = "https://home.nps.gov/ever/wilderness.htm"








# class NationalPark(object):
# 	def __init__(self, html_string):









# Write your test cases here.
print("\n\n ********** TESTS (PASS/FAIL) **********\n")

class Test_Initial_Caching(unittest.TestCase):

	def test1_cachefile(self):
		file = open("si206final_project_cache.json","r")
		read_var = file.read()
		file.close()
		self.assertEqual(type(read_var),type(""),"Something wrong with Cache file, open file from directory and evaluate")

	def test2_cachedict(self):
		random_dict = {}
		self.assertEqual(type(CACHE_DICTION),type(random_dict), "CACHE_DICTION IS MISSING")

class Test_ParksData(unittest.TestCase):

	def test1_list(self):
		self.assertEqual(type(get_parks_data()), type(["a","beta", "see"]))
	


if __name__ == "__main__":
	unittest.main(verbosity=2)


## Remember to invoke all your tests...