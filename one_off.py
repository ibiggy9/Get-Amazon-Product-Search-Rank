from product_rank_tracker import Scrape
import time

#MAKE SURE YOU TURN OFF THE DB FUNCTION

#inputs go here
keyword_input = ['candy']
number_of_pages = 10

# Calculations
actual_pages = number_of_pages + 1
page_number_formatted = []
keyword_formatted = []
results = []

#Data formatting

#formatting the scrape pull
for word in keyword_input:
    for number in range(1,actual_pages):
        keyword_formatted.append(word)

for word in keyword_input:
    for number in range(1, actual_pages):
        page_number_formatted.append(number)

formatted_data = list(zip(keyword_formatted,page_number_formatted))

for searchTerm, pageNumber in formatted_data:
    result = (Scrape(searchTerm, pageNumber))
    

    



 
        

        


