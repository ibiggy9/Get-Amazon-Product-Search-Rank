from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import title_contains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
from asinGenerator import canadian, american
from bs4 import BeautifulSoup
import pyrebase


class Scrape:
    def __init__(self, keyword, page_number):
        self.PATH = "/Users/main/desktop/code/scraping/chromedriver_PATH_for_selenium_ref/chromedriver"
        self.keyword = keyword
        self.keyword_list = []
        self.now = datetime.now()
        self.current_time = self.now.strftime("%d %m %Y")
        self.dates = []
        self.page_number = page_number
        self.page_number_save = []
        self.chrome_options = Options()
        self.chrome_options.headless = True
        self.chrome_options.add_argument = ("--disable-extensions")
        self.chrome_options.add_argument = ("--disable-gpu")
        self.driver = webdriver.Chrome(self.PATH, options=self.chrome_options) 
        self.actions = ActionChains(self.driver)
        self.canAsins = canadian()
        self.usAsins = american()
        self.url = f'https://www.amazon.ca/s?k={keyword}&page={page_number}&qid=1615988169&ref=sr_pg_2'
        self.dictRank = []
        self.dare_match = [] 
        self.title = []
        self.asin_list = []
        self.rank = []
        self.getinfo()
        self.render_output()
        self.firebase()
  
       
    
    def getinfo(self):
        self.driver.get(self.url)
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        self.cards = self.soup.find_all('div', {'data-asin': True, 'data-component-type':'s-search-result'})

        for card in self.cards:
            h2 = card.h2
            self.title.append(h2.text.strip())
            self.asin_list.append(card.get('data-asin').strip())

        for search in self.soup.select('div[data-index]'):
            rank = 60*(int(self.page_number)-1)+int(search['data-index'])
            self.rank.append(rank)

        for i in range(1,len(self.asin_list)):
            self.dates.append(self.current_time.strip())

        self.page_number_save.append(self.page_number)  
        self.keyword_list.append(self.keyword)
        try:
            self.dictRank = list(zip(self.rank, self.asin_list , self.dates, self.title)) 
        except:
            pass 

    def render_output(self):
        try:
            for rank, code, dates, title in self.dictRank:
                #Logic is if there is any asin in the value list that matches the value in the canAsin list...
                if any(asin in code for asin in self.canAsins):
                    self.dare_match = list(zip((code, title, rank, self.page_number_save, dates, self.keyword_list)))           
        except:
            self.driver.close()
            pass

        try:
            print(f'ASIN:{self.dare_match[0]}')
            print(f'Product Title:{self.dare_match[1]}')
            print(f'Search Rank:{self.dare_match[2]}')
            print(f'Page Number: {self.dare_match[3]}')
            print(f'Date Scraped:{self.dare_match[4]}')
            print(f'Search Term:{self.dare_match[5]}')
        except Exception:
            print("No Search Results")
            pass

        return self.dare_match

    def firebase(self):
         
        firebaseCongif = {
                "apiKey": "AIzaSyBmQ8WwUeU7nyuP0VbRepBhzFKKCkiLzgo",
                "authDomain": "dare-database---scraping.firebaseapp.com",
                "databaseURL": "https://dare-database---scraping-default-rtdb.firebaseio.com",
                "projectId": "dare-database---scraping",
                "storageBucket": "dare-database---scraping.appspot.com",
                "messagingSenderId": "68821745335",
                "appId": "1:68821745335:web:e2950ef3ae727c03a61732"
            }
        firebase=pyrebase.initialize_app(firebaseCongif)

        db=firebase.database()
        try:
            data={
                "ASIN": self.dare_match[0],
                "Product Title": self.dare_match[1],
                "Search Rank": self.dare_match[2],
                "Page Number": self.page_number,
                "Date Scraped": self.dare_match[4],
                "Search Term": self.keyword,
            }
            
            db.child(self.keyword).child(self.current_time).child('Results').push(data)
        
        except:
            pass
        
        
