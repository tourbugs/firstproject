
import requests
from requests_futures.sessions import FuturesSession

URL = 'https://video-api.cartoonnetwork.com'

temp = open('qwerty1.txt','r').read().split('\n')

urls =  list()

for line in temp:
    urls.append(URL + '/' + line)
    

    
with FuturesSession(max_workers=100) as session:
    reallocation = set()
    futures = [session.get(url ,allow_redirects=False) for url in urls]
    for future in futures:
        all_response = future.result()
        if all_response.status_code in [301,302]: 
            if all_response.headers['Location'] not in reallocation:
                print("status:",all_response.status_code,end=" , ")
                print("Size:" ,all_response.headers['Content-Length'], end=" , ")
                print(all_response.url,end=" >> ")
                print(all_response.headers['Location'])
                reallocation.add(all_response.headers['Location'])
        else:
            print("status:",all_response.status_code,end=" , ")
            print("Size:" ,all_response.headers['Content-Length'], end=" , ")
            print(all_response.url)
        
 
        
    