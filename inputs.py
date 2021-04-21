from product_rank_tracker import Scrape
import time

#inputs go here Standard pull is in there now 
category_terms = ['cookies','crackers','candy','cooky','gluten free','all natural','vegan','snacks','chips','add on crackers','add on cookies','add on candy']
brand_terms = ['realfruit','bear paws','breton','whippet','ultimates', 'dare']
competitive_brand_terms = ['oreo','chips ahoy','maynards','Sour patch','triscuit','Good thins','Wheat thins','goldfish','leclerc']
number_of_pages = 3



# Calculations
actual_pages = number_of_pages + 1
page_number_formatted = []
keyword_formatted = []
results = []

#Data formatting
#Combining lists of keywords
keyword_input = []
for i in category_terms:
    keyword_input.append(i)
for i in brand_terms:
    keyword_input.append(i)
for i in competitive_brand_terms:
    keyword_input.append(i)

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
    

    



 
        

        


