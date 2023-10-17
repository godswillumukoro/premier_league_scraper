import requests
from bs4 import BeautifulSoup  # For parsing HTML
import pandas as pd

stats_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

data = requests.get(stats_url)  # download the HTML of this page

# Initialize the soup object
soup = BeautifulSoup(data.text,  features="html.parser")

# select the first element. using css selector
stats_table = soup.select('table.stats_table')[0]

# print(stats_table)  # View downloaded HTML
href_links = stats_table.find_all('a')  # select anchor tags using find_all

# get href properties using list comprehension
href_links = [h.get('href') for h in href_links]

# get rid of the link if its not squads links
href_links = [h for h in href_links if '/squads/' in h]

team_urls = [f"https://fbref.com{h}" for h in href_links] # append leading string to have full absolute urls

print(team_urls)

# Get stats
team_url = team_urls[0]
data = requests.get(team_url)

