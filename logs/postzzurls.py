import os
import codecs
import json

def curls():
    jsonpath = "../data/casts.json"

    file = codecs.open(jsonpath, 'r', encoding='utf-8')
    urlfile = codecs.open("urls.txt", 'w', encoding='utf-8')
    castjson = json.loads(file.read())
    for c in castjson:
        print(c['name'])
        url="http://www.tor01.com/fh/cast/{0}\r\n".format(c['name'].encode("utf-8"))
        print(url.decode("utf8"))
        urlfile.write(url.decode("utf8"))

    file.close()
    urlfile.close()

if __name__ == "__main__":
    curls()
