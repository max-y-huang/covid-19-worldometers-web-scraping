"""===========================================================================
| COVID-19 WORLDOMETERS WEB SCRAPING
|   By: Max Huang
|   Last edited: May 3rd, 2020
|
| This program scrapes some COVID-19 data from worldometers.info/coronavirus
| and exports it as a CSV.
==========================================================================="""

import csv
import re
from bs4 import BeautifulSoup
from selenium import webdriver

def formatDatemAsNumber(datem):
  datem = re.sub(r'[^\d.]+', '', datem) # Get rid of unnecessary characters.
  return 'N/A' if datem == '' else datem

# Configure and start scraping.
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('log-level=3')
driver = webdriver.Chrome(options=options)  # chromedriver.exe must be located in PythonXX/Scripts.
driver.get('https://www.worldometers.info/coronavirus/')

# Find data table.
soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find(id='main_table_countries_today')
tbody = table.findAll('tbody')[0]
rows = tbody.findAll('tr', role='row')

#####################################################

# Create CSV header.
fieldNames = [
  'Country',
  'Total Cases',
  'Total Cases per Million',
  'Total Deaths',
  'Total Deaths per Million',
  'Total Tests',
  'Total Tests per Million'
]
outputFile = open('output.csv', 'w', newline='')
writer = csv.DictWriter(outputFile, fieldnames=fieldNames)
writer.writeheader()

# Loop through rows.
for r in rows:

  # Get row data.
  cols = r.findAll('td')

  # Only consider individual countries.
  if 'row_continent' in r['class']:
    continue
  if 'total_row_world' in r['class']:
    continue
  
  # Get entry values.
  fieldValues = [
    cols[0].text.strip(),
    formatDatemAsNumber(cols[1].text),
    formatDatemAsNumber(cols[8].text),
    formatDatemAsNumber(cols[3].text),
    formatDatemAsNumber(cols[9].text),
    formatDatemAsNumber(cols[10].text),
    formatDatemAsNumber(cols[11].text)
  ]

  # Write row to CSV.
  entry = {}
  for i in range(len(fieldNames)):
    entry[fieldNames[i]] = fieldValues[i]
  writer.writerow(entry)

outputFile.close()
print('\nExported data to output.csv!')
