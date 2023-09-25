#This Code is for a one off search. 


# Import necessary libraries
from product_rank_tracker import Scrape

# Constants
KEYWORD_INPUT = ['candy']
NUMBER_OF_PAGES = 10

# Data preparation

# Adjust pages to cover the range
actual_pages = NUMBER_OF_PAGES + 1

# Lists to hold formatted data
keyword_formatted = []
page_number_formatted = []

# Format keyword and page number data for scraping
for word in KEYWORD_INPUT:
    for number in range(1, actual_pages):
        keyword_formatted.append(word)
        page_number_formatted.append(number)

# Combine keyword and page number to use in scraping
formatted_data = list(zip(keyword_formatted, page_number_formatted))

# Scrape data using the provided formatted data
results = []
for searchTerm, pageNumber in formatted_data:
    result = Scrape(searchTerm, pageNumber)
    results.append(result)  # Assuming you want to store the result in a list
