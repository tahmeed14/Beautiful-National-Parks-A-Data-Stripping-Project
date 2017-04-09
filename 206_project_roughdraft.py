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
import sys
import codecs

# Open Cache File or Strip Data from internet into cache file
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

CACHE_FILENAME = "si206final_project_cache.json" 

try:
	f = open(CACHE_FILENAME,'r')
	cache_data = f.read()
	f.close()
	CACHE_DICTION = json.loads(cache_data) #Dump data into Cache Dictionary
except:
	CACHE_DICTION = {} #Create Cache Dictionary


# Personal Function I created to be used in get_parks_data. This function returns a list of all the links of the states containing all the parks in that
# state. This is how I initially started to think about my project and I think it will work. So I went with it. 
def get_state_page():
	state_identifier = "parks_by_state"
	natty_park_site = "https://www.nps.gov/index.htm"

	if state_identifier in CACHE_DICTION:
		stateslink_list = CACHE_DICTION[state_identifier]

	else:
		print("Stripping Online Data")
		
		request_park_data = requests.get(natty_park_site).text
		soup_var1 = BeautifulSoup(request_park_data, "html.parser")
		states_button = soup_var1.find("div", {"class" : "SearchBar-keywordSearch input-group input-group-lg"})
		drop_down_menu = states_button.find("ul", {"class" : "dropdown-menu SearchBar-keywordSearch"})
		states_link = drop_down_menu.find_all("a")
		states_page_list = [a["href"] for a in states_link]
		stateslink_list = ["https://www.nps.gov" + i for i in states_page_list]

		CACHE_DICTION[state_identifier] = stateslink_list

		f = open(CACHE_FILENAME, "w") #Reference lecture + previous hw to format, simple.
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	return stateslink_list

# Get data from the National Parks website using BeautifulSoup, which has a lot of hierarchy of links inside it. 
# The root page is: https://www.nps.gov/index.htm 
# Write a function to get and cache HTML data about each national park/monument from every state. 
# I recommend storing the data in a big list, so you can return a list of HTML strings which each represent a park/site/monument from a function. 
# Each HTML string should contain all the data you need, like what state(s) the park is in, the park's name, etc… so you could pass each HTML string 
# straight into a class constructor!

def get_parks_data():
	link_list = get_state_page()

	parks_identifier = "natty_parks_data"
	
	for i in link_list:
		if parks_identifier in CACHE_DICTION:
			#print("Accessing Cached Data for National Parks")
			nattyparks_str_lst = CACHE_DICTION[parks_identifier]

		else:
			stripped_data = requests.get(i).text
			soup_var2 = BeautifulSoup(stripped_data, "html.parser") 
			column_grid = soup_var2.find("div", {"class" : "ColumnMain col-sm-12"}) #Nested HTML 
			park_names = column_grid.find_all("h3") #Under h3
			park_a = [i.find("a") for i in park_names] #All elements with a has href
			park_link_list = [a["href"] for a in park_a] #index href to get links
			dummy_url_lst = ["https://www.nps.gov" + href + "index.htm" for href in park_link_list] #Need appropriate url, thus, we add two extra str's
			
			nattyparks_str_lst = [requests.get(link).text for link in dummy_url_lst] # Constructed by referring to beautsoup_example_errors.py

			CACHE_DICTION[parks_identifier] = nattyparks_str_lst #Dictionary key value pair

			#Write it into cache file
			f = open(CACHE_FILENAME, "w")
			f.write(json.dumps(CACHE_DICTION))
			f.close()

	return nattyparks_str_lst


# 		else:
# 		print("Stripping Online Data")
# 		nattyparks_str_lst = [] #Initialize List
# 		request_park_data = requests.get(natty_park_site)
		
# 		print(request_park_data)

# 		# soup_var = BeautifulSoup(request_park_data, "html.parser")
# 		# print(soup_var)

# 		# print("****************************************************************************************************************************************")
# 		# states_button = soup_var.find("div", {"class" : "SearchBar-keywordSearch input-group input-group-lg"})
# 		# print(states_button)
		
# 		#parks_html = request_park_data.text # .text let's us put html in string format

# 		#nattyparks_str_lst.append(parks_html)

# 		CACHE_DICTION[parks_identifier] = nattyparks_str_lst

# 		f = open(CACHE_FILENAME, "w")
# 		f.write(json.dumps(CACHE_DICTION)) #dump html strings into file
# 		f.close()

# 	return nattyparks_str_lst
# link_list = get_state_page()

# stripped_data = requests.get(link_list[55]).text
# soup_var2 = BeautifulSoup(stripped_data, "html.parser")

# column_grid = soup_var2.find("div", {"class" : "ColumnMain col-sm-12"})

# park_names = column_grid.find_all("h3")
# # print(park_names)
# # print(type(park_names))

# park_a = [i.find("a") for i in park_names]
# # print(park_a)

# park_link_list = [a["href"] for a in park_a]
# # print(park_link_list)

# dummy_url_lst = ["https://www.nps.gov" + href + "index.htm" for href in park_link_list]

# nattyparks_str_lst = [requests.get(link).text for link in dummy_url_lst]


# park_link_list = [a["href"] for a in park_a]
# print(park_link_list)

# nattyparks_str_lst = [requests.get(link) for link in park_link_list]

# print(type(nattyparks_str_lst[0]))




# Write a function to get and cache HTML data from each of the articles on the front page of the main NPS website. An example of an article can be found 
# at https://home.nps.gov/ever/wilderness.htm -- which you get to by clicking on this displayed link on the front page of NPS.gov, for example:

# def get_articles_data():
# 	articles_identifier = "articles_data"
# 	article_stripped_site = "https://home.nps.gov/ever/wilderness.htm"

natty_park_site = "https://www.nps.gov/index.htm"

request_park_data = requests.get(natty_park_site).text
soup_var3 = BeautifulSoup(request_park_data, "html.parser")

big_container = soup_var3.find("div", {"class" : "MainContent"})
#print(big_container)
row_container = big_container.find("div", {"class" : "FeatureGrid-item col-xs-12"})
#row_container = big_container.find("div", {"class" : "row"})
#print(row_container)
articles_a = row_container.find_all("a")
#print(articles_a)
article_sub_urls = [a["href"] for a in articles_a]
print(article_sub_urls)


# f = open(CACHE_FILENAME, "w") #Reference lecture + previous hw to format, simple.
# f.write(json.dumps(CACHE_DICTION))
# f.close()







# class NationalPark(object):
# 	def __init__(self, html_string):

# umich_resp1 = requests.get(base_url).text

# umich_resp = BeautifulSoup(umich_resp1,"html.parser")
# 	sub_div = umich_resp.find("div",{"id":"in-the-news"}) #Do we want class = 
# 	news_articles_set = sub_div.find("ul",{"class":"news-items"})

# 	pe_articles_set = sub_div.find("ul",{"class":"pe-items"})
# 	news_links = news_articles_set.find_all("a") #
# 	pe_links = pe_articles_set.find_all("a")
# 	total_article_elements = news_links + pe_links		
# 	article_html_urls = [elem["href"] for elem in total_article_elements]
# 	print(article_html_urls)
# 	article_html_tups = [(requests.get(url).text, url)  for url in article_html_urls]



# stateparks_a = states_link.find_all("a") #find_all just in case!
# print(stateparks_a)


# stateparks_urls = [a["href"] for a in stateparks_a]
# print(stateparks_urls)


# site_by_park = "https://www.nps.gov/findapark/index.htm"

# request_park_data = requests.get(site_by_park).text

# soup_parks = BeautifulSoup(request_park_data, "html.parser")
# print(soup_parks)

# find_park_button = soup_parks.find("div", {"class" : "btn-group open"})

# print(find_park_button)
# print(type(find_park_button))

# drop_down_menu = find_park_button.find("ul", {"class" : "multiselect-container dropdown-menu"})
# all_options = drop_down_menu.find_all("li")
# print(all_options)

# # dummy_parks_list = [] #create dummy list
# # for li in all_options:
# # 	if (a in li):
# # 		dummy_parks_list.append(li)
# # 	else:
# # 		None

# # print(dummy_parks_list)








# Write your test cases here.
# print("\n\n ********** TESTS (PASS/FAIL) **********\n")

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
			self.assertEqual(type(x), type("stats"), "CACHE DICTION does not have your unique identifier!")

class Test_StatesData(unittest.TestCase):

	def test1_return_type(self):
		x = get_state_page()
		self.assertEqual(type(x), type([]))
		
	def test2_return_len(self):
		y = get_state_page()
		self.assertEqual(len(y), 56, "This function must return a list with 56 elements because there are 56 states on the website")

	def test3_last_state(self):
		z = get_state_page()[55]
		self.assertEqual(z, "https://www.nps.gov/state/wy/index.htm", "Something is wrong with the link for Wyoming")

class Test_ParksData(unittest.TestCase):

	def test1_ret_type(self):
		self.assertEqual(type(get_parks_data()), type(["a","beta", "see"]), "The returned value for this function is not a list looks like")

	def test2_listelemtype(self):
		self.assertEqual(type(get_parks_data()[0]), type("alpha"), "The first element in get_parks_data list is not a string")

	
	


if __name__ == "__main__":
	unittest.main(verbosity=2)


## Remember to invoke all your tests...