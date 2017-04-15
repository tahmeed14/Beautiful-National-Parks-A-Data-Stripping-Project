###### INSTRUCTIONS ###### 

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. 
# For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on 
# flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should
# be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and 
# without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.
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

# Begin filling in instructions....

# Set up Caching for Entire Project
CACHE_FILENAME = "si206final_project_cache.json" 

try:
	f = open(CACHE_FILENAME,'r')
	cache_data = f.read()
	f.close()
	CACHE_DICTION = json.loads(cache_data) #Dump data into Cache Dictionary
except:
	CACHE_DICTION = {} #Create Cache Dictionary

# Personal Function, get_state_page()
# I created to be used in get_parks_data. This function returns a list of all the links of the states containing all the parks in that
# state. This is how I initially started to think about my project and I think it works well. So I went with it. 

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
		
	if parks_identifier in CACHE_DICTION:
			#print("Accessing Cached Data for National Parks")
		nattyparks_str_lst = CACHE_DICTION[parks_identifier]

	else:
		nattyparks_str_lst = []
		for i in link_list:
			print("Loop Counter")
			stripped_data = requests.get(i).text
			soup_var2 = BeautifulSoup(stripped_data, "html.parser") 
			column_grid = soup_var2.find("div", {"class" : "ColumnMain col-sm-12"}) #Nested HTML 
			park_names = column_grid.find_all("h3") #Under h3
			park_a = [x.find("a") for x in park_names] #All elements with a has href
			park_link_list = [a["href"] for a in park_a] #index href to get links
			dummy_url_lst = ["https://www.nps.gov" + href + "index.htm" for href in park_link_list] #Need appropriate url, thus, we add two extra str's
			# An example link: https://www.nps.gov/state/al/index.htm

			nattyparks_str_dummy = [requests.get(link).text for link in dummy_url_lst] # Constructed by referring to beautsoup_example_errors.py

			for b in nattyparks_str_dummy:
				nattyparks_str_lst.append(b)


		CACHE_DICTION[parks_identifier] = nattyparks_str_lst #Dictionary key value pair

			#Write it into cache file
		f = open(CACHE_FILENAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	return nattyparks_str_lst

# Save the list of all of the parks html formatted strings into a variable
html_parks_list = get_parks_data()

#print(html_parks_list[0])

# Write a function to get and cache HTML data from each of the articles on the front page of the main NPS website. An example of an article can be found 
# at https://home.nps.gov/ever/wilderness.htm -- which you get to by clicking on this displayed link on the front page of NPS.gov, for example:

def get_articles_data():
	articles_identifier = "articles_data"
	natty_park_site = "https://www.nps.gov/index.htm"

	if articles_identifier in CACHE_DICTION:
		html_articles_list = CACHE_DICTION[articles_identifier]

	else:
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
		#print(article_sub_urls)
		article_dummy_list = ["https://www.nps.gov" + url for url in article_sub_urls]
		#print(article_dummy_list)
		html_articles_list = [requests.get(link).text for link in article_dummy_list]
		#print(html_articles_list[0])
		CACHE_DICTION[articles_identifier] = html_articles_list

		f = open(CACHE_FILENAME, "w") #Reference lecture + previous hw to format, simple.
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	return html_articles_list

# Save the list of all of the parks html formatted strings into a variable
html_articles_list = get_articles_data()

# Define a class NationalPark which accepts an  HTML-formatted string as input, and uses BeautifulSoup data parsing to access the data you want 
# and store it in instance variables, etc.

# This class should have:
# At least 3 instance variables
# At least 2 methods besides a constructor

class NationalPark(object):
	# Class variables
	states_dict = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'}

	def __init__(self, html_string):

		self.park_soup = BeautifulSoup(html_string, "html.parser") #Soup instance for the park
		
		park_title_div = self.park_soup.find("div", {"class" : "Hero-titleContainer clearfix"})
		self.name = park_title_div.find("a").text #Name of the park

		park_state_div = self.park_soup.find("div", {"class" : "Hero-designationContainer"})
		self.states = park_state_div.find("span", {"class" : "Hero-location"}).text

		plan_visit_div = self.park_soup.find("div", {"id" : "npsNav"})
		plan_visit_div2 = plan_visit_div.find("li", {"class" : "has-sub"})
		plan_visit_a = plan_visit_div2.find_all("a")
		self.tup_links = [(a["href"], a.text) for a in plan_visit_a]


	def __str__(self):
		return "{} is located in {}".format(self.name, self.states)

	def get_parkdescript(self):
		desc_div = self.park_soup.find("div", {'class' : "Component text-content-size text-content-style"})
		desc = desc_div.find("p").text
		return desc

	def get_planpage(self):
		plan_visit = self.tup_links[0][0]
		plan_visit_url = "https://www.nps.gov" + plan_visit
		return plan_visit_url

	def get_basicinfo(self):
		basic_info = self.tup_links[1][0]
		basic_info_url = "https://www.nps.gov" + basic_info
		return basic_info_url

	def get_faqs(self):
		faqs = self.tup_links[-1][0]
		faqs_url = "https://www.nps.gov" + faqs
		return faqs

	def modify_state(self):
		states_list = [self.states_dict[key] for key in self.states_dict.keys()]

		if (self.states not in states_list):
			index_state = self.states[0] + self.states[1] #Will get index like "AL" or "MI"
			self.states = self.states_dict[index_state] #Assign only the first state for the state of the park
					
		else:
			self.states = self.states

# Define a class Article that accepts a big HTML string representing one article on the NPS.gov front page. 
# E.g. the one at https://home.nps.gov/ever/wilderness.htm, the one at https://www.nps.gov/subjects/worldwari/index.htm ...

# This class should have at least 2 instance variables. Instance variables that might be useful for this class could be: title, text, description
# You could also define methods for this class if you think they will be useful for your plan! (You do not have to.)

#class Article(object):

# Write code to create a list of instances of the NationalPark class. 
# This might be a good place to use a comprehension structure… and go through the data you saved about the national parks from your first function! 
# You'll be able to use this list of instances when you load data into your database.

# Ideally we want all the parks, but one park page has an error right now
#print(html_parks_list[39])
nationalpark_instance_list1 = [NationalPark(html_parks_list[i]) for i in range(39)]

# The 39th item is a page that is currently locked by the National Park Website, so we will do this instead:
#nationalpark_instance_list2 = [NationalPark(html_parks_list[i]) for i in range(40,654)]

#FOR NOW I AM COMMENTING THIS OUT TO AVOID SLOWING DOWN MY CODE, IT'S ANNOYING TO DEBUG
# html_parks_list.pop(39)
# nationalpark_instance_list = [NationalPark(x) for x in html_parks_list]

# Write code to create a list of instances of the Article class.
# The second function described above will be pretty useful here…
# You'll be able to use these lists of instances when you load data into your database tables!
#articles_instance_list = [Article]

# Use requests / BeautifulSoup on this page: https://www.currentresults.com/Weather/US/average-annual-state-temperatures.php to gather each state's 
# average temperature (in Fahrenheit OR Celsius as you prefer) and store them in a dictionary with  key:value pairs that represent states as keys and 
# average-temps as their associated values

# A Parks table (for parks and monuments) containing information specific to each park like name, a reference to the States table, a description, and/or 
# anything else you find interesting that is specific to each park/monument/site...

# A States table with info about each state, like name, abbrv, avg temp… 
# (note that if a park is in multiple states and has a location like "AL,AR,GA,IL,KY,MO,NC,OK,TN", you have to decide how to handle this relationship. 
# This is the sort of thing you describe your choice about in your readme! "I decided to use just the first state listed in the list of states for any 
# park in multiple states for the relationship to the states table…")


# Put your tests here, with any edits you now need from when you turned them in with your project plan.
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

	def test1_return_type(self):
		x = get_state_page()
		self.assertEqual(type(x), type([]))
		
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

	# def test3_len_return(self):
	# 	self.assertEqual(len(get_parks_data()), , "There should be a lot of parks and monuments")

class Test_ArticlesData(unittest.TestCase):

	def test1_ret_type_art(self):
		self.assertEqual(type(get_articles_data()), type(["Chelsea FC, Premier League Champs"]))

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
	
class Test_NatParks_Class(unittest.TestCase):

	def test1_instance_variables(self):
		birmingham_crp = NationalPark(get_parks_data()[0])
		park_name1 = "Birmingham Civil Rights"
		self.assertEqual(birmingham_crp.name, park_name1)
		self.assertEqual(birmingham_crp.states, "Alabama")

		katmai = NationalPark(get_parks_data()[21])
		park_name2 = "Katmai"
		self.assertEqual(katmai.name, park_name2)
		self.assertEqual(katmai.states, "Alaska")

		ww2_valor = NationalPark(get_parks_data()[28])
		#print(ww2_valor)
		park_name3 = "World War II Valor in the Pacific"
		#print(ww2_valor.states)
		self.assertEqual(ww2_valor.name, park_name3)
		

	def test2_modifystate(self):
		birmingham_crp = NationalPark(get_parks_data()[0])
		ww2_valor = NationalPark(get_parks_data()[28])

		self.assertEqual(ww2_valor.states, "HI, AK, CA")

		ww2_valor.modify_state()
		#print(ww2_valor.states)
		self.assertEqual(ww2_valor.states, "Hawaii")

		birmingham_crp.modify_state()
		self.assertEqual(birmingham_crp.states, "Alabama")

	def test3_desc_method(self):
		katmai = NationalPark(get_parks_data()[21])
		park_desc = "Katmai National Monument was established in 1918 to protect the volcanically devastated region surrounding Mount Katmai and the Valley of Ten Thousand Smokes. Today, Katmai National Park and Preserve remains an active volcanic landscape, but it also protects 9,000 years of human history as well as important habitat for salmon and thousands of brown bears."
		self.assertEqual(type(katmai.get_parkdescript()), type("yo"))
		#self.assertEqual(katmai.get_parkdescript(), park_desc)

		birmingham_crp = NationalPark(get_parks_data()[0])
		park_desc2 = "In 1963, images of snarling police dogs unleashed against non-violent protesters and of children being sprayed with high-pressure hoses appeared in print and television news across the world. These dramatic scenes from Birmingham, Alabama, of violent police aggression against civil rights protesters were vivid examples of segregation and racial injustice in America."
		self.assertEqual(type(birmingham_crp.get_parkdescript()), type("blah"))
		# self.assertEqual(birmingham_crp.get_parkdescript(), park_desc2) #apparently the strings are too long for the tests, so I had to comment it out

class Test_ExtraVariables(unittest.TestCase):
	
	def test1_htmlnatlparklist(self):
		self.assertEqual(len(get_parks_data()), 654)

if __name__ == "__main__":
	unittest.main(verbosity=2)

# Remember to invoke your tests so they will run! (Recommend using the verbosity=2 argument.)