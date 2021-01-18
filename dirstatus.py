import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)
import datetime
import argparse
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession
parser = argparse.ArgumentParser()
parser.add_argument("-u", action='store', type=str, default=None, nargs='+', help="Enter All, and at least one URL separate by space")
parser.add_argument('-l','--urllist', action='store', type=str, default=None,  help="URL List file")
parser.add_argument("-w", action='store', type=str, required=True,  help="Enter Wordlist")
parser.add_argument('-i','--include', action='store', nargs='+', type=int, default=None, help="include-status separate by space (eg.: -x 200 301 302)")
parser.add_argument('-x','--exclude', action='store', nargs='+', type=int, default=None, help="exclude-status separate by space (eg.: -x 404 400)")
parser.add_argument('-s','--success', action='store_true',default=False, help="Successful responses (200–299)")
parser.add_argument('-r','--redirects', action='store_true',default=False, help="Redirects (300–399)")
parser.add_argument('--reresponse', action='store_true',default=False, help="Redirects Response")

args = parser.parse_args()


def time():
    realtime = datetime.datetime.now().strftime("%H:%M:%S")
    return realtime
def banner(i):
    print()
    print(f'\033[0;33mTarget: \033[0;36m{i}')
    print()
    print(f'\033[1;35m[{time()}] ',end="    ")
    print('\033[33mStarting:')
 
def redirectResponse(new,li200,li):
    li400 = [i for i in range(400,500)]
    with FuturesSession() as session1:
            reResponse = session1.get(new.url)
            reResponse = reResponse.result()
            if reResponse.status_code not in li400:
                otherResponse(reResponse,li200,li)

def redirectLocation(r,li200,li,re_location):
    if r.headers['Location'] in re_location:
        return
    re_location.add(r.headers['Location'])
    a = r.status_code
    b = r.headers.get('Content-Length')
    c = r.url
    h = r.headers['Location']
    print(f'\033[1;35m[{time()}] ',end="    ")
    print('\033[33m'"%-4d %-9s %s --> %s" %(a,b,c,h))
    if restatus:
        redirectResponse(r,li200,li)

def otherResponse(r,li200,li):
    soup200 = BeautifulSoup(r.text, 'html.parser')
    newlist = list(([tag.name for tag in soup200.find_all()]))
    if newlist not in li:

        li.append(newlist) 
        a = r.status_code
        b = r.headers.get('Content-Length')
        c = r.url
        if r.status_code in li200:
            print(f'\033[1;35m[{time()}] ',end="    ")
            print('\033[32m'"%-4d %-9s %s" %(a,b,c))
        else:
            print(f'\033[1;35m[{time()}] ',end="    ")
            print('\033[31m'"%-4d %-9s %s" %(a,b,c))
       

def request(ur,i):
    try:
        banner(i)
        # li =[] list is used for storing each page tag name  for comparing with other in def otherResponse(r)
        li = []
        # re_location used in def redirectLocation() to check each response headers [location] must be unique
        re_location = set()
        with FuturesSession(max_workers=50) as session:
            futures = [session.get(url ,allow_redirects=False) for url in ur]
            li300 =[x for x in range(300,400)]
            li200 =[x for x in range(200,300)]
            for future in futures:
                Response = future.result()
                if includeToprint is not None:
                    if Response.status_code in includeToprint:
                        if Response.status_code in li300:
                            redirectLocation(Response,li200,li,re_location)
                        else:
                            otherResponse(Response,li200,li)
                elif excludeToprint is not None:
                    if Response.status_code not in excludeToprint:
                        if Response.status_code in li300:
                            redirectLocation(Response,li200,li,re_location)
                        else:
                            otherResponse(Response,li200,li)
                elif okResponse:
                    if Response.status_code in li200:
                        otherResponse(Response,li200,li)
                elif redirect:
                    if Response.status_code in li300:
                        redirectLocation(Response,li200,li,re_location)
                else:
                    if Response.status_code in li300:
                        redirectLocation(Response,li200,li,re_location)
                    else:
                        otherResponse(Response,li200,li)
        li.clear()
        re_location.clear()

    except:
        print()
        print('\033[31mInvaild URL')
    finally:
        print()
        print('\033[33m[ TASK COMPLETED ]')



def checkGivenURLandTextFile(u,t,l):
    if u is not None:
        url =  list()
        temp = open(t,'r').read().split('\n')
        for i in u:
            if i[-1] == '/':
                for line in temp:
                    url.append(i +line)
            else:
                for line in temp:
                    url.append(i +'/'+line)
            request(url,i)
            url.clear()
    elif l is not None:
        url =  list()
        temp = open(t,'r').read().split('\n')
        presenturl = open(l,'r').read().split('\n')
        for i in presenturl:
            if i[-1] == '/':
                for line in temp:
                    url.append(i+line)
            else:
                for line in temp:
                    url.append(i +'/'+line)
            request(url,i)
            url.clear()



includeToprint = args.include
excludeToprint = args.exclude
restatus = args.reresponse       
redirect = args.redirects
okResponse = args.success
urlslist = args.urllist
URL = args.u
wordlist = args.w

urls =checkGivenURLandTextFile(URL,wordlist,urlslist)



        

        
    