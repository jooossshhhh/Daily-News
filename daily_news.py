# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:47:51 2022

@author: josh.smith
"""
from bs4 import BeautifulSoup
import requests
from automate_email import email_alert
import datetime

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
    #search google for the weather
    read_google = scrapin(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',headers)
    weather_link = read_google.find('div',class_='YfftMc')
    #here we find the link for weather.com
    for i in weather_link:
        if i.get('href'):
            actual_weather_link = i.get('href')
    #now we scrape weather.com and find the information we need
    read = scrapin(actual_weather_link,headers)
    try:
        #get all of the correct data from the wbsite
        location = read_google.select('#wob_loc')[0].getText().strip()  
        
        weather_labels= read.find_all('div',class_='WeatherDetailsListItem--label--2ZacS')

        weather = read.find_all('div',class_='WeatherDetailsListItem--wxData--kK35q')

        weather_up=location+'\n'+len(location)*'-'+'\n'
        #i only want specific weather conditions so i leave some out
        for i in zip(weather_labels,weather):
            if 'Wind' not in i[0] and 'Visibility' not in i[0] and 'Dew Point' not in i[0] and 'Pressure' not in i[0]:
                weather_up = weather_up+i[0].getText()+' : '+i[1].getText()+'\n'
        
    except Exception as Err: 
        print('here',Err)
        weather_up='Look up the weather yourself today\n'
    return(weather_up)

#here we want to scrape the news for the day, the goal is to find 5 articles
def webscrapeNews():
    old_news_path = path_to_text_file
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
        with open(old_news_path,'r') as f:
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
        with open(old_news_path,'w') as f:
            for title in title_set:
                f.write((title+'\n'))
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
def getWotd():
    #we are finding the word of the day - just scraping a website for it
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    read = scrapin('https://www.merriam-webster.com/word-of-the-day', headers)
    #wotd=read.find('div',class_='word-and-pronunciation')
    wotdef=read.find('div',class_='wod-definition-container')

    wotdeff=str(wotdef)
    #print(wotdef)
    wotd_def = wotdeff[wotdeff.find('<p>')+3:wotdeff.find('</p>')]
    wotd_linked=wotd_def.replace('<em>','<a href=https://www.merriam-webster.com/word-of-the-day>',1).replace('</em>','</a>',1)+'</pre>'
    #print(wotd_linked)
    return '<pre>\nWord of the day:\n\n'+wotd_linked
links,titles = webscrapeNews()
import holidays
def checkHoliday(today):
    #get all us holidays
    us_holidays=holidays.UnitedStates(years = today.year)
    #save the day and month 
    day = today.day
    month = today.month
    #if the above variables correspond to a specific holiday we tailor the
    #message with unicode emojis
    if month == 12 and day == 25:
        return 'Today is Christmas Day! ' + '\U00002603' + '\U0001F384' + '\U0001F381'
    elif month == 10 and day == 31:
        return 'Today is Halloween! ' +'\U0001F383'
    elif us_holidays[today] == 'Thanksgiving':
        return 'Today is Thanksgiving! '+'\U0001F983 '+'\U000027A1'+' \U0001F357'
    else:
        return us_holidays[today]
def findHoliday():

    now = datetime.date.today()
    #create holiday list so we can find the nearest one
    holiday_list = []
    #set of all us holidays
    us_holidays=holidays.UnitedStates(years = now.year)
    #cycle through all the holidays and save them to the list if the holiday is after today
    for ptr in holidays.UnitedStates(years = now.year).items():
        if ptr[0] > now:
            holiday_list.append(ptr[0])
    #find nearest holiday
    res = min(holiday_list,key=lambda sub:abs(sub-now))
    #subtract 10 days from the resulting holiday
    close_holiday = res - datetime.timedelta(days=10)
    #checks to see if today is a holiday
    if now == res:
        print('today is '+us_holidays[res]+'!')
        holiday_message = '<pre>\n'+'-'*20+'\n\n'+checkHoliday(now)+'<pre>'
    #if the holiday is after today and within 10 days we start the countdown
    elif now > close_holiday and now < res:

        print(res.day-now.day,'days until '+us_holidays[res]+'.')
        holiday_message  = '<pre>\n'+'-'*20+'\n\n'+str(res.day-now.day)+' days until '+str(us_holidays[res]+'.')+'<pre>'
    #otheriwse no holiday message
    else:
        holiday_message=''
    return holiday_message
def newCity(city,emails):
    #use func from above
    weather_info = webscrapeWeather(city)

    qotd = getQuote()
    wotd = getWotd()
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
    email_stuff.append('<pre>\n\n'+qotd.replace('\n\n\n','',1).replace('\n\n\n','\n-')+'</pre>')
    holiday_message = findHoliday()
    email_stuff.append(holiday_message)
    email_stuff.append('\n'+'-'*20+'\n'+wotd)
    email_alert('Daily News', 'placeholder',''.join(email_stuff), emails)
    
#dict of the cities and list of users it's sent to
the_boys = {
            'Chicago':email_list1,
            'New York':email_list2,
            'Los Angeles':email_list3,

            }
#send it all out!
for boy in the_boys:
    newCity(boy,the_boys[boy])



