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
     abort, render_template, flash

sys.path.append("../")
from datetime import datetime
from sqlalchemy.sql import func
from config import Config
from models.models_v1 import db,SearchHash_v1,AlchemyEncoder,TORFILES

import requests

class posthash():

    maxid = 0
    db = None

    def tableslice(self):
        session = db.session
        if self.maxid == 0:
            listDbHash = session.query(func.max(SearchHash_v1.id)).all()
            for l in listDbHash:
                self.maxid = l[0]

        maxid = self.maxid
        splitSize = 1000;
        print('init visited')
        for c in range(splitSize):
            print((maxid / splitSize) * c , (maxid / splitSize) * (c + 1))
            listDbHash = session.query(
                SearchHash_v1).filter(
                    and_(SearchHash_v1.id > (maxid / splitSize) * c,
                        SearchHash_v1.id < (maxid / splitSize) * (c + 1)
                    )
            ).all()
            i=0
            yield listDbHash

    def start(self):

        app = Flask(__name__)

        app.config.from_object(Config)
        print(app.app_context())
        app.app_context().push()
        with app.app_context():
            db.init_app(app)
            url = "http://tor01.com/hashcode/api/v1/posthash/"
            headers = {'Content-Type': 'application/json'}

            session = db.session()
            for result in self.tableslice():
                for a in result:
                    print("read files..")
                    files = session.query(TORFILES).filter(TORFILES.infohash == a.info_hash).all()

                    a.files = files
                    print("dump json..")
                    ajson = json.dumps(a, cls=AlchemyEncoder)
                    print(ajson)
                    #requests.post(url, headers=headers)
                    requests.request("post",url,data=ajson,headers=headers)
            session.close()


if __name__ == "__main__":
    posthash1 = posthash()
    posthash1.start()
