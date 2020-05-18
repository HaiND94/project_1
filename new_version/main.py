from get_content import get_link_article,\
                        get_content_all,\
                        get_next_page,\
                        link_new

import threading
from threading import Thread
import pymongo
from bs4 import BeautifulSoup
import datetime
import time

def write_data(link_article):
    data = get_content_all(link_article)
    mytable.insert(data, check_keys=False)
    return None
def update_new(link_new):
    '''
    Detail: to update new article
    :param link_new: link of new article
    :return: None
    '''
    for i in range(len(link_new)):
        if link_new[i].find('https://vnexpress.net/') is -1:
            continue
        thread[i] = threading.Thread(target=get_content_all, \
                                     args=(all_link_article[i],))
        thread[i].start()
    # Wait thread end
    for i in range(len(link_new)):
        if link_new[i].find('https://vnexpress.net/') is -1:
            continue
        thread[i].join()
    return None
class Thread_With_Return_Value(Thread):
    '''
    Detail: Return value of thread
    '''
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
    old_href = get_link_article(url_1)
    # Connect to MongoDB and create new database
    name_database = "VnExpressArticle"
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    #Create new client
    mydb = myclient["VnExpress"]
    # Create new database
    mytable = mydb[name_database]
    # Main program
    while url_1 is not None:
        all_link_article = get_link_article(url_1)
        # Run thread get link page
        thread_get_next_page = Thread_With_Return_Value(\
                            target=get_next_page, args=(url_1, url_2,))
        thread_get_next_page.start()
        thread = [str(i) for i in range(len(all_link_article))]
        # Run thread
        for i in range(len(all_link_article)):
            if all_link_article[i].find('https://vnexpress.net/') is -1:
                continue
            thread[i] = threading.Thread(target=write_data,\
                                args=(all_link_article[i],))
            thread[i].start()
        # Wait thread end
        for i in range(len(all_link_article)):
            if all_link_article[i].find('https://vnexpress.net/') is -1:
                continue
            thread[i].join()
        url_1 = thread_get_next_page.join()
        #print(url_1)
    print("program execution time:", time.time()-time_start)
    while True:
        link_new = link_new(old_href)
        old_href = get_link_article()
        update_new(link_new)
