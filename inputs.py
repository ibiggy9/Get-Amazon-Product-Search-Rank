# Import necessary modules
from product_rank_tracker import Scrape
import time

# ========================== CONFIGURATION ==========================

# Keywords related to different categories we want to search
category_terms = [
    'cookies', 'crackers', 'candy', 'cooky', 'gluten free', 'all natural', 
    'vegan', 'snacks', 'chips', 'add on crackers', 'add on cookies', 'add on candy'
]

# Brands that are of interest to us
brand_terms = ['realfruit', 'bear paws', 'breton', 'whippet', 'ultimates', 'dare']

# Competitor brands that we want to monitor
competitive_brand_terms = [
    'oreo', 'chips ahoy', 'maynards', 'Sour patch', 'triscuit', 
    'Good thins', 'Wheat thins', 'goldfish', 'leclerc'
]

# Number of pages to scrape for each keyword
number_of_pages = 3

# ========================== CALCULATIONS & FORMATTING ==========================

# Calculate actual pages to scrape (incremented by one)
actual_pages = number_of_pages + 1

# Lists to store formatted keywords and page numbers
keyword_formatted = []
page_number_formatted = []

# Combine category, brand, and competitor terms into one list
keyword_input = category_terms + brand_terms + competitive_brand_terms

# Format the data for scraping by creating pairs of keyword and page number
for word in keyword_input:
    for number in range(1, actual_pages):
        keyword_formatted.append(word)
        page_number_formatted.append(number)

# Pair each keyword with its corresponding page number using zip
formatted_data = list(zip(keyword_formatted, page_number_formatted))

# ========================== SCRAPING ==========================

# Initialize an empty list to store the results
results = []

# Iterate over the formatted data to scrape results for each keyword-page pair
for searchTerm, pageNumber in formatted_data:
    result = Scrape(searchTerm, pageNumber)  # Scrape function call
    results.append(result)  # Append the scraped data to the results list
