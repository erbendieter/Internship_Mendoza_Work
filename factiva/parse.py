# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 14:41:04 2017

@author: Dieter Erben
"""
import requests, datetime, itertools, time
import urllib3, urllib
urllib3.disable_warnings()
import pandas as pd
from bs4 import BeautifulSoup
url='https://global-factiva-com.proxy.library.nd.edu/services/ajaxservice.aspx'
headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Cookie': "__hstc=246422427.352f90bac35d329ce755c4e9be3e303d.1498069331758.1498069331758.1498069331758.1; hubspotutk=352f90bac35d329ce755c4e9be3e303d; __utma=3838575.1191629643.1490212569.1500394826.1500418214.5; __utmz=3838575.1500418214.5.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); libraryndedu=10.16.164.78.1500573753811387; ezproxylib=So4SuuOFApxqEjK; _ga=GA1.2.1191629643.1490212569; _gid=GA1.2.2130201456.1500660381; LSLogin=FP%5FUT=B&GL%5FUT=B&FP%5FRS=0099990000&GL%5FRS=0099990000&FP%5FCL=VO&GL%5FCL=VO; login=; Mds=; Search=; Admn=; General=; s_cc=true; s_sq=%5B%5BB%5D%5D",
        'Content-Type': 'application/x-www-form-urlencoded'
        }
payload='serviceType=factiva.com.ui.services.SearchResultsService&_XFORMSESSSTATE=AAx7Mjp7MTQ0OnszNzp7MzU6MCwxMDU6MSw4OltdLDVkAQU3ODoxLDExMGICODlIAwEwOnsxcAEAAjY6W119LDE6MCwyOjAsMzoiIiw0fAJwCG4DLDd2ATM5dAADNDk6MCw1cQA2cgAxMnICMTV0AAQyNTo5LDUymAecDXUJNokDN2gJAAI1MDoiKGNhbGwgcmVwb3J0IG9yICk5AHN8AQZGRklFQyAwMzEpMAAONDEpIG5vdCAoUlNUPXNmYndsA2wBD3BybikgYW5kIHJlPVVTQSIsN4oUMTCNHjSoEwwxNDoiMjAwMDAxMDEiLDiJAzbIAwIzOjAsOIMUMTE1fhY5N34mMTZtATSOIzk4bQQxYQI5lgA2MXQodQIycQAzcSo0hAEGMzoyLDExOnswbAgnMwUwLDRkJgo6MCw2OjIsNzowfSwyaS0xegIyNGwGAjc6MSw0eQE1TxUiLDWFMDeJMDZtAzedLzaQDH8BMTE3fBEFNTc6WzBdLDiWAzEwdS05dQg0oQIxnTMxbQ00aRI4bgMxMXoEMTCYOgYxOTpbOV0sNjB1CTiVADm0Q2EjOXIAODZRGTmdITZ9BzJmCTEzmD19AzGBCTSAAgMzNjoxLDaIAQQ1NjoxMCw2kQM3lgAxMIgrnQc5jUQ5bkIxMIk2M5EqMm0TNVQsKLwGUDYMOiIyMSBKdWx5IDIwMTcgfCYDNyJ9LDI2mlxbXWkOMLhcjQk0gA2fLyIiLJgRiCmcPIwRnSMyZWAzbSQ0mAbsWimwCHNbOV0smRIzmSMyVEQocQI1mUg0TQIiZmwwLLFdNYwouU83mQYzgRA2ehs2NHA9iUsxjlEyOHUvM3E7NIECNpUAMWUiMrwEgS80ID%2FxDDFpSzKkSykdCjV5KTaJJjdlPjN5BDSJHDNgGnBIj0gwLDFgQEiQAVtdLDeIPK2NMpAFAzEzOjksMpkxM5UAMpVKM4UyNI0BNXBNsUYzeVY1bSAxaIkDNDM6MSw3REMAJCJ9LG46IlJldHVybiB0byBIZWFkbGluZXMifX0sMDp7VToiL2hhL2RlZmF1bHQuYXNweCIsMUhklHIBMjoiU4lCIkSlCCJdLDQ6ImVuIiw17XYx4aAxmIlUIApid2FzaWtAbmQuZWR1ZAUDIjE2Iiw2YKcAJyI3MEU0MTEwNjNFRDgwMTAzRTEwMDA2RDI2NEM4MzI4MUFGRjBEMEJDMDI0MEU4MDA4fDIyfDV8MCkHADV8NSo4ACwsAAo1fC0xfDIwNDh8MTAicBsPMDoiY29leGUsMCwwO2NvdHJuhAEAEWVudHdzanAsMjtjb2N1cywwIiwxOiJkdG1vbiwwO0JFSUpYfASUFwEwMDg2aSU3hBgACTU3QzIzMTAwNzQwNDAzMzAwMERFNHwwMjEwMHABdKZOAjQ3YALkAo0DMqwYlhIyMnonMX1xO3t5NjBsnIzLAzEsMDoxfXCiBjAsMTM6IkFsbGjLjDFsOwIyOjEsM2YEMjSMCAQsMToxMiwyhAKQMghbezA6ImRvdGNvbXAabAMBIjgifXTVAjc6e30sU7syMixweFJMe31MQAc4OiJ1bm5vdGRhSEV8SQM3OiJtYm1AKAo4OiJtYm0wLTAifX19EQAALgcAAA%3D%3D&_XFORMSTATE=AAd7MTp7Mzc6ezM1OjAsMTA1OjEsODpbXSw1ZAEFNzg6MSwxMTBiAjg5SAMBMDp7MXABAAI2OltdfSwxOjAsMjowLDM6IiIsNHwCcAhuAyw3dgEzOXQAAzQ5OjAsNXEANnIAMTJyAjE1dAAEMjU6OSw1MpgHnA11CTaJAzdoCQACNTA6IihjYWxsIHJlcG9ydCBvciApOQBzfAEGRkZJRUMgMDMxKTAADjQxKSBub3QgKFJTVD1zZmJ3bANsAQ9wcm4pIGFuZCByZT1VU0EiLDeKFDEwjR40qBMMMTQ6IjIwMDAwMTAxIiw4iQM2yAMCMzowLDiDFDExNX4WOTd%2BJjE2bQE0jiM5OG0EMWECOZYANjF0KHUCMnEAM3EqNIQBBjM6MiwxMTp7MGwIJzMFMCw0ZCYKOjAsNjoyLDc6MH0sMmktMXoCMjRsBgI3OjEsNHkBNU8VIiw1hTA3iTA2bQM3nS82kAx%2FATExN3wRBTU3OlswXSw4lgMxMHUtOXUINKECMZ0zMW0NNGkSOG4DMTF6BDEwmDoGMTk6WzldLDYwdQk4lQA5tENhIzlyADg2URk5nSE2fQcyZgkxM5g9fQMxgQk0gAIDMzY6MSw2iAEENTY6MTAsNpEDN5YAMTCIK50HOY1EOW5CMTCJNjORKjJtEzVULCi8BlA2DDoiMjEgSnVseSAyMDE3IHwmAzcifSwyNppcW11pDjC4XI0JNIANny8iIiyYEYgpnDyMEZ0jMmVgM20kNJgG7FopsAhzWzldLJkSM5kjMlREKHECNZlINE0CImZsMCyxXTWMKLlPN5kGM4EQNnobNjRwPYlLMY5RMjh1LzNxOzSBAjaVADFlIjK8BIEvNCA%2F8QwxaUsypEspHQo1eSk2iSY3ZT4zeQQ0iRwzYBpwSI9IMCwxYUA0jR03iDytjTKQBQMxMzo5LDKZMTOVADKVSjOFMjSNATVwTbFGM3lWNW0gMWiJCjQzOjEsNzE6IiJ9fX0RAADlBAAA&hs={pg}&ipccs=0&ht=Advanced&ipid=&ipin=&ipgi=False&isst=LegacySavedSearch&scs=%5B%5D&xsc=%5B%5D&sls=%5B%5D&xsls=%5B%5D&als=%5B%5D&xaul=%5B%5D&xil=%5B%5D&ils=%5B%5D&xrl=%5B%5D&rls=%5B%5D&xnl=%5B%5D&nls=%5B%5D&xpl=%5B%5D&pls=%5B%5D&aus=%5B%5D&cos=%5B%5D&xau=%5B%5D&xco=%5B%5D&cls=%5B%5D&xcl=%5B%5D&pes=%5B%5D&xpe=%5B%5D&nss=%5B%5D&xns=%5B%5D&ins=%5B%5D&xin=%5B%5D&res=%5B%5D&xre=%5B%5D&ipcl=%5BEN%5D&iadmio=False&ist=Advanced&iceu=0&fess=%5B%5D&iefs=%5B%5D&sicr=0&aicr=0&cicr=0&nsicr=0&iicr=0&ricr=0&pecr=0&flagBox=lo&scrAllPub=%7B14%3A1%2C0%3A0%2C11%3A%22P%7C%22%2C12%3A0%2C4%3A0%2C5%3A0%2C6%3A0%2C7%3A0%2C8%3A%22All+Publications%22%2C10%3A0%7D&scrAllWeb=%7B14%3A3%2C0%3A0%2C11%3A%22W%7C%22%2C12%3A0%2C4%3A0%2C5%3A0%2C6%3A0%2C7%3A0%2C8%3A%22All+Web+News%22%2C10%3A0%7D&scrAllPic=%7B14%3A2%2C0%3A0%2C11%3A%22I%7C%22%2C12%3A0%2C4%3A0%2C5%3A0%2C6%3A0%2C7%3A0%2C8%3A%22All+Pictures%22%2C10%3A0%7D&scrAllMlt=%7B14%3A5%2C0%3A0%2C11%3A%22M%7C%22%2C12%3A0%2C4%3A0%2C5%3A0%2C6%3A0%2C7%3A0%2C8%3A%22All+Multimedia%22%2C10%3A0%7D&scrAllBlg=%7B14%3A6%2C0%3A0%2C11%3A%22B%7C%22%2C12%3A0%2C4%3A0%2C5%3A0%2C6%3A0%2C7%3A0%2C8%3A%22All+Blogs%22%2C10%3A0%7D&searchBuilder=1&isnf=%7B%7D&atx=&otx=&ntx=&htx=&assistedSearch=1&ftx={term}&inasm=false&sbFTQSize=2048&dr=Custom&frdt={date_from}&dateFrom_txb={date_from}&dateFrom_extc_ClientState=%7B%22CalendarPosition%22%3A1%2C%22CalendarDateDisplayFormat%22%3A%22d+MMMM+yyyy%22%2C%22CalendarMonthYearDisplayFormat%22%3A%22MMM%2C+yyyy%22%7D&dateFrom_extc__MaskedEditExtender_ClientState=&todt={date_to}&dateTo_txb={date_to}&dateTo_extc_ClientState=%7B%22CalendarPosition%22%3A0%2C%22CalendarDateDisplayFormat%22%3A%22d+MMMM+yyyy%22%2C%22CalendarMonthYearDisplayFormat%22%3A%22MMM%2C+yyyy%22%7D&dateTo_extc__MaskedEditExtender_ClientState=&frd=&frm=&fry=&tod=&tom=&toy=&dfmt=CCYYMMDD&isrd=None&srcNmOnly=on&excDiscSrcs=on&cop=Or&sop=Or&iop=Or&rop=Or&srcNmOnlylk=on&excDiscSrcslk=on&sfd=&istesfn=True&istesfn_bool=True&ister=True&ister_bool=True&isteo=True&isteo_bool=True&hso=PublicationDateMostRecentFirst&requiredParts=disc|tabs|nf|sbnf|ss|ssb|du'

date0=datetime.date(2000, 1, 1)
date1=datetime.date(2017, 7, 19)
keywords=['(call report or call reports or FFIEC 031 or FFIEC 041)', 'Y-9C']
sources=[' not (RST=sfbw or RST=prn)', ' and (RST=sfbw or RST=prn)', ' and rst=tdjw']
usa=' and re=USA'
terms=[''.join(x)+usa for x in itertools.product(keywords,sources)]
len_terms=len(terms)

#for d in range(0, (date1-date0).days+1):
#    now=date0+datetime.timedelta(d)
df = pd.DataFrame(columns=['link','title','source','date','snippet'])
for term_idx, term in enumerate(terms[1:]): 
    offset=0
    hits=1
    while offset < hits:
        print("[Term: {}/{}] [Page: {}/{}]".format(term_idx+1, len_terms, offset//100+1, hits//100+1))
        r=requests.post(url, headers=headers, data=payload.format(term=urllib.parse.quote(term), date_from=date0.strftime('%Y%m%d'), date_to=date1.strftime('%Y%m%d'), pg=offset), verify=False)
        
        #formstate= urllib.parse.quote(r.json()['formState'])
        soup = BeautifulSoup(r.json()['headlinesHtml'],'lxml')
        
        headlines = soup.find_all('tr',class_='headline')
        hits = int(''.join(soup.find('span', class_='resultsBar').text.split(' of ', maxsplit=1)[1].split(','))) if len(headlines) else 0
        for headline in headlines:
            a=headline.find('a',class_='enHeadline')
            title = a.get_text(strip=True)
            link = a.get('href')
            div=headline.find('div',class_="leadFields")
            src=div.contents[0].get_text(strip=True)
            date=str(div.contents[1])
            snippet=headline.find('div',class_='snippet').get_text(strip=True)
            df=df.append(pd.Series({'link':link,'title':title,'source':src,'date':date,'snippet':snippet,'term':term}), ignore_index=True)
        offset+=100
        time.sleep(.5)
        

#with open('resp.htm', 'w', encoding='utf8') as f:
#    f.write(r.text)

f_dates=lambda x: datetime.datetime.strptime(x.split(",")[-3], " %d %B %Y")
f_words=lambda x: x.split(",")[-2]
f_links=lambda x: x[32:57]
words = df.date.apply(f_words)
df = df.assign(date=df.date.apply(f_dates))
df = df.assign(words = [int(x[:-6]) for x in words])
df = df.assign(access = df.link.apply(f_links))
df = df[['access','title','source','date','snippet','term','words']]

#df = pd.DataFrame(columns=['link','title','source','date','snippet'])

agg=df.groupby(['term', 'date']).size()
agg.name='hits'

df.to_csv('output.csv',index=False)
agg.to_csv('summary.csv',header=True)
