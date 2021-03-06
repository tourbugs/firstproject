
import datetime
import argparse
from bs4 import BeautifulSoup
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

def replace(URL):
    Str = ""
    for char in URL:
        if char>='a' and char <= 'z':
            Str +=char
        else:
            continue
    newStr1 = Str +'.txt'
    newStr2 = '.'+Str +'_temp.txt'
    return newStr1 ,newStr2

URL = args.u
CURL = URL.split('//')
CURL = CURL[-1]
Str,StrTemp = replace(CURL)
wordlist = args.w
fileName = args.f

ToSave = args.s
To_Print_300 = args.t
To_Print_200 = args.o

temp = open(wordlist,'r').read().split('\n')
urls =  list()

for line in temp:
    urls.append(URL + '/' + line)

try:
    checklist = [x for x in open(StrTemp,'r').read().split('\n')]
except:
    pass
realtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
with FuturesSession(max_workers=100) as session:
    re_location = set()
    li = []
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
                    print("Size:" ,all_response.headers.get('Content-Length'), end=" , ")
                    print(all_response.url,end=" >> ")
                    print(all_response.headers['Location'])
                    re_location.add(all_response.headers['Location'])
                    store = all_response.url.split('/')
                    check1 = "/" + str(store[-1]) + "/"
                    check2 = all_response.url + '/'
                    same = (all_response.headers['Location'])

                    if check1 == same or check2 == same:
                        newResponse = all_response.url +"/"
                        with FuturesSession() as session1:
                            r = session1.get(newResponse)
                            r = r.result()
                            soup = BeautifulSoup(r.text, 'html.parser')
                            ifmeta = soup.find("meta")
                            if ifmeta.has_attr('content') and ifmeta.has_attr('http-equiv'):
                                if "refresh" == (soup.meta.get('http-equiv')):
                                    metaURL= (soup.meta.get('content'))
                                    if metaURL is not None:
                                        filtering = metaURL.split('=')
                                        filterURL = filtering[-1]
                                        newR = session1.get(filterURL)
                                        newR = newR.result()
                                        print("->",newR.status_code, end=" , ")
                                        print(newR.url)
                            else:
                                print("->",r.status_code, end=" , ")
                                print(r.url)
                                                  
        elif To_Print_200:
            if all_response.status_code in [200]:
                if ToSave:
                    with open(fileName,'a') as wf:
                        wf.write(all_response.url + "\n")           
                store = all_response.url.split('.')
                check = store[-1]
                if check in ['json','ico','xml','txt']:       
                    print("status:",all_response.status_code,end=" , ")
                    print("Size:" ,all_response.headers.get('Content-Length'), end=" , ")
                    print(all_response.url)
                    continue
                soup200 = BeautifulSoup(all_response.text, 'html.parser')
                response = list(([tag.name for tag in soup200.find_all()]))
                if response not in li:
                    li.append(response) 
                    try:
                        if all_response.url not in checklist:
                            with open(StrTemp,'a') as file:
                                file.write(all_response.url + "\n")
                            with open(Str,'a') as printing:
                                printing.write("New Response "+realtime +"\t"+ all_response.url + "\n")
                            print("new response",end=" ")
                            print("status:",all_response.status_code,end=" , ")
                            print("Size:" ,all_response.headers.get('Content-Length'), end=" , ")
                            print(all_response.url)
                            continue
                    
                    except:
                        with open(StrTemp,'a') as file:
                            file.write(all_response.url + "\n")
                        with open(Str,'a') as printing:
                            printing.write(realtime +"\t" + all_response.url + "\n")

                    print("status:",all_response.status_code,end=" , ")
                    print("Size:" ,all_response.headers.get('Content-Length'), end=" , ")
                    print(all_response.url)
                    
                # for link in bs.BeautifulSoup(all_response.text, 'html.parser',parseOnlyThese=SoupStrainer('meta')):
                #      if "refresh" == link.get('http-equiv'):
                #         metaURL= link.get('content')
                #         filtering = metaURL.split('=')
                #         filterURL = filtering[-1]
                #         newR = requests.get(filterURL)
                #         print("->",newR.status_code, end=" , ")
                #         print(newR.url)        
        else:
            if all_response.status_code in [301,302]:
                if all_response.headers['Location'] not  in re_location:
                    print("status:",all_response.status_code,end=" , ")
                    print("Size:" ,all_response.headers.get('Content-Length'), end=" , ")
                    print(all_response.url,end=" -->> ")
                    print(all_response.headers['Location'])
                    re_location.add(all_response.headers['Location'])
            elif all_response.status_code in [200]:   
                print("status:",all_response.status_code,end=" , ")
                print("Size:" ,all_response.headers.get('Content-Length'), end=" , ")
                print(all_response.url)
            else:
                print("status:",all_response.status_code,end=" , ")
                print("Size:" ,all_response.headers.get('Content-Length'), end=" , ")
                print(all_response.url)   