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














# Write your test cases here.
print("\n\n ********** TESTS (PASS/FAIL) **********\n")

class Test_NatlParkData(unittest.TestCase):

	def test1_cachedict(self):
		random_dict = {}
		self.assertEqual(type(CACHE_DICTION),type(random_dict), "CACHE_DICTION IS MISSING")
	
	#def test2_identifier(self):

if __name__ == "__main__":
	unittest.main(verbosity=2)


## Remember to invoke all your tests...