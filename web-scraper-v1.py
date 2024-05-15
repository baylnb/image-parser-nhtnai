import requests
import os
#from requests.adapters import HTTPAdapter
#from tenacity import retry

def clear_all_cookies(session):
    session.cookies.clear()
    
def simple_request_handler_check():
    domains = ["nhentai"]
    tlds = ["com", "net"]
    
    session = requests.Session()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36 EdgA/115.0.1901.196',
    }
    
    session.headers.update(headers)
    
    #cookies = {
     #   'cf_clearance': removed
      #  'csrftoken': removed
       # }
    
    #for cookie_name, cookie_value in cookies.items():
     #   session.cookies.set(cookie_name, cookie_value)
      #  print(f"Session.Cookies var is: {session.cookies}, Cookie_Name var is: {cookie_name}, Cookie_Value var is: {cookie_value}")

    while True:
        counter = 0
        for domain in domains:
            for tld in tlds:
                if domain == "nhentai":
                    tld = "net"
                else: 
                    tld = "com"
                url = f"https://www.{domain}.{tld}"
                try:
                    response = session.get(url)
                    counter = counter + 1
                    print(f"Count: {counter}: New Line Status code for {url}: {response.status_code}")
                    if response.status_code == 403: 
                        #print(f"Requests to {domain} have the following headers:{response.request.headers}")
                        print(f"The cookies before: {session.cookies}")
                        clear_all_cookies(session)
                        print(f"The cookies after: {session.cookies}")
                except requests.exceptions.RequestException as e:
                    print(f"Error for {url}: {e}")
                else:
                    if counter >= 40:
                        break

            #print(response)

simple_request_handler_check()