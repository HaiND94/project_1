##### Nguyen Dinh Hai ####
######### ver :1.0 #######
##### Data:14/04/2020#####


import requests
import pymongo
from bs4 import BeautifulSoup
import datetime
import time

# Get all of the link article from homepage
def getlink(url):
    page = requests.get(url)
    if page.status_code == 200:     #Connected
        soup = BeautifulSoup(page.content, "html.parser")
        tmp1 = soup.find_all(class_='title-news')
        tmp2 = soup.find_all(class_='title_news')
        getLink = []
        for getlink in tmp1:
            oneTag = getlink.find('a')['href']
            getLink.append(oneTag)
        for getlink in tmp2:
            oneTag = getlink.find('a')['href']
            getLink.append(oneTag)

    else: print("We cant connect to your url, please check it again")
    return (getLink)
#Get content and title for each article
def getcontent(url):
    page = requests.get(url)
    if page.status_code==200:   #Connected
        soup = BeautifulSoup(page.content,"html.parser")
        title_name = soup.title.getText()   #get title
        #print(title_name)
        content_lis = soup.find_all("p", class_="Normal")   #Find all the content tab
        description = soup.find(class_='description')   #get description
        content = str()     #Create content variable
        #content.append = soup.find(class_='description').getText()
        count = 0
        #Join all of the part content from tab to one string
        for li in content_lis:
            if count >=1:
                content = content + li.getText()
            count = 1
        if content == '':
            content_lis = soup.find_all('p')
            count = 0
            for li in content_lis:
                if count >= 1:
                    content = content + li.getText()
                count = 1
        #print(content)
        diction = {'title' : title_name, 'discription' : description.getText(), 'content': content}
    else:
        print('Request Fail, please check your url again!')
    #time.sleep(1)
    return diction
#create a client with name is VnEpress, its have table name is time at present


if __name__=='__main__':
    url = 'https://vnexpress.net/tin-tuc/giao-duc'
    # Connect to MongoDB and create new database with name is the time at present
    name_database = str(datetime.datetime.now())
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    #Create new client
    mydb = myclient["VnEpressDB"]
    # Create new database
    mytable = mydb[name_database]
    allTag = getlink(url)
    count = 0
    diction = getcontent(str(allTag[1]))
    mytable.insert(diction)
    for link in allTag:
        count = count+1
        print(str(count)+link)
        diction = getcontent(str(link))
        mytable.insert(diction)     #write to MongoDB

