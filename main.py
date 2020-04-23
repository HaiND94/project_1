##### Nguyen Dinh Hai ####
######### ver :1.1 #######
##### Date:21/04/2020#####

import requests
import threading
from threading import Thread
import pymongo
from bs4 import BeautifulSoup
import datetime
import time

# Get all of the all of the link article from homepage
def get_link_article(url):
    page = requests.get(url)
    if page.status_code == 200:     #Connected
        soup = BeautifulSoup(page.content, "html.parser")
        all_link = []
        for link in soup.find_all('',\
                                  {'class': {'title-news', 'title_new'}}):
            all_link.append(link.find('a')['href'])
        return (all_link)
    else:
        print("We cant connect to your url, please check it again")

# Get link homepage
def get_link_page(url_1,url_2):
    page = requests.get(url_1)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        check = soup.find('a', class_='btn-page next-page')
        if check is None:
            return None
        else:
            url = check.get('href')
            return (url_2+url)
    else:
        print("We cant connect to your url, please check it again")

# Get content and title for each article
def get_content(url):
    page = requests.get(url)
    # Check connected
    if page.status_code == 200:
        soup = BeautifulSoup(page.content,"html.parser")
        title_name = soup.title.getText()
        # Find all the content tab
        content = str()
        count = 0
        # Join all of the part content from tab to one string
        for list_one in soup.find_all("p", class_="Normal"):
            if count >= 1:
                content = content + list_one.getText()
            count = 1
        if content == '':
            count = 0
            for list_two in soup.find_all('p'):
                if count == 1:
                    content = content + list_two.getText()
                count = 1
        diction = {'Title': title_name, 'Content': content}
        mytable.insert(diction)
    else:
        print('Request Fail, please check your url again!')

# Return the value of thread
class Thread_With_Return_Value(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,\
                                        **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return


if __name__ == '__main__':
    time_start = time.time()
    url_1 = 'https://vnexpress.net/tin-tuc/giao-duc'
    url_2 = 'https://vnexpress.net'
    # Connect to MongoDB and create new database
    name_database = "VnExpressDB"
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    #Create new client
    mydb = myclient["VnExpress"]
    # Create new database
    mytable = mydb[name_database]
    # Main program
    while url_1 is not None:
        all_link_article = get_link_article(url_1)
        # Run thread get link page
        thread_get_link_page = Thread_With_Return_Value(\
                            target=get_link_page, args=(url_1,url_2,))
        thread_get_link_page.start()
        thread = [str(i) for i in range(len(all_link_article))]
        # Run thread
        for i in range(len(all_link_article)):
            thread[i] = threading.Thread(target=get_content,\
                                args=(all_link_article[i],))
            thread[i].start()
        # Wait thread end
        for i in range(len(all_link_article)):
            thread[i].join()
        url_1 = thread_get_link_page.join()
        print(url_1)
    print("program execution time:", time.time()-time_start)