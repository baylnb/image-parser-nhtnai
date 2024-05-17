import requests
from bs4 import BeautifulSoup

url = ""
response = ""

def get_url_prompt():
    global url
    print("Enter a url")
    url = input()


def test_200():
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
    }
    session.headers.update(headers)
    response = session.get(url)
    try:
        print(f"Status code for {url}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error for {url}: {e}")

def parse_html():
    #count number of elements tagged data-src= in the html file
    #choose path 
    #download logic








get_url_prompt()
test_200()