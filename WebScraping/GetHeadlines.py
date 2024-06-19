'''
Create a program that searches a few news sites and returns the first headline from them. World news.

'''

from bs4 import BeautifulSoup
import requests
import re

def bbcNews():
    url = 'https://www.bbc.co.uk/news/world'
    
    result = requests.get(url)
    doc = BeautifulSoup(result.text, 'html.parser')
    mydivs = doc.find_all('div', class_=re.compile(r'\bUncontainedPromoWrapper\b'))
    Title = mydivs[0].find('p', class_=re.compile(r'-PromoHeadline'))
    Comment = mydivs[0].find('p', class_=re.compile(r'-Paragraph'))
    
    Title = Title.string
    Comment = Comment.string
    return f'''Latest from BBC news:\nHeadline: "{Title}"\nText:     "{Comment}"'''


#Search for a headline from cnn world

def cnnNews():
    url = 'https://edition.cnn.com/world'
    
    request = requests.get(url)
    doc = BeautifulSoup(request.text, 'html.parser')    
    mydivs = doc.find_all('a', class_=re.compile(r'container__link container__link--type-article container_lead-plus-headlines__link')) 
    Title = mydivs[1].find('span', class_=re.compile(r'container__headline-text'))
    if mydivs:        
        return f'''Latest from CNN news:\nHeadline: "{Title.string}"'''
    else:
        return f'''Latest from CNN news:\nHeadline: Failed getting headline '''

#Search for a headline from aljazeera


def aljazNews():
    url = 'https://www.aljazeera.com/'
    request = requests.get(url)
    doc = BeautifulSoup(request.text, 'html.parser') 
    mydivs = doc.find_all('div', class_=re.compile(r'home-page-article-list'))    
    Title = mydivs[0].find('h3', {"class": "article-card__title"})
    Comment = mydivs[0].find('p', {"class": "article-card__excerpt"})
    
    
    return f'''Latest from Aljazeera news:\nHeadline: "{Title.string}"\nText:     "{Comment.string}"'''

print("Printing news headlines: \n")
print(bbcNews()+'\n')
print(cnnNews()+'\n')
print(aljazNews()+'\n')
  
    
    
     