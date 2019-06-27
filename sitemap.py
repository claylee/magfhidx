import os
import sys
import re
import requests
import json
import codecs
#from . import magsearcher
from sqlalchemy import or_, and_
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from models.Models import *
from models.fanhao import *
from database import db_session
from datetime import datetime
import jieba
from application import app
import logging
from xml.etree import ElementTree as ET
import os
from flask import url_for
from datetime import datetime,time
import urllib

import io
import re

SITEMAP_DIR = os.path.join(os.path.abspath(os.path.dirname(__name__)), "static/sitemaps")
SITEMAP_URL = "http://wwww.tor01.com/static/sitemaps/"

INDEX_SITEMAP_NAME = "sitemap_index"
POSTS_SITEMAP_NAME = 's_posts'
BASE_SITEMAP_NAME = "s_base"

lastmod_format = "%Y-%m-%dT%H:%M:%S+00:00"

NO_UPDATE = 0
MODIFY = 1
NEW_UPDATE = 2

URL_MAX_COUNT = 50000

DEF_POST_PRIORITY = "0.6"
DEF_POST_CHANGEFREQ = "Weekly"


class SitemapFile:
    """
    """
    def __init__(self, base_name, sitemap_dir=SITEMAP_DIR, index=False):
        """
        :param base_name: sitemap
        :param sitemap_dir: dir for sitemap
        :param index: if it's sitemap index
        self.sitemap_dir = sitemap_dir
        if not os.path.exists(self.sitemap_dir):
            os.makedirs(self.sitemap_dir)

        if index:
            xml_item = self.get_index(base_name)
        else:
            xml_item = self.get_child_sitemap(base_name)

        self.base_name = base_name
        self.xml_name = xml_item.get("xml_name")
        self.xml_path = xml_item.get("xml_path")
        self.xml_tree = xml_item.get("xml_tree")
        self.index = index
        self.update = NO_UPDATE
        self.xml_item = xml_item
        """


    def generate_xml(self,filename, url_list, priority_list, lastmod_list, changefreq_list):
        """Generate a new xml file use url_list"""
        root = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        idx = 0
        for urladdress, prio,mod,freq in zip(url_list,priority_list,lastmod_list,changefreq_list):
            idx +=1
            if idx % 1000 == 0:
                print(idx)
            url = ET.Element('url')
            loc = ET.Element('loc')
            priority = ET.Element('priority')
            lastmod = ET.Element('lastmod')
            changefreq = ET.Element('changefreq')

            loc.text = urladdress
            priority.text = prio
            lastmod.text = mod
            changefreq.text = freq
            url.append(loc)
            url.append(priority)
            url.append(lastmod)
            url.append(changefreq)

            root.append(url)
        header = u'<?xml version="1.0" encoding="UTF-8"?>\n'
        s = ET.tostring(root, encoding='utf-8')#, pretty_print=True)
        with io.open(filename, 'w', encoding='utf-8') as f:
            f.write(unicode(header+s))

    def update_xml(self,filename, url_list):
        """Add new url_list to origin xml file."""
        f = open(filename, 'r')
        lines = [i.strip() for i in f.readlines()]
        f.close()
        old_url_list = []
        for each_line in lines:
            d = re.findall('<loc>(http:\/\/.+)<\/loc>', each_line)
            old_url_list += d
            url_list += old_url_list
            generate_xml(filename, url_list)


    def generatr_xml_index(self, filename, sitemap_list, lastmod_list):
        """Generate sitemap index xml file."""
        root = ET.Element('sitemapindex', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        for each_sitemap, each_lastmod in zip(sitemap_list, lastmod_list):
            sitemap = ET.Element('sitemap')
            loc = ET.Element('loc')
            loc.text = each_sitemap
            lastmod = ET.Element('lastmod')
            lastmod.text = each_lastmod
            sitemap.append(loc)
            sitemap.append(lastmod)
            root.append(sitemap)
        header = u'<?xml version="1.0" encoding="UTF-8"?>\n'
        s = ET.tostring(root, encoding='utf-8', pretty_print=True)
        with io.open(filename, 'w', encoding='utf-8') as f:
            f.write(unicode(header+s))


def get_lastmod_time(filename):
    time_stamp = os.path.getmtime(filename)
    t = time.localtime(time_stamp)
    return time.strftime('%Y-%m-%dT%H:%M:%S+08:00', t)

def maphash():
    fh = Fanhao()
    idx_publisher = fh.load_fanhao()['publisher']

    idx = 0
    for h in idx_publisher.keys():
        c = h.replace("/","[_]")
        urls.append("http://www.tor01.com/publisher/{}".format(urllib.quote(c.encode('utf-8'))))
        idx += 1
        if idx % 1000 == 0:
            print(idx, "http://www.tor01.com/publisher/{}".format(h))
        mods.append(datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S+08:00'))
        #generatr_xml_index('index.xml', urls, mods)
        changefreqs.append("weekly")
        prioritys.append("0.6")

    cast = Cast()
    idx_cast = cast.load_casts()
    for c in idx_cast.keys():
        print(c)
        c = c.replace("/","[_]")
        urls.append("http://www.tor01.com/cast/{}".format(urllib.quote(c.encode('utf-8'))))
        idx += 1
        if idx % 1000 == 0:
            print(idx, "http://www.tor01.com/cast/{}".format(c.encode('utf-8')))
        mods.append(datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S+08:00'))
        #generatr_xml_index('index.xml', urls, mods)
        changefreqs.append("weekly")
        prioritys.append("0.6")

    idx_publisher = fh.load_fanhao()['data']
    for k,h in idx_publisher.items():
        c = k.replace("/","[_]")
        print(h['cast'])
        c_name = ""
        if len(h['cast']) > 0:
            c_name = h['cast'][0]
        urls.append("http://www.tor01.com/fhhash/{}/{}".format(
            urllib.quote(c.encode('utf-8')),urllib.quote(c_name.encode('utf-8'))
        ))
        idx += 1
        if idx % 1000 == 0:
            print(idx, "http://www.tor01.com/fhhash/{}/".format(h), c_name)
        mods.append(datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S+08:00'))
        #generatr_xml_index('index.xml', urls, mods)
        changefreqs.append("weekly")
        prioritys.append("0.6")

    sm = SitemapFile("sitemap_r1")
    sm.generate_xml("static/sitemap_r1.xml",urls,prioritys,mods,changefreqs)

def mapfh():
    pass

if __name__ == '__main__':
    urls = []
    mods = []
    prioritys = []
    changefreqs = []
    print(datetime.now())
    print(type(datetime.now()))
    print(datetime.now())

    db.init_app(app)
    app.app_context().push()

    maphash()
