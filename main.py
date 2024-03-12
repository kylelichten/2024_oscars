import requests
import csv
import re
from bs4 import BeautifulSoup

URL = "https://www.oscars.org/oscars/ceremonies/2024"
HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36" }
INDIVIDUAL_CATEGORIES = ["Actor in a Leading Role", "Actor in a Supporting Role", "Actress in a Leading Role", "Actress in a Supporting Role", "Music (Original Song)"]

result = requests.get(URL, headers=HEADERS, timeout=20)
soup = BeautifulSoup(result.text, "html.parser")

print(result.status_code)

# Create a CSV file and write the header
with open('oscars_2024.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Category', 'Winner or Nominee', 'Film Name', 'Nominee Names'])

    # Find the awards section
    awards_section = soup.find('div', class_='quicktabs-tabpage')

    # Find all the sections containing categories
    category_sections = awards_section.find_all('div', class_='view-grouping')

    # Iterate through each category section
    for category_section in category_sections:

        # Extract the category name
        category_name = category_section.find('h2').text.strip()

        # Extract films, winners, and nominees
        nominees = category_section.find_all('h4', class_='field-content')
        contents = category_section.find_all('div', class_='views-field views-field-title')

        # Set counter to determine winner; winner will appear 1st
        counter = 1

        # Iterate through films and winners/nominees
        for content, nominee in zip(contents, nominees):

            if category_name in INDIVIDUAL_CATEGORIES:
                nominee_names = nominee.text.strip()
                if category_name == "Music (Original Song)":
                    pattern = r'from\s(.*?);'
                    match = re.search(pattern, content.text.strip())
                    if match:
                        film_name = match.group(1).strip()
                    else:
                        film_name = None
                else:
                    film_name = content.text.strip()
            else:
                film_name = nominee.text.strip()
                nominee_names = content.text.strip()

            # The first entry is the winner
            winner_or_nominee = 'Nominee'
            if counter == 1:
                winner_or_nominee = 'Winner'

            counter += 1
            writer.writerow([category_name, winner_or_nominee, film_name, nominee_names])
            print(f"{category_name}, {winner_or_nominee}, {film_name}, {nominee_names}")

print("CSV file created successfully.")
