import json

from connect import connect
from bs4 import BeautifulSoup

def render_cmt(soup):
    '''
    Detail: Render comment from page of article
    :param soup: the result when request and use beautifulsoup for page
    :return:
    '''
    article_id = get_article_id(soup)
    if (article_id['article_type'] is 'text') or \
            (article_id['article_id'] is None):
        #print('da vao catch')
        return None
    else:
        return (get_comment(get_ulr_cmt(\
                        article_id)))

# Extra comment from api of website to dictionary
def get_comment(url):
    '''
    Task: get comment from api of page article
    :param url is link api get from home page, where is contain comment:
    :return:  None when not cmt and comment when it have comment in page
    '''
    page_cmt = connect(url)
    comment = dict()
    soup = BeautifulSoup(page_cmt.content, "html.parser")
    data = json.loads(soup.getText())
    if data['data']['total'] is 0:
        return None
    else:
        for i in range(len(data['data']['items'])):
            comment[data['data']['items'][i]['full_name']] = \
                data['data']['items'][i]['content']
            #print(comment)
            return comment
        else:
            return None


def get_ulr_cmt(article):
    '''
    Task: extra url api of comment from
    :param article_id: article id of article
    :return: url
    '''
    url_cmt = 'https://usi-saas.vnexpress.net/index/get?offset=0&limit=15&frommobile=0&sort=like&is_onload=1&objectid='\
              +str(article['article_id'])+\
              '&objecttype='+str(article['article_type'])+'&siteid=1000000'
    #print(url_cmt)
    return url_cmt

def get_article_id(soup):
    '''

    :param soup: page of article we need to crawl
    :return: article id
    '''
    article = dict()
    try:
        tmp = soup.find('div', class_='box_comment_vne box_category width_common').\
                        get('data-component-input')
        article_id = json.loads(tmp)['article_id']
        article_type = json.loads(tmp)['article_type']
    except AttributeError:
        try:
            tmp = soup.find('section', class_='section page-detail top-detail').\
                        get('data-component-config')
            article_id = json.loads(tmp)['article_id']
            article_type = json.loads(tmp)['type']
        except AttributeError:
            article_id = None
            article_type = None


    article['article_type'] = article_type
    article['article_id'] = article_id
    #print(tmp)

    #print(article)
    return article

if __name__=='__main__':
    url = 'https://vnexpress.net/ong-hut-choc-thung-khoai-tay-4097836.html'
    page = connect(url)
    soup = BeautifulSoup(page.content, "html.parser")
    article = get_article_id(soup)
    url_cmt = get_ulr_cmt(article)
    #print(get_comment(url_cmt))
    print(render_cmt(soup))