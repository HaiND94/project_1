# Test value of request method when the network disconnected
import requests
import time

def is_interner_on(url):
    '''

    :param url: link which we need to check
    :return: False when it is loss, and page when ok
    '''
    try:
        page = requests.get(url)
        if page.status_code is 200:
            return page
    except requests.ConnectionError:
        #print('Connection Error')
        return False


def connect(url):
    '''

    :param url: link which we need to work
    :return: page follow request method
    '''
    while is_interner_on(url) is False:
        print('Connecting...')
        time.sleep(1)
        is_interner_on(url)
    return is_interner_on(url)

if __name__ == '__main__':

    url = 'https://vnexpress.net'
    print(connect(url))