import os
import sys
import re
import requests
import json
import codecs
from sqlalchemy import or_, and_
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from datetime import datetime
import logging

moviedatapath = "./data/movie"

def movieinfo(moviename):
    pass

def top():
    jsonpath = os.path.join(moviedatapath,'movie_top.json')
    if not os.path.exists(jsonpath):
        file = codecs.open(jsonpath, 'w',encoding='utf-8')
        content = doubanapitop()
        file.write(json.dumps(content,ensure_ascii=False))
        return content

    file = codecs.open(jsonpath, 'r',encoding='utf-8')
    return json.loads(file.read())


def hot():
    jsonpath = os.path.join(moviedatapath,'movie_hot.json')
    if not os.path.exists(jsonpath):
        file = codecs.open(jsonpath, 'w',encoding='utf-8')
        content = doubanapihot()
        file.write(json.dumps(content,ensure_ascii=False))
        return content

    file = codecs.open(jsonpath, 'r',encoding='utf-8')
    return json.loads(file.read())

def doubanmovieinfo(moviename):
    url = "https://api.douban.com/v2/movie/search?q=" + moviename
    r = requests.get(url)
    r.encoding='UTF_8'
    content=r.json()
    if not content:
        return None
    return content

def doubanapitop():
    #file = codecs.open('movie.json', 'w',encoding='utf-8')
    #API
    url = 'http://api.douban.com/v2/movie/top250'
    start=0
    count=50
    r = requests.get(url, params={'start': start, 'count': count})
    r.encoding='UTF_8'
    return r.json()


def doubanapihot():
    #file = codecs.open('movie.json', 'w',encoding='utf-8')
    #API
    url = 'https://api.douban.com/v2/movie/in_theaters'
    r = requests.get(url)
    r.encoding='UTF_8'
    content=r.json()

    #file.write(json.dumps(content,ensure_ascii=False))
    return content
