import json
from get_comment import get_article_id,\
                        render_cmt
from connect import connect
from bs4 import BeautifulSoup
import time

# Get all of the all of the link article from homepage
def get_link_article(\
            page='https://vnexpress.net/tin-tuc/giao-duc'):
    '''
    :param page: home page which we need to crawl
    :return: all of link in home page
    '''
    page = connect(page)
    soup = BeautifulSoup(page.content, "html.parser")
    all_link = []
    for link in soup.find_all('',\
                            {'class': {'title-news', 'title_new'}}):
        all_link.append(link.find('a')['href'])
    return (all_link)

# Get link homepage
def get_next_page(page='https://vnexpress.net/tin-tuc/giao-duc',\
                  url_2='https://vnexpress.net'):
    '''

    :param page: previous page
    :param url_2: home page
    :return: next page
    '''
    page = connect(page)
    soup = BeautifulSoup(page.content, "html.parser")
    check = soup.find('a', class_='btn-page next-page')
    if check is None:
        return None
    else:
        url = check.get('href')
        print(url_2+url)
        return (url_2+url)

# Get content and title for each article
def get_content_all(page):
    '''

    :param page:
    :return:
    '''
    print(page)
    page = connect(page)
    soup = BeautifulSoup(page.content, "html.parser")
    article = get_article_id(soup)
    title_name = get_title(soup)
    content = get_content_article(soup)
    comment = render_cmt(soup)
    diction = {'Title': title_name, 'Content': content,
               'Comment': comment}
    #print(diction)
    return diction
def get_title(soup):
    '''

    :param soup: the output from beautifulSoup
    :return: tile of page
    '''
    title_name = soup.title.getText()
    return title_name

def get_content_article(soup):
    '''
    Detail: render only the content of the article
    :param soup: the output from beautifulSoup
    :return: content
    '''
    # Find all the content tab
    content = str()
    # Join all of the part content from tab to one string
    for list_one in soup.find_all("p", class_="Normal"):
        content = content + (list_one.getText())
    if content == '':
        for list_two in soup.find_all('p'):
            content = content + (list_two.getText())
    return content

'''def check_new(old_href, url='https://vnexpress.net/tin-tuc/giao-duc'):
    new_href = get_link_article(url)
    print(new_href)
    i =0
    while new_href == old_href is True:
        i +=1
        print(i)
        print()
        time.sleep(1800)
        tmp = get_link_article(url)
        print(tmp)
    return link_new(old_href, new_href)
'''
def link_new(old_href, \
             url='https://vnexpress.net/tin-tuc/giao-duc'):
    '''
    detail: extra link of new article
    :param old_href: all of link old href
    :param url: home page
    :return: link new article
    '''
    link_update = []
    count = 0
    new_href = get_link_article(url)
    while count == 0:
        print("catch!")
        for link in new_href:
            if link not in old_href:
                count += 1
                print(count)
                link_update.append(link)
        time.sleep(18000)
        new_href = get_link_article(url)
    return link_update

# Run in Module
if __name__=='__main__':
    url_1 = 'https://vnexpress.net/tin-tuc/giao-duc'
    url_2 = 'https://vnexpress.net'
    all_link = get_link_article(url_1)
    print(all_link)
    #print(all_link)
    #for link in all_link:
    #    if link.find('https://vnexpress.net/') is -1:
    #        continue
        #print(link)
    #    get_content_all(link)
    #get_next_page()
    print(link_new(all_link))
    #link_new(all_link)
    #get_requier("https://vnexpress.net/kho-dat-diem-10-voi-de-tham-khao-tot-nghiep-thpt-4095938.html")
    #get_comment('https://usi-saas.vnexpress.net/index/get?offset=0&limit=15&frommobile=0&sort=like&is_onload=1&objectid=4095938&objecttype=1&siteid=1000000&categoryid=1004215&sign=f4a972bb1dc9b30291b655be284a74e3&cookie_aid=fwkektgqa2sioff0.1589510681&usertype=4&template_type=1&title=Kh%C3%B3+%C4%91%E1%BA%A1t+%C4%91i%E1%BB%83m+10+v%E1%BB%9Bi+%C4%91%E1%BB%81+tham+kh%E1%BA%A3o+t%E1%BB%91t+nghi%E1%BB%87p+THPT+-+VnExpress&app_mobile_device=0')
