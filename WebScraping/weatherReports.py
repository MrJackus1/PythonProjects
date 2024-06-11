#Create an app that asks for a location and returns a weather report for today.
#Scrape met office and check for invalid location.
from bs4 import BeautifulSoup
import requests


#Find location and return the 5 possible locations
mydivs = ''
count = 0
while len(mydivs) == 0:
    if count > 0:        
        print(f'{location} is invalid')
    location = input('Where do you want to search?: ')
    url = f'https://www.metoffice.gov.uk/search?query={location}'
    result = requests.get(url)
    doc = BeautifulSoup(result.text, 'html.parser')
    mydivs = doc.find_all("div", {"class": "location-results-box"})
    count =+ 1
      
#Extracting urls and titles from each div
urls = []
titles = []
for div in mydivs:
    links = div.find_all('a')    
    for link in links:
        href = link.get('href')
        title = link.get_text(strip=True)        
        urls.append(href)
        titles.append(title)

#Print out a list of the locations 
count = 1
for t in titles:
    print(f'''{str(count)}:----------------------\n {t}''')
    count += 1
    
#Take user input of 1-5 and return the url in a string
print('')
tempval = input('Enter 1-5 to choose your location: ')
tempval = int(tempval) - 1
x = 'https://www.metoffice.gov.uk/' + urls[tempval]

#Now scrape the weather report from the url produced by user input. 
url = x
result = requests.get(url)
doc = BeautifulSoup(result.text, 'html.parser')

selection = doc.find("li", {"id": "tabDay0"})

newSelect = selection.find("div", {"class": "off-screen"})

comments = newSelect.get_text()

#Gets the name of the location from the document itself. Allows you to search for things you shouldnt be able to. Paris, Norway ect.
newlocation = doc.find("input", {"id": "location-search-input"})
newlocation = newlocation['value']

print('')
print(f'The weather in, {newlocation} is: ')
print(comments[6:].title())
 

