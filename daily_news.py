# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:47:51 2022

@author: josh.smith
"""

from bs4 import BeautifulSoup
import requests
import webbrowser
from automate_email import email_alert

def scrapin(url,user):
    res = requests.get(str(url),headers = user)
    res.status_code == requests.codes.ok
    #USED TO HALT A BAD DOWNLOAD
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))
    res_web = BeautifulSoup(res.text,'html.parser')
    return res_web
def webscrape(city):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    city = city +' weather'
    city=city.replace(' ','+')
    read = scrapin(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',headers)
    read_news = scrapin('https://www.allsides.com/',headers)
    try:
        location = read.select('#wob_loc')[0].getText().strip()  
        info = read.select('#wob_dc')[0].getText().strip() 
        weather = read.select('#wob_tm')[0].getText().strip()
        print(location+': ' + info + ' - ' + weather + ' degrees\n')

        hyper_set=[]
        title_set = []
        #compile list of titles from the entire website
        url = 'https://www.allsides.com'
        articles = read_news.find_all('a',class_='main-link')
        for article in articles:
            if len(title_set) < 5:    
                if url not in article['href']:
                    title_set.append(article.getText())
                    hyper_set.append(url+article['href'])
    except: 
        print('invalid search')
    return(hyper_set,title_set)

links,titles = webscrape(city)

user_agent={'User-agent': 'Mozilla/5.0'}

us_cases_web = scrapin('https://www.cdc.gov/poxvirus/monkeypox/response/2022/us-map.html',user_agent)
cases_web = scrapin('https://www.monkeypoxmeter.com/',user_agent)


center=cases_web.find_all('center')
us_cases = us_cases_web.find('span',class_='fs12 text-primary').getText().lstrip()


counter = 1
text_message = []
email_stuff = []
for title in zip(titles,links):
    news_print = '('+str(counter)+') '+title[0]+'\n' 
    email = '<pre>\n(<a href='+str(title[1])+'>_'+str(counter)+'_</a>) ' + title[0] +'</pre>'
    print(news_print)
    text_message.append(news_print)
    email_stuff.append(email)
    counter +=1
    

email_alert('Daily News', 'placeholder',','.join(email_stuff).replace(',',''), list_of_emails)


print('\nU.S. Cases\n------\n' + us_cases)
print('\n\nWorldwide\n------')
print(center[3].getText().replace('cases','cases\n').replace(')vs',') vs')+'\n')

print('Enter article number to open: \n')
x = input()

while x:
    open_article = links[int(x)-1]
    webbrowser.open(open_article)
    print('Now opening... '+open_article)
    print("\nInput another number or press enter to leave.\n")
    x=input()
print('Exiting...')
