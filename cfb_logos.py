# File: cfb_logos.py
# CS 5010
# Homework: Python and Web Scraper
# Name (Computing ID): Drew Haynes (rbc6wr) and Sarah Rodgers (pjk2wq)

############
## Part 1 ##
############

# Import libraries
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

# Collect ESPN's FPI Page (Page containing links to all FBS teams)
page = requests.get('https://www.espn.com/college-football/fpi/_/season/2017')

# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')

# Pull all text from the Table__TBODY div
team_table = soup.find(class_='Table__TBODY')

# Pull text from all instances of data-clubhouse-uid attribute
# within Table__TBODY div
all_team_items = team_table.find_all(attrs={"data-clubhouse-uid": True}) 

team_name = []
logo = []

# Loop through the all_team_items element and get the logo links
for team in all_team_items:
        team_id = team['data-clubhouse-uid'].partition('t:')[2]
        team_logo = "https://a.espncdn.com/combiner/i?img=/i/teamlogos/ncaa/500/"\
            + team_id + ".png&h=50&w=50"
        team_name.append(team.get_text())
        logo.append(team_logo)
    
        
# Pull all text from the Table__Scroller class then get all the text from the Table__TR Table__TR--sm Table__even class
fpi_table = soup.find(class_='Table__Scroller')
team_records = fpi_table.find_all(class_='Table__TR Table__TR--sm Table__even')

# Create an empty list
record = []
fpi = []
rank = []

# Loop through the team_records element and get the text from the first three contents
for team in team_records:
    record.append(team.contents[0].get_text())
    fpi.append(float(team.contents[1].get_text()))
    rank.append(int(team.contents[2].get_text()))

# Store the resulting listing into a dataframe
df = pd.DataFrame({'Team':team_name, 'Record':record,'Rank':rank,'FPI':fpi,
                   'Logo':logo})

############
## Part 2 ##
############

# Export to excel
df.to_excel("cfb_logos.xlsx", index = False)

############
## Part 3 ##
############

# Create a list of teams that did not win a game
no_wins = []
for i in range(0,len(df)):
    # Using regular expression to find teams that have a record beginning with 0
    if (re.search("^0", df["Record"][i]) is not None) == True:
        no_wins.append(df["Team"][i])
print(no_wins)

# Get the number of wins of each team
wins = []
for i in df["Record"]:
    # Get the value prior to the hypen
    wins.append(int(i.split("-")[0]))

df["Wins"] = wins

# Plotting the number FPI vs number of wins
fig, ax = plt.subplots(figsize=(20, 15))
ax.scatter(df.FPI, df.Wins)
plt.xticks(np.arange(-35, 40, 5))
plt.ylabel("Number of wins")
plt.xlabel("FPI")
plt.title("Number of wins vs FPI")
# Adding Regression Line
m, b = np.polyfit(df.FPI, df.Wins, 1)
plt.plot(df.FPI, m*df.FPI + b)

# Using the logos as icons for the plot of FPI vs number of wins
for x, y, path in zip(df.FPI, df.Wins, df.Logo):
    ab = AnnotationBbox(OffsetImage(plt.imread(path)), (x, y), frameon=False)
    ax.add_artist(ab)
    
# Get the number of losses of each team
losses = []
for i in df["Record"]:
    # Get the value after to the hypen
    losses.append(int(i.split("-")[1]))

df["Losses"] = losses

# Average number of games this season
df["Total Games"] = df["Losses"] + df["Wins"]

avg_games = round(sum(df["Total Games"]/len(df)),0)
print("The average number of games was", str(avg_games))