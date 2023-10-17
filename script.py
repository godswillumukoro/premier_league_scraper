import requests
from bs4 import BeautifulSoup  # For parsing HTML
import pandas as pd
from io import StringIO

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

# append leading string to have full absolute urls
team_urls = [f"https://fbref.com{h}" for h in href_links]

# print(team_urls)

# Get stats
team_url = team_urls[0]
response = requests.get(team_url)
html_content = response.text
# Search for the table titled Scores & Fixtures
matches = pd.read_html(StringIO(html_content), match="Scores & Fixtures")
# print(matches[0])

# Scrape shooting stats
soup = BeautifulSoup(response.text, features="html.parser")
shooting_links = soup.find_all('a')
shooting_links = [link.get('href') for link in shooting_links]
shooting_links = [
    # find links to the shooting stats
    link for link in shooting_links if link and 'all_comps/shooting/' in link]

shooting_data = requests.get("https://fbref.com" + str(shooting_links[0]))


shooting = pd.read_html(StringIO(shooting_data.text), match="Shooting")[0]

shooting.columns = shooting.columns.droplevel()  # Drop 1 level of the columns


# Merge both dataframes
merged_data = matches[0].merge(
    shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")

print(merged_data)
