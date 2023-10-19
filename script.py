import requests
from bs4 import BeautifulSoup  # For parsing HTML
import pandas as pd
from io import StringIO
from colorama import init, Fore, Style
import pyfiglet

# Initialize colorama
init(autoreset=True)

# ASCII art title
title = r"""
██████╗░██████╗░███████╗███╗░░░███╗██╗███████╗██████╗░  ██╗░░░░░███████╗░█████╗░░██████╗░██╗░░░██╗███████╗
██╔══██╗██╔══██╗██╔════╝████╗░████║██║██╔════╝██╔══██╗  ██║░░░░░██╔════╝██╔══██╗██╔════╝░██║░░░██║██╔════╝
██████╔╝██████╔╝█████╗░░██╔████╔██║██║█████╗░░██████╔╝  ██║░░░░░█████╗░░███████║██║░░██╗░██║░░░██║█████╗░░
██╔═══╝░██╔══██╗██╔══╝░░██║╚██╔╝██║██║██╔══╝░░██╔══██╗  ██║░░░░░██╔══╝░░██╔══██║██║░░╚██╗██║░░░██║██╔══╝░░
██║░░░░░██║░░██║███████╗██║░╚═╝░██║██║███████╗██║░░██║  ███████╗███████╗██║░░██║╚██████╔╝╚██████╔╝███████╗
╚═╝░░░░░╚═╝░░╚═╝╚══════╝╚═╝░░░░░╚═╝╚═╝╚══════╝╚═╝░░╚═╝  ╚══════╝╚══════╝╚═╝░░╚═╝░╚═════╝░░╚═════╝░╚══════╝

░██████╗░█████╗░██████╗░░█████╗░██████╗░███████╗██████╗░
██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
╚█████╗░██║░░╚═╝██████╔╝███████║██████╔╝█████╗░░██████╔╝
░╚═══██╗██║░░██╗██╔══██╗██╔══██║██╔═══╝░██╔══╝░░██╔══██╗
██████╔╝╚█████╔╝██║░░██║██║░░██║██║░░░░░███████╗██║░░██║
╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚══════╝╚═╝░░╚═╝

"""

# Introduction Prompt Message
try:
    print(Fore.GREEN + title)
except:
    print(pyfiglet.figlet_format("Premier League Scraper", font="slant"))

print(Style.RESET_ALL + "Welcome to the " + Fore.GREEN +
      "Premier League Scrapper" + Style.RESET_ALL + "!")
print("Explore the latest scores and team information in the league.")

# Instructions
print("Use the following commands:")
print("- " + Fore.YELLOW + "latest" +
      Style.RESET_ALL + ": to see the latest score")
print("- " + Fore.YELLOW + "top5" + Style.RESET_ALL + ": to see the top 5 teams")
# print("- " + Fore.YELLOW + "standings" + Style.RESET_ALL +
#       ": to view the current league standings")
# print("- " + Fore.YELLOW + "team <team_name>" + Style.RESET_ALL +
#       ": to get detailed information about a specific team")
print("- " + Fore.YELLOW + "exit" + Style.RESET_ALL + ": to exit the application")


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


def runScript():
    while True:
        userPrompt = input("Enter a command: ").lower().strip()
        if userPrompt == "latest":
            print(merged_data)
        elif userPrompt == 'top5':
            print(merged_data.head())
        elif userPrompt == "exit":
            print('Okie Dokie.. See ya later :)')
            break
        else:
            print("Oops! It seems there might be a small mistake with your command. Please choose the correct command.")


runScript()
