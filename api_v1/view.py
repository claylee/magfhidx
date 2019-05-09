import os
import sys
import re
import requests
import json
import codecs
from . import api
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
import redis


@api.route('/v1/posthash/', methods=['GET','POST'])
def posthash():
    print(request.json)
    print("-------------------------------------------")
    if not request.json or not 'info_hash' in request.json:
        abort(400)

    rdb = redis.StrictRedis(host='localhost', db=1)

    if rdb.llen('info_hash') > 10000:
        return 'busy', 201

    jdata = request.json
    jdata = {k.encode('utf8'): v for k, v in jdata.iteritems()}
    info_hash = jdata['info_hash']
    rdb.lpush('info_hash' , jdata)
    return "ok", 201


@api.route('/', methods=['GET','POST'])
def about():
    print("-------------------------------------------")
    return "ok"
