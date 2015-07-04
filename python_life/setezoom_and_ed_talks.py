# -*- coding: utf-8 -*-
# http://elcio.com.br/papo-de-maluco/
import requests
import re


def Ed(text):
    params = dict(
        server='0.0.0.0:8085', charset_post='utf-8',
        charset='utf-8', pure=1, js=0, tst=1, msg=text)

    return re.sub('[^>]*>', '', re.sub(r'\n+$', '', requests.get('http://www.ed.conpet.gov.br/mod_perl/bot_gateway.cgi', params=params).text))


def SeteZoom(text):
    params = dict(server='127.0.0.1:8088', pure=1, js=0, tst=1, msg=text)
    return re.sub(r'\n+$','',
        requests.get('http://bot.insite.com.br/cgi-bin/bot_gateway.cgi',
        params=params).text)

msg = 'Oi!'
while True:
    print('SeteZoom: %s' % msg)
    msg=Ed(msg)
    print('Ed: %s' % msg)
    msg=SeteZoom(msg)
