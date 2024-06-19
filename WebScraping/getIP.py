#Create a program which scrapes http://whatsmyip.strath.ac.uk/ and returns your ip and some other info.
#Try and use a class

#import libs
from bs4 import BeautifulSoup
import requests

#vars
link = 'http://whatsmyip.strath.ac.uk/'

#functions
def getPage(url):
    url = "http://whatsmyip.strath.ac.uk/"
    payload = ""
    headers = {
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://www.google.com/"
    }

    response = requests.request("GET", url, data=payload, headers=headers)
    doc = BeautifulSoup(response.text, 'html.parser')
    doc = doc.find_all("td", {"class": "v"})
    return doc

def getIP(IP=True, DNS=False):
    docu = getPage(link)
    if IP == True and DNS == False:
        ip = docu[0].find('span')
        return ip.text
    elif IP == True and DNS == True:
        ip = docu[0].find('span')
        ip = ip.text
        dns = docu[1].text
        return ip, dns
    elif IP == False and DNS
        dns = docu[1].text
        return dns
    else:
        return print('Wrong usage. Both IP and DNS are set to false.')

#Code
print(getIP(IP=True, DNS=True))
