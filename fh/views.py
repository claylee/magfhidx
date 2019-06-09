import os
import sys
import re
import requests
from math import *
import json
import codecs
from . import fh
from sqlalchemy import or_, and_
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from models.Models import *
from database import db_session
from datetime import datetime
import jieba
from application import app
import logging
from models.movie import *
import random
from scrapyfh import queryhash as qh
from models.movie import *
import sys
from models.fanhao import *
from urllib import *

@fh.route("/",methods = ["Get","POST"])
def index():
    return render_template("/fh/index.html")

@fh.route("/fhs/",methods = ["Get","POST"])
@fh.route("/fhs/<page>",methods = ["Get","POST"])
@fh.route("/fhs_date",methods = ["Get","POST"])
@fh.route("/fhs_date/<year>",methods = ["Get","POST"])
@fh.route("/fhs_tag",methods = ["Get","POST"])
@fh.route("/fhs_tag/<tag>",methods = ["Get","POST"])
def fhs(page = 1 , year = "", tag = "", pagesize = 40, sensfilter = True):
    perfile = 400
    page = int(page)

    fh = Fanhao()
    fh_arr = []
    total = 0
    if year:
        fh_arr, total = fh.load_fanhao_year(year,page,pagesize)
    elif tag:
        fh_arr, total = fh.load_fanhao_tag(tag,page,pagesize)
    else:
        fh_arr, total = fh.load_fanhao_page(page,pagesize)


    return render_template("/fh/fanhao.html", title = "fanhao "
        , pages= ceil(total/float(pagesize)) ,curpage = page, fanhaolist = fh_arr)

    fileidx = int((page-1) * pagesize / perfile  + 1) * 10
    #print("./data/fanhao/fanhao_{}.json".format(fileidx))
    file = codecs.open("./data/fanhao/fanhao_{}.json".format(fileidx), 'r',encoding='utf-8')
    dict = json.loads(file.read())
    start = (page-1)*pagesize - int((page-1) * pagesize / perfile) * perfile
    #print(start)
    l = dict[start: start +pagesize]
    return render_template("/fh/fanhao.html", title = "fanhao "
    , pages= (400 * 40)/pagesize ,curpage = page, fanhaolist = l)

@fh.route("/fhhash/<fhno>/<cast>/",methods = ["Get","POST"])
def fhhash(fhno,cast):
    #castfile = codecs.open("data/cast.json",'r',encoding='utf-8')
    #json_cast = json.loads(castfile.read())
    castLoader = Cast()
    json_cast = castLoader.load_casts()

    fhjson = {}
    linkfhs = []
    results = []
    s_lmt = request.cookies.get('s_lmt')

    fh = Fanhao()
    jsonData = fh.load_fanhao()
    fhjson = jsonData["data"][fhno]

    castsDetail = []
    for c in fhjson['cast']:
        if c in json_cast:
            castsDetail.append(json_cast[c])

    linkfhs,casttotal = fh.load_fanhao_filter("cast",cast,1,12)

    linkPublisherfhs,link_pub_totals = fh.load_fanhao_publisher(fhjson['publisher'],1,12)
    if s_lmt and s_lmt == "0":
        # results = SearchHash.query.filter(
        #     and_(SearchHash.sensi ==0, SearchHash.name.like(fh))
        # ).all()
        idlist = qh.query(fhno)

        results = SearchHash.query.filter(
                SearchHash.id.in_(idlist)
        ).all()

    return render_template("/fh/fh_fhhash.html", fh = fhjson,
        cast = cast, hashlist = results
        , linkfhs = linkfhs, castsDetail=castsDetail,
        link_pub_fhs = linkPublisherfhs, link_pub_totals = link_pub_totals)

@fh.route("/publishers/",methods = ["Get","POST"])
def publishers():
    #fh = Fanhao()
    #fh.convert_to_shelve()

    #cr = Cast()
    #cr.convert_to_shelve()
    fh = Fanhao()
    jsondata = fh.load_fanhao()
    idx_pub = jsondata['publisher']
    publist = []
    for c in idx_pub.keys():
        if not c:
            continue
        publist.append({'pub':c,'count':len(idx_pub[c])})
    #file = codecs.open("data/publisher.json",'r',encoding='utf-8')
    #jsondata = json.loads(file.read())
    return render_template("/fh/fh_serial.html", publist = publist)

@fh.route("/publisher/<pub>",methods = ["Get","POST"])
@fh.route("/publisher/<pub>/<page>",methods = ["Get","POST"])
@fh.route("/publisher_date/<pub>/<year>",methods = ["Get","POST"])
@fh.route("/publisher_date/<pub>/<year>/<page>",methods = ["Get","POST"])
def publisher(pub, year = "", page = 1 , pagesize = 20, sensfilter = True):
    #file = codecs.open("data/publisher.json",'r',encoding='utf-8')
    pub = pub.replace("[_]","/")
    page = int(page)
    year = str(year)
    #jsondata = json.loads(file.read())
    fhlistPub = []
    fhlist = []
    total = 0
    fh = Fanhao()
    #fhlistPub, total = fh.load_fanhao_publisher(pub, page, pagesize)
    idx_publisher = fh.load_fanhao()['publisher']
    fhdata = fh.load_fanhao()['data']

    if year:
        for fh in idx_publisher[pub]:
            if not fh in fhdata:
                continue
            if fhdata[fh]['issuedate'].find(year)>-1:
                fhlist.append(fhdata[fh])
    else:
        for fh in idx_publisher[pub]:
            if not fh in fhdata:
                continue
            fhlist.append(fhdata[fh])

    total = len(fhlist)
    totalpages = ceil(total/float(pagesize))
    fhlist = fhlist[(page-1)*pagesize:(page-1)*pagesize + pagesize]
    return render_template("/fh/fh_serialfh.html", fanhaolist = fhlist, year=year, publisher=pub, pages = totalpages, curpage = page)


@fh.route("/casts/",methods = ["Get","POST"])
@fh.route("/casts/<page>",methods = ["Get","POST"])
@fh.route("/casts_date/<year>",methods = ["Get","POST"])
@fh.route("/casts_date/<year>/<page>",methods = ["Get","POST"])
@fh.route("/casts_tag/<tag>",methods = ["Get","POST"])
@fh.route("/casts_tag/<tag>/<page>",methods = ["Get","POST"])
def casts(page = 1 , year="", tag="", pagesize = 40, sensfilter = True):
    #file = codecs.open("data/casts.json",'r',encoding='utf-8')
    #jsondata = json.loads(file.read())
    cr = Cast()
    page = int(page)

    castlist = []
    total = 0
    if year:
        castlist, total = cr.load_casts_year(year,page,pagesize)
    elif tag:
        castlist, total = cr.load_casts_tag(tag,page,pagesize)
    else:
        castlist, total = cr.load_casts_page(page,pagesize)

    totalpages = ceil(total/float(pagesize))
    return render_template("/fh/fh_castlist.html", casts = castlist, tag = tag , year = year, pages = totalpages, curpage = page)

@fh.route("/cast/<cast>/",methods = ["Get","POST"])
@fh.route("/cast/<cast>/<page>",methods = ["Get","POST"])
@fh.route("/castfh/<cast>/",methods = ["Get","POST"])
@fh.route("/castfh/<cast>/<page>",methods = ["Get","POST"])
def cast(cast, page = 1 , pagesize = 8, sensfilter = True):
    #file = codecs.open("data/casts.json",'r',encoding='utf-8')
    #jsondata = json.loads(file.read())
    cr = Cast()
    fh = Fanhao()

    castjson = cr.load_casts()[cast]

    castfhjson,total = fh.load_fanhao_filter("cast",cast,int(page),pagesize)
    page = int(page)
    print(total, pagesize)
    totalpages = ceil(total/float(pagesize))
    return render_template("/fh/fh_castfh.html", cast = castjson, fhlist = castfhjson, total = total, pages = totalpages, curpage = page)


@fh.route("/mvhot/", methods = ["Get","POST"])
def mvhot():
    jsoncontent = hot()
    return render_template("/fh/mv_hot.html",
        mvs = jsoncontent)


@fh.route("/mvtop/", methods = ["Get","POST"])
def mvtop():
    jsoncontent = top()
    return render_template("/fh/mv_top.html",
        mvs = jsoncontent)


@fh.route("/sitemap",methods = ["Get","POST"])
@fh.route("/sitemap.xml",methods = ["Get","POST"])
def sitemap():
    return app.send_static_file('sitemap.xml')


@fh.route("/sitemap_i1",methods = ["Get","POST"])
@fh.route("/sitemap_i1.xml",methods = ["Get","POST"])
def sitemap_i1():
    return app.send_static_file('sitemap_r1.xml')

@fh.route('/fh/<path:page_name>/')
def redirectNew(page_name=''):
    print '''
    UserAgent: {}
    Method   : {}
    GetArgs  : {}
    PostArgs : {}
    '''.format(
        request.headers.get('User-Agent'),
        request.method,
        request.args,
        request.form,
    )
    return redirect('/{0}'.decode('utf-8').format(page_name), code=301)
