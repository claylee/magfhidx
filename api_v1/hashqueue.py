import redis
import sqlalchemy
import requests
import json
import codecs
import sys
import os
import time
from sqlalchemy import or_, and_
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash,jsonify

sys.path.append("../")
from database import db_session
from datetime import datetime
from config import Config
from models.Models import *
from pybloom_live import BloomFilter

class bulkstore():

    bloomfiltercache = None

    bulkTorFiles = []
    bulkSearchHash = []
    def start(self):

        app = Flask(__name__)

        app.config.from_object(Config)
        print(app.app_context())
        app.app_context().push()

        rdb = redis.StrictRedis(host='localhost', db=1)

        while True:
            try:
                time.sleep(1)
                print("redis length:{0} , bulkstore length:{1}".format(
                    rdb.llen("info_hash"),
                    len(self.bulkSearchHash)))
                strjson = rdb.lpop("info_hash")
                info = strjson
                if not info:
                    print("no data")
                    time.sleep(1)
                    continue

                info = eval(info)
                info_hash = info['info_hash']
                files = info['files']
                dhtHashNew = SearchHash(
                    info_hash = info['info_hash'],
                    category = info['category'],
                    data_hash = info['data_hash'],
                    name = info['name'],
                    extension = info['extension'],
                    classified = info['classified'],
                    source_ip = info['source_ip'],
                    tagged = info['tagged'],
                    length = info['length'],
                    create_time = info['create_time'],
                    last_seen = info['last_seen'],
                    filescount = info['filescount'],
                    requests = info['requests']
                )

                self.bulkTorFiles += TORFILES.BulkCreate(info_hash,files)
                self.bulkSearchHash.append(dhtHashNew)

                if len(self.bulkSearchHash) % 500 == 0:
                    self.flush()
            except Exception as ex:
                print(ex)

    def flush(self):
        session = Session()
        infohashlist = [z.info_hash for z in self.bulkSearchHash]
        dhtHashStoreList = session.query(SearchHash).filter(SearchHash.info_hash in infohashlist).all()
        infohashlistStored = [z.info_hash for z in dhtHashStoreList]
        infohashlistNoFile = [z.info_hash for z in dhtHashStoreList if not z.filescount or z.filescount == 0]
        dhtHashNewList = [z for z in self.bulkSearchHash if not z.info_hash in infohashlistStored ]

        for y in dhtHashStoreList:
            for z in self.bulkSearchHash:
                if z.info_hash == y.info_hash :
                    y.last_seen = z.last_seen
                    y.filescount = z.filescount = len(files)
                    break
        self.bulkSearchHash = dhtHashStoreList + dhtHashNewList

        session.bulk_save_objects(self.bulkSearchHash)
        if len(self.bulkTorFiles) > 0:
            self.bulkTorFiles = [z for z in self.bulkTorFiles if z.infohash not in infohashlistStored or z.infohash in infohashlistNoFile]
            session.bulk_save_objects(self.bulkTorFiles)
        session.commit()
        session.close()

        self.bulkTorFiles = []
        self.bulkSearchHash = []

    def exists(self, hashid):
        if binhash in self.bloomvisit:
            return True
        self.bloomvisit.add(hashid)
        return False


    def initbloom(self):
        if not bloomfiltercache:
            self.bloomfiltercache = BloomFilter(capacity=5000000)

        cursor = session.query(SearchHash).filter(SearchHash.info_hash in infohashlist)
        for d in cursor:
            self.bloomvisit.add(d.info_hash.decode('hex'))






if __name__ == "__main__":
    bulkstore1 = bulkstore()
    bulkstore1.start()
