import schedule
import os

def run():
    os.system("python3.9 /Users/main/desktop/code/scraping/dare_stuff/new_scrapers/search_performance/inputs.py")
    print('running')
schedule.every(24).hours.do(run)

while True:
    schedule.run_pending()
