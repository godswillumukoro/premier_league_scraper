import requests
from bs4 import BeautifulSoup  # For parsing HTML
import pandas as pd
from io import StringIO
from colorama import init, Fore, Style
import pyfiglet
from ascii_art import ASCII_ART

# Initialize colorama
init(autoreset=True)

# ASCII art title
title = ASCII_ART

commands = f"""
- {Fore.YELLOW}latest{Style.RESET_ALL}: to see the latest score
- {Fore.YELLOW}top5{Style.RESET_ALL}: to see the top 5 teams
- {Fore.YELLOW}exit{Style.RESET_ALL}: to exit the application
"""

message = f"""
Welcome to {Fore.GREEN}Premier League Scrapper{Style.RESET_ALL}!
Stay up-to-date with the most recent Premier League news directly from your command line.

Use the following commands:
{commands}
"""

# stats_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
team_urls = []

try:

    # download the HTML of this page
    data = requests.get("https://fbref.com/en/comps/9/Premier-League-Stats")
    data.raise_for_status()  # Check for HTTP errors

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
except requests.exceptions.RequestException as e:
    # Handle network-related errors
    print("An expected error occurred. Try again.")
    # Or you can return the error message if this code is inside a function
    # return "An expected error occurred. Try again."
except Exception as e:
    # Handle other unexpected errors
    print(f"An unexpected error occurred: {e}")
    # Or you can return the error message if this code is inside a function
    # return f"An unexpected error occurred: {e}"

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

# Introduction Prompt Message
try:
    print(Fore.GREEN + title + "\n" + message)
except:
    print(pyfiglet.figlet_format(
        "Premier League Scraper", font="slant"), "\n" + message)


def runScript():
    while True:
        userPrompt = input("Enter a command: ").lower().strip()
        if userPrompt == "latest":
            print(Fore.GREEN + 'LATEST NEWS')
            print(merged_data)
            print(commands)
        elif userPrompt == 'top5':
            print(Fore.GREEN + 'TOP 5 RESULTS')
            print(merged_data.head())
            print(commands)
        elif userPrompt == "exit":
            print(Fore.YELLOW + 'Okie Dokie.. See ya later :)')
            break
        else:
            print(Fore.RED + "Oops! It seems there might be a small mistake with your command. Please select a command from the list below:")
            print(commands)


runScript()
