# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from asinGenerator import canadian, american
from bs4 import BeautifulSoup
import pyrebase

class Scrape:
    def __init__(self, keyword, page_number):
        # Initialize instance variables
        self.keyword = keyword
        self.keyword_list = []
        self.now = datetime.now()
        self.current_time = self.now.strftime("%d %m %Y")
        self.dates = []
        self.page_number = page_number
        self.page_number_save = []
        self.chrome_options = Options()
        self.chrome_options.headless = True
        # Set Chrome options
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=self.chrome_options)  # Removed direct path to chromedriver
        self.actions = ActionChains(self.driver)
        self.canAsins = canadian()
        self.usAsins = american()
        self.url = f'https://www.amazon.ca/s?k={keyword}&page={page_number}'  # Removed specific query id and reference
        self.dictRank = []
        self.dare_match = []
        self.title = []
        self.asin_list = []
        self.rank = []
        self.getinfo()
        self.render_output()
        self.firebase()

    def getinfo(self):
        # Fetch the webpage and parse it
        self.driver.get(self.url)
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        # Extract necessary data from the parsed page
        self.cards = self.soup.find_all('div', {'data-asin': True, 'data-component-type':'s-search-result'})
        for card in self.cards:
            h2 = card.h2
            self.title.append(h2.text.strip())
            self.asin_list.append(card.get('data-asin').strip())
        for search in self.soup.select('div[data-index]'):
            rank = 60*(int(self.page_number)-1)+int(search['data-index'])
            self.rank.append(rank)
        for _ in range(1,len(self.asin_list)):
            self.dates.append(self.current_time.strip())
        self.page_number_save.append(self.page_number)  
        self.keyword_list.append(self.keyword)
        try:
            self.dictRank = list(zip(self.rank, self.asin_list, self.dates, self.title))
        except:
            pass

    def render_output(self):
        # Process and display the extracted data
        try:
            for rank, code, dates, title in self.dictRank:
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
        # Initialize and push data to Firebase
        firebaseConfig = {
            # Placeholder values for public version
            "apiKey": "YOUR_API_KEY_HERE",
            "authDomain": "YOUR_AUTH_DOMAIN_HERE",
            "databaseURL": "YOUR_DATABASE_URL_HERE",
            "projectId": "YOUR_PROJECT_ID_HERE",
            "storageBucket": "YOUR_STORAGE_BUCKET_HERE",
            "messagingSenderId": "YOUR_MESSAGING_SENDER_ID_HERE",
            "appId": "YOUR_APP_ID_HERE"
        }
        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()
        try:
            data = {
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
