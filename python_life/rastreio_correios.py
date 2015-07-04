# -*- coding: utf-8 -*-

# rastreio teste: SS123456789BR, SW836849949BR
import urllib.request
import re
import sys

if len(sys.argv) > 2:
    raise SystemError("Please inform code of packet!")

url = ("http://websro.correios.com.br/"
       "sro_bin/txect01$.QueryList?P_ITEMCODE=&P_LINGUA=001&P_TESTE="
       "&P_TIPO=001&P_COD_UNI={}").format(sys.argv[1])

resp = urllib.request.urlopen(url).read()
resp = resp.decode('utf-8', 'ignore')


for line in resp.split('\n'):
    match = re.search(
        r'<tr><td rowspan=.*>(.*)</td><td>.*</td><td>'
        '<FONT COLOR=".*">(.*)</font></td></tr>',
        line)

    if match:
        print("Data: {0}".format(match.group(1)))
        print("Status: {0}".format(match.group(2)))
        print("-"*10)
