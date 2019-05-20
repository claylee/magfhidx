import json
import os
import json
import codecs
import datetime
import shelve
import codecs
import requests
import sys
import urllib

from models import fanhao

def initUrls():
    urls = ""
    cast = fanhao.Cast()
    c_data = cast.load_casts()
    for c,v in c_data.items():
        print(c)
        url = "http://www.tor01.com/cast/{0}/".format(urllib.quote(c.encode("utf-8")))
        #url = urllib.quote(url)
        #print(url)
        urls = "{0}\r\n{1}".decode('utf-8').format(urls,url)


    fh = fanhao.Fanhao()
    f_data = fh.load_fanhao()
    for c in f_data["publisher"]:
        #print(c.decode("utf-8"))
        c.replace("//","[ ]")
        url = "http://www.tor01.com/publisher/{0}".format(urllib.quote(c.encode("utf-8")))
        #url = urllib.quote(url)
        print(url)
        urls = "{0}\r\n{1}".decode('utf-8').format(urls,url)

    for c,v in f_data["data"].items():
        if len(v["cast"]) < 1:
            continue
        url = "http://www.tor01.com/fhhash/{0}/".format(
            urllib.quote(c.encode("utf-8")+"/"+v["cast"][0].encode("utf-8"))
        )
        #url = urllib.quote(url)
        print(url)
        urls = "{0}\r\n{1}".decode('utf-8').format(urls,url)

    file = codecs.open('urls.txt','w','utf-8')
    file.writelines(urls)
    file.close()

def posturls():
    try:
        url = 'http://data.zz.baidu.com/urls?site=www.tor01.com&token=t0vpftn7MLqge4xc'
        headers = {
            'Content-Type': 'text/plain'
        }
        url_list = []
        file = codecs.open('urls.txt','r','utf-8')
        urls = file.readlines()
        file.close()
        #print(urls)
        if len(urls) > 2000:
            i =0
            while i< len(urls):
                url_sp = urls[i+1:i+1+500]
                print(i,len(url_sp))
                r = requests.post(url,headers=headers,data='\n'.join(url_sp))
                data = r.json()
                print(data)
                i += 500
        else:
            r = requests.post(url,headers=headers,data='\n'.join(urls))
            data = r.json()
            print(data)
        #html = requests.post(url, headers=headers, data=urls, timeout=5).text
        #return html
    except Exception as ex:
        raise

if __name__ == "__main__":
    initUrls()
    posturls()
