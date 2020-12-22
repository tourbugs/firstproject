import argparse
import requests
from requests_futures.sessions import FuturesSession
parser = argparse.ArgumentParser()
parser.add_argument("-u", action='store', type=str, required=True, help="Enter URL")
parser.add_argument("-w", action='store', type=str, required=True,  help="Enter Wordlist")
parser.add_argument("-f", action='store', type=str, help="New file name")
parser.add_argument("-s", action='store_true',default=False, help="save")
parser.add_argument("-t", action='store_true',default=False, help="To print 300 response")
parser.add_argument("-o", action='store_true',default=False, help="To print 200 response")
args = parser.parse_args()

URL = args.u
wordlist = args.w
fileName = args.f

ToSave = args.s
To_Print_300 = args.t
To_Print_200 = args.o

temp = open(wordlist,'r').read().split('\n')
urls =  list()

for line in temp:
    urls.append(URL + '/' + line)
    
with FuturesSession(max_workers=100) as session:
    re_location = set()
    futures = [session.get(url ,allow_redirects=False) for url in urls]
    for future in futures:
        all_response = future.result()
        if To_Print_300:
            
            if all_response.status_code in [301,302]:
                if all_response.headers['Location'] not  in re_location:
                    if ToSave:
                        with open(fileName,'a') as wf:
                            wf.write(all_response.url + "-->>"+ all_response.headers['Location'] +"\n")
                    print("status:",all_response.status_code,end=" , ")
                    print("Size:" ,all_response.headers['Content-Length'], end=" , ")
                    print(all_response.url,end=" >> ")
                    print(all_response.headers['Location'])
                    re_location.add(all_response.headers['Location'])
#                     check = all_response.url +'/'
#                     same = (all_response.headers['Location'])
#                     print("check:",check)
#                     print(type(check))
#                     print("same",same)
#                     print(type(same))
#                     if check == same:
#                         r = requests.get(all_response.headers['Location'])
#                         print("same")
        elif To_Print_200:
            if all_response.status_code in [200]:
                if ToSave:
                    with open(fileName,'a') as wf:
                        wf.write(all_response.url + "\n")
                print("status:",all_response.status_code,end=" , ")
                print("Size:" ,all_response.headers['Content-Length'], end=" , ")
                print(all_response.url)
        else:
            if all_response.status_code in [301,302]:
                if all_response.headers['Location'] not  in re_location:
                    print("status:",all_response.status_code,end=" , ")
                    print("Size:" ,all_response.headers['Content-Length'], end=" , ")
                    print(all_response.url,end=" -->> ")
                    print(all_response.headers['Location'])
                    re_location.add(all_response.headers['Location'])
            elif all_response.status_code in [200]:   
                print("status:",all_response.status_code,end=" , ")
                print("Size:" ,all_response.headers['Content-Length'], end=" , ")
                print(all_response.url)
            else:
                print("status:",all_response.status_code,end=" , ")
                print("Size:" ,all_response.headers['Content-Length'], end=" , ")
                print(all_response.url)
        
        
Heloo wlwkjkaj
kaksnd
        
    
