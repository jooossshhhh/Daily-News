# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:47:51 2022

@author: josh.smith
"""

from bs4 import BeautifulSoup
import requests
import webbrowser
from automate_email import email_alert

#function to scrape information from the web using only a url and user agent
def scrapin(url,user):
    #get information from url
    res = requests.get(str(url),headers = user)
    res.status_code == requests.codes.ok
    #USED TO HALT A BAD DOWNLOAD
    try:
        res.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))
    #parse the result
    res_web = BeautifulSoup(res.text,'html.parser')
    return res_web
def webscrape(city):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    #takes input and makes it usable for the google link
    city = city +' weather'
    city=city.replace(' ','+')
    #scrape two websites
    read = scrapin(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',headers)
    read_news = scrapin('https://www.allsides.com/',headers)
    try:
        #get information about the weather then pice it together for return
        location = read.select('#wob_loc')[0].getText().strip()  
        info = read.select('#wob_dc')[0].getText().strip() 
        weather = read.select('#wob_tm')[0].getText().strip()
        print(location+': ' + info + ' - ' + weather + ' degrees\n')
        weather = location.replace(' ',', ')+': ' + info + ' - ' + weather + ' degrees\n'
        
        #make list of the hyperlinks and titles for the articles we are finding
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
    return(hyper_set,title_set,weather)

links,titles,weather_info = webscrape(city)

user_agent={'User-agent': 'Mozilla/5.0'}

#find quote of the day
quotes_web = scrapin('https://www.brainyquote.com/quote_of_the_day',user_agent)
try:
    qotd= quotes_web.find('div',class_='grid-item qb clearfix bqQt').getText()
except Exception as err:
    #if theres an error, send the error to your email for later fixing
    qotd = '\nNo quote today.'
    email_alert('Error with qotd','File: '+__file__+'\n'+str(err),None,[admin_email])
    #print(err)
    
counter = 1
text_message = []
email_stuff = []
for title in zip(titles,links):
    news_print = '('+str(counter)+') '+title[0]+'\n' 
    #make list of strings ready to be displayed in an email
    email = '<pre>\n'+str(counter)+'. <a href='+str(title[1])+'>'+title[0]+'</a> </pre>'
    #print(news_print)
    text_message.append(news_print)
    email_stuff.append(email)
    counter +=1

#make weather and quote of the day ready for email
email_stuff.insert(0,'<pre>'+weather_info+'\n</pre>')
email_stuff.append('<pre>'+qotd+'</pre>')

#send out the email
list_of_emails = ['blah','blahblah','blah']
email_alert('Daily News', 'placeholder',','.join(email_stuff).replace(',',''), list_of_emails)



#only if you are running this on local computer and not a server
#print('Enter article number to open: \n')
#x = input()

#while x:
#    open_article = links[int(x)-1]
#    webbrowser.open(open_article)
#    print('Now opening... '+open_article)
#    print("\nInput another number or press enter to leave.\n")
#    x=input()
#print('Exiting...')
