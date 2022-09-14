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

#today's date
x=datetime.datetime.now()
weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
#get the first three characters from todays weekday
today = weekDays[x.weekday()][:3]
#find tomorrow too so we can parse the correct stuff
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
    #define our user agent for scraping the website
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    city = city +' weather'
    city=city.replace(' ','+')
    #find the weather for the city using google
    read = scrapin(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',headers)
    
    try:
        #get all of the correct data from the wbsite
        location = read.select('#wob_loc')[0].getText().strip()  
        #info = read.select('#wob_dc')[0].getText().strip() 
        #weather = read.select('#wob_tm')[0].getText().strip()
        #this is where the high and lows are located
        more_Weather = read.select('#wob_dp')[0].getText().strip()

        degree_sign = u'\N{DEGREE SIGN}'
        #parse the string to find todays temperatures
        high = more_Weather[more_Weather.find(today)+3:more_Weather.find(tomorrow)][:2]+degree_sign
        low = more_Weather[more_Weather.find(today)+3:more_Weather.find(tomorrow)][5:7]+degree_sign
        #put it all together 
        weather_up = location +' Weather\n'+len(location+' Weather')*'-'+'\nHigh: '+high+'\nLow: '+low+'\n'

    except: 
        print('invalid search')
    return(weather_up)

#here we want to scrape the news for the day, the goal is to find 5 articles
def webscrapeNews():
    try:
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        #website of choise
        read_news = scrapin('https://www.allsides.com/',headers)
        hyper_set=[]
        title_set = []
        #compile list of titles from the entire website
        url = 'https://www.allsides.com'
        articles = read_news.find_all('a',class_='main-link')
        #read what the news was from yesterday
        with open('C:\\Users\josh.smith\Desktop\yesterdays_news.txt','r') as f:
            yesterdays_news=f.read()

        for article in articles:
            #we're shooting for five articles and we want to make sure to not repeat yesterdays news
            if len(title_set) < 5 and article.getText() not in yesterdays_news:    
                #we also dont want to insert the wrong urls (this could be added to the above line instead)
                if url not in article['href']:
                    #print(len(title_set))
                    title_set.append(article.getText())
                    hyper_set.append(url+article['href'])
        #save the news articles we found for today for later use
        with open('C:\\Users\josh.smith\Desktop\yesterdays_news.txt','w') as f:
            for title in title_set:
                f.write(str(title+'\n'))
    #just in case anything goes wrong
    except Exception as err: 
        print(err)
        print('invalid search')
    return(hyper_set,title_set)

#we are finding the quote of the day here
def getQuote():
    #same drill, define user agents and scrape the website
    user_agent={'User-agent': 'Mozilla/5.0'}
    quotes_web = scrapin('https://www.brainyquote.com/quote_of_the_day',user_agent)

    try:
        #find the quote
        qotd= quotes_web.find('div',class_='grid-item qb clearfix bqQt').getText()
    #if anything goes wrong we insert this qotd instead
    except Exception as err:
        qotd = '\nNo quote today.'
        email_alert('Error with qotd','File: '+__file__+'\n'+str(err),None,['josh.smith@kennypipe.com'])
        #print(err)
    return qotd
def newCity(city,emails):
    #use func from above
    weather_info = webscrapeWeather(city)
    links,titles = webscrapeNews()
    qotd = getQuote()
    
    #this counter is to number the articles
    counter = 1
    email_stuff = []
    #run through all the links and titles to compile the email
    for title in zip(titles,links):
         
        email = '<pre>\n'+str(counter)+'. <a href='+str(title[1])+'>'+title[0]+'</a> </pre>'
        email_stuff.append(email)
        dashes=len(str(title[0]))*'-'
        counter +=1
    #further compiling
    email_stuff.insert(0,'<pre>'+weather_info+'\n</pre>')
    email_stuff.append('<pre>\n\n'+qotd.replace('\n\n\n','').replace('.','.\n-')+'</pre>')
    email_alert('Daily News', 'placeholder',','.join(email_stuff).replace(',',''), emails)
    
#send it all out! the above func makes it easy to add people from different places
#newCity('Chicago',email_list1)
#newCity('New York',email_list2)
#newCity('Los Angeles',email_list3)


