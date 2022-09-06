# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:47:51 2022

@author: josh.smith
"""
from bs4 import BeautifulSoup
import requests
import sys
from automate_email import email_alert
import datetime


x=datetime.datetime.now()
weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
today = weekDays[x.weekday()][:3]
tomorrow = weekDays[x.weekday()+1][:3]
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
def webscrapeWeather(city):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    city = city +' weather'
    city=city.replace(' ','+')
    read = scrapin(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',headers)
    
    try:
        location = read.select('#wob_loc')[0].getText().strip()  
        info = read.select('#wob_dc')[0].getText().strip() 
        weather = read.select('#wob_tm')[0].getText().strip()
        more_Weather = read.select('#wob_dp')[0].getText().strip()
        #print((more_Weather))
        degree_sign = u'\N{DEGREE SIGN}'
        high = more_Weather[more_Weather.find(today)+3:more_Weather.find(tomorrow)][:2]+degree_sign
        low = more_Weather[more_Weather.find(today)+3:more_Weather.find(tomorrow)][5:7]+degree_sign
        #more_Weather[more_Weather.find('°')+1:more_Weather.find('°')]
        #print(location+': ' + info + ' - ' + weather + ' degrees\n')
        
        weather_up = location +' Weather\n'+len(location+' Weather')*'-'+'\nHigh: '+high+'\nLow: '+low+'\n'
        #print(weather_up)
        #weather = location.replace(' ',', ')+': ' + info + ' - ' + weather + ' degrees\n'

    except: 
        print('invalid search')
    return(weather_up)
def webscrapeNews():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        read_news = scrapin('https://www.allsides.com/',headers)
        hyper_set=[]
        title_set = []
        #compile list of titles from the entire website
        url = 'https://www.allsides.com'
        articles = read_news.find_all('a',class_='main-link')
        with open(yesterdays_news_path,'r') as f:
            yesterdays_news=f.read()

        for article in articles:

            if len(title_set) < 5 and article.getText() not in yesterdays_news:    
                if url not in article['href']:
                    #print(len(title_set))
                    title_set.append(article.getText())
                    hyper_set.append(url+article['href'])

        with open(yesterdays_news_path,'w') as f:
            for title in title_set:
                f.write(str(title+'\n'))
    except Exception as err: 
        print(err)
        print('invalid search')
    return(hyper_set,title_set)
weather_info = webscrapeWeather(first_city)
weather_second = webscrapeWeather(second_city)
links,titles = webscrapeNews()
#print(weather_indy)
user_agent={'User-agent': 'Mozilla/5.0'}

quotes_web = scrapin('https://www.brainyquote.com/quote_of_the_day',user_agent)

#print(quotes_web.find('div',class_='grid-item qb clearfix bqQt').getText())
try:
    qotd= quotes_web.find('div',class_='grid-item qb clearfix bqQt').getText()
except Exception as err:
    qotd = '\nNo quote today.'
    email_alert('Error with qotd','File: '+__file__+'\n'+str(err),None,[admin_email])
    #print(err)
counter = 1
text_message = []
email_stuff = []
indy_email_stuff=[]
for title in zip(titles,links):
    news_print = '('+str(counter)+') '+title[0]+'\n' 
    #email = '<pre>\n(<a href='+str(title[1])+'>_'+str(counter)+'_</a>) ' + title[0] +'</pre>'
    email = '<pre>\n'+str(counter)+'. <a href='+str(title[1])+'>'+title[0]+'</a> </pre>'
    #print(news_print)
    #text_message.append(news_print)
    email_stuff.append(email)
    second_city_email_stuff.append(email)
    counter +=1

email_stuff.insert(0,'<pre>'+weather_info+'\n</pre>')
email_stuff.append('<pre>'+qotd+'</pre>')
second_city_email_stuff.insert(0,'<pre>'+weather_second+'\n</pre>')
second_city_email_stuff.append('<pre>'+qotd+'</pre>')
#print(email_stuff)
#print(indy_email_stuff)
email_alert('Daily News', 'placeholder',','.join(email_stuff).replace(',',''), [emails])

email_alert('Daily News', 'placeholder',','.join(second_city_email_stuff).replace(',',''), [more_emails])
#print(titles)
#print(email_stuff)


