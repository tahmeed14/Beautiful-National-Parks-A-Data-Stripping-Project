## Your name: Tahmeed Tureen
## The option you've chosen: Project #1: BeautifulSoup and National Parks

# Put import statements you expect to need here!
import unittest
import codecs
import json
import requests
import sqlite3 #For DataBase
from bs4 import BeautifulSoup
import collections #for Counter
import sys #for encoding errors in windows
import codecs #for encoding errors in windows














# Write your test cases here.

class Test_Initial_Caching(unittest.TestCase):

	def test1_cachefile(self):
		file = open("si206final_project_cache.json","r")
		read_var = file.read()
		file.close()
		self.assertEqual(type(read_var),type(""),"Something wrong with Cache file, open file from directory and evaluate")

	def test2_cachedict(self):
		random_dict = {}
		self.assertEqual(type(CACHE_DICTION),type(random_dict), "CACHE_DICTION IS MISSING")

	def test3_cachedict(self):
		if "natty_parks_data" in CACHE_DICTION:
			x = "blah"
			self.assertEqual(type(x), type("stats"))
		else:
			x = 1
			self.assertEqual(type(x), type("stats"), "CACHE DICTION does not have your unique identifier for parks data!")

class Test_StatesData(unittest.TestCase):
	#Please refer to my 206_project_roughdraft.py to get a better understanding of what this function is. Thank you!
	def test1_return_type(self):
		x = get_state_page()
		self.assertEqual(type(x), type([]), "This function is suppose to return a list variable")
		
	def test2_return_len(self):
		y = get_state_page()
		self.assertEqual(len(y), 56, "This function must return a list with 56 elements because there are 56 states on the website")

	def test3_michigan(self):
		greatest_state_but_the_weather_sucks = get_state_page()[24]
		self.assertEqual(greatest_state_but_the_weather_sucks, 'https://www.nps.gov/state/mi/index.htm' )

	def test4_last_state(self):
		z = get_state_page()[55]
		self.assertEqual(z, "https://www.nps.gov/state/wy/index.htm", "Something is wrong with the link for Wyoming")

class Test_ParksData(unittest.TestCase):

	def test1_ret_type(self):
		self.assertEqual(type(get_parks_data()), type(["a","beta", "see"]), "The returned value for this function is not a list looks like")

	def test2_listelemtype(self):
		self.assertEqual(type(get_parks_data()[0]), type("alpha"), "The first element in get_parks_data list is not a string")

	def test3_len_return(self):
		self.assertEqual(len(get_parks_data()), 654 , "There should be a lot of parks and monuments, I think it's 654 but we'll make sure soon!")

class Test_ArticlesData(unittest.TestCase):

	def test1_ret_type_art(self):
		self.assertEqual(type(get_articles_data()), type(["Chelsea FC, Premier League Champs"]), "This function should return a list!")

	def test2_elem_type(self):
		self.assertEqual(type(get_articles_data()[-1]), type(""), "Last element in returned value is not a str")
		self.assertEqual(type(get_articles_data()[0]), type(""), "First element in returned value is not a str")

	def test3_len_return(self):
		#AS OF RIGHT NOW, the homepage has only 2 articles but this actually may change. So this test will be tentative...
		self.assertEqual(len(get_articles_data()), 2)

	def test4_cachedict(self):
		if "articles_data" in CACHE_DICTION:
			x = "blah"
		else:
			x = 1
		self.assertEqual(type(x), type("stats"), "CACHE DICTION does not have your unique identifier for articles data!")

if __name__ == "__main__":
	unittest.main(verbosity=2)


## Remember to invoke all your tests...