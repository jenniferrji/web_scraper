import requests
from bs4 import BeautifulSoup

def scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    # ...add your scraping logic here...
    return soup

if __name__ == "__main__":
    url = "https://example.com"
    data = scrape(url)
    print(data.prettify())
