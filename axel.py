

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
#import vlc
import urllib
import urllib.request
import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import wikipedia
import random
from time import strftime
import playsound
from gtts import gTTS
import cosinesimilarity



def axelResponse(audio):
    "speaks audio passed as argument"
    # print(audio)

         #os.system("say " + audio)
    tts = gTTS(text=audio,lang ='en')
    r = random.randint(1,1000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    print(audio)
    playsound.playsound(audio_file)
    os.remove(audio_file)
    return audio


def assistant(command):
    "if statements for executing commands"

    if 'open' in command:
        
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain + ".com"
            webbrowser.open(url)
            return axelResponse('The website you have requested has been opened for you Sir.')
        else:
            pass
    #open subreddit Reddit
    elif 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        return axelResponse('The Reddit content has been opened for you Sir.')

    elif 'shutdown' in command:
        return axelResponse('Bye')
        sys.exit()

    #open website


    #greetings
    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            return axelResponse('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            return axelResponse('Hello Sir. Good afternoon')
        else:
            return axelResponse('Hello Sir. Good evening')

    elif 'help me' in command:
        return ("""
        You can use these commands and I'll help you out:\n
        1. Open reddit subreddit : Opens the subreddit in default browser.\n
        2. Open xyz.com : replace xyz with any website name\n
        3. Send email/email : Follow up questions such as recipient name, content will be asked in order.\n
        5. Current weather in {cityname} : Tells you the current condition and temperture\n
        7. Greetings\n
        8. news for today : reads top news of today\n
        9. time : Current system time\n
        10. top stories from google news (RSS feeds)\n
        11. tell me about xyz : tells you about xyz\n
        
        12. It can hold a regular small talk experience too .
        """)


    #top stories from google news
    elif 'news for today' in command:
        try:
            news_url="https://news.google.com/news/rss"
            Client=urlopen(news_url)
            xml_page=Client.read()
            Client.close()
            soup_page=soup(xml_page,"xml")
            news_list=soup_page.findAll("item")
            
            for news in news_list[:15]:     
                axelResponse(news.title.text.encode('utf-8'))
        except Exception as e:
            print(e)

    #current weather
    elif 'current weather' in command:
        
        # US english

      
        session = requests.Session()
        session.headers['User-Agent'] = USER_AGENT
        session.headers['Accept-Language'] = "en-US,en;q=0.5"
        session.headers['Content-Language'] = "en-US,en;q=0.5"
        reg_ex = re.search('current weather (.*)', command)
        LC = ''
        try:
            loc = "+"
            loc = loc + reg_ex.group(1).split()[1]
            LC = loc

        except:
            print("Scraping Local Weather Data...\n")

        finally:
            page= session.get("https://www.google.com/search?q=weather"+LC)
            s = soup(page.text,'html.parser')
            # store all results on this dictionary
            id1 = s.find(id = 'wob_wc')
            location = id1.find(class_ = "vk_gy vk_h").text
            time =id1.find(class_ = "vk_gy vk_sh" , id = "wob_dts").text
            weather = id1.find(class_ = "vk_gy vk_sh", id = "wob_dc" ).text
            id2 = s.find(id = 'wob_d')
            temperature = id2.find(class_ = 'wob_t', id = 'wob_tm').text
            return "Location : {} \nUpdated Time : {} \nWeather: {} deg Celsius, {}".format(location,time,temperature,weather)


    


    #time
    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        return axelResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))

    #send email
    elif 'email' in command:
        return axelResponse('Who is the recipient?')
        recipient = myCommand()
        if 'david' in recipient:
            axelResponse('What should I say to him?')
            content = myCommand()
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('redforman2000@gmail.com', '1233445')
            mail.sendmail('1234@gmail.com', 'kelso@gmail.com', content)
            mail.close()
            return axelResponse('Email has been sent successfuly. You can check your inbox.')
        else:
            return axelResponse('I don\'t know what you mean!')

    


    #play youtube song
    elif 'play me a song' in command:
        return axelResponse('What song shall I play Sir?')
        mysong = myCommand()
        if mysong:
            flag = 0
            url = "https://www.youtube.com/results?search_query=" + mysong.replace(' ', '+')
            response = urlopen(url)
            html = response.read()
            soup1 = soup(html,"lxml")
            url_list = []
            for vid in soup1.findAll(attrs={'class':'yt-uix-tile-link'}):
                if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                    flag = 1
                    final_url = 'https://www.youtube.com' + vid['href']
                    url_list.append(final_url)

            url = url_list[0]
            ydl_opts = {}

            os.chdir(path)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            #vlc.play(path)

            if flag == 0:
               return axelResponse('I have not found anything in Youtube ')

    
    

    #ask me anything
    elif 'tell me about' or 'i want to know' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                return ny.content[:500]
        except Exception as e:
            print(e)
            axelResponse(e)

        #runningtfidfchatbot
    else :
        print(cosinesimilarity.chats(command))
        return axelResponse(cosinesimilarity.chats(command))

        



