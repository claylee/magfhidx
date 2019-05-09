# -*- coding:utf-8 -*-
#from sqlalchemy import create_engine
import sys
sys.path.append('../')
#from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from config import Config
import re
#from sqlalchemy import create_engine
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.orm import scoped_session, sessionmaker
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
from sqlalchemy import create_engine

#app.config['DATABASE'] = 'sqlite:////tmp/test.db'

#print("flask-sqlalchemy database url :",app.config['DATABASE'])
#print("flask-sqlalchemy database url :",app.config['SQLALCHEMY_DATABASE_URI'])

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
db_session = db.session

#session = Session()

def init_db():
    print("init db ")

    #db2 = SQLAlchemy(app)
    db.init_app(app)
    from models.Models import Test,InfoHash
    app.app_context().push()
    print(db)
    print(db.Model.metadata.tables)
    db.create_all()
    print("init db done")

def init_db_engine():
    print("init db engine")
    from models.Models import Test

    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI,encoding="utf-8",echo=True)
    print(engine)
    Base = declarative_base(bind=engine)
    print(Base.metadata)
    Base.metadata.create_all(engine)
    print("init db done")

def initAuth():
    print("init auth db")
    from models.auth import roles_users,Role,User
    from models import auth

    app = Flask(__name__)

    app.config.from_object(Config)
    #db.init_app(app)

    print(app.app_context())
    app.app_context().push()
    with app.app_context():
        print("-------------------------")
        db.init_app(app)

    auth.build_sample_db(app)


import sqlite3
import os

def immisqlite(filepath = 'data/infohash.db'):
    if not os.path.exists(filepath):
        print("file not exists")

    db.init_app(app)
    from models.Models import Test,SearchHash
    app.app_context().push()


    con = sqlite3.connect(filepath)
    c = con.execute("SELECT * FROM SearchHash")
    sess = db.session
    i =0
    for row in c:
        try:
            t=0
            print(row[4])
            print(row[9])
        except Exception, e:
            print(type(row[4]), len(row[4]))
            print(e)
            continue


        s = SearchHash(
            info_hash = row[1],
            category = row[2],
            data_hash = row[3],
            name = row[4].encode('utf8'),
            extension = row[5],
            classified = row[6],
            source_ip = row[7],
            tagged = row[8],
            length = row[9],
            create_time = row[10],
            last_seen = row[11],
            requests = row[12]
        )
        sess.add(s)
        i+=1
        if i % 2000 == 0:
            print(i)
            sess.commit()
    sess.commit()

    c.close()
    con.close()

def filterUtfmb4(text):
    try:
        text = unicode(text,"utf-8")
    except TypeError as e:
        pass

    try:
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

    return highpoints.sub(u'',text)


def expsqlite(filepath = 'data/infohash.db'):
    if not os.path.exists(filepath):
        print("file not exists")

    import pymysql

    db = pymysql.connect(host='localhost', port=3306,
                     user='root', passwd='123456', db='hashdb', charset='utf8')
    cursor = db.cursor()
    cursor.execute('truncate table searchhash')

    sql = "INSERT INTO searchhash(info_hash, category, data_hash,name,extension,classified,\
        source_ip,tagged,length,create_time,last_seen,requests) \
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    con = sqlite3.connect(filepath)
    c = con.execute("SELECT * FROM searchhash")

    T = []
    i=0
    try:
        for row in c:
            i+=1
            try:
                t=0
                #print(row[1],row[4],row[9])
                s = row[4].encode('utf-8')
            except Exception, e:
                print(type(row[4]), len(row[4]))
                print(e)
                continue
            s = filterUtfmb4(row[4])
            try:
                T.append((row[1],row[2],row[3],s,row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12]))

                if i % 100000 == 0:
                    print(i)
                    cursor.executemany(sql, T)
                    db.commit()
                    T = []
            except Exception as e:
                print(T[0][0],T[1][0])
                print(i, e)
                T = []

    except Exception ,ex:
        print(ex)
        db.rollback()

    cursor.executemany(sql, T)
    db.commit()

    c.close()
    con.close()
    cursor.close()
    db.close()


def PrintSchema(filepath = 'data/infohash.db'):
    if not os.path.exists(filepath):
        print("file not exists")
    con = sqlite3.connect(filepath)
    c = con.execute("SELECT NAME FROM SQLITE_MASTER")
    for SchemaName in c:
        print(SchemaName[0])
    c.close()
    con.close()

def RenameTable(Name, NewName,filepath = 'data/infohash.db'):
    if not os.path.exists(filepath):
        print("file not exists")
    con = sqlite3.connect(filepath)
    con.execute("ALTER TABLE {} RENAME TO {}".format(Name,NewName))
    con.commit()
    print('rename table {} to name {}'.format(Name,NewName))

    con.close()

def TestSelectOpr(TableName = 'SearchHash',filepath = 'data/infohash.db'):
    if not os.path.exists(filepath):
        print("file not exists")
    con = sqlite3.connect(filepath)
    cursor = con.execute("SELECT * FROM {}".format(TableName))
    print('TEST SELECT {}:'.format(TableName))
    for row in cursor:
        rowText = ''
        for t in row:
            rowText += str(t) + " "
        print(rowText)
    con.close()

def TestSql(SqlText, filepath = 'data/infohash.db'):
    if not os.path.exists(filepath):
        print("file not exists")
    con = sqlite3.connect(filepath)
    cursor = con.execute(SqlText)
    print('TEST SQL :')
    for row in cursor:
        rowText = ''
        for t in row:
            rowText += str(t).decode() + " "
        print(rowText)
    con.close()

def inittag():
    print("init_app")
    db.init_app(app)
    print("import cultag")
    from madmin.tag import cultag
    print("SearchHash")
    from models.Models import Test,SearchHash
    print("push")
    app.app_context().push()
    print("cultag")
    cultag()


def createallcuts():
    print("init_app")
    db.init_app(app)
    print("import cultag")
    from madmin.tag import allcuts
    print("SearchHash")
    from models.Models import Test,SearchHash
    print("push")
    app.app_context().push()
    print("cultag")
    allcuts()


def filtercuts():
    print("init_app")
    db.init_app(app)
    print("import cultag")
    from madmin.tag import AllCuts
    print("SearchHash")
    from models.Models import Test,SearchHash
    print("push")
    app.app_context().push()
    print("cultag")
    AllCuts.filtercuts()

def culFilterCuts():
    db.init_app(app)
    from madmin.tag import Tag
    from models.Models import Test,SearchHash
    app.app_context().push()
    t = Tag("")
    t.initHashTag()

from sensitivewords import filter as textfilter
def filterhash():
    db.init_app(app)
    from models.Models import Test,SearchHash
    app.app_context().push()
    print(dir(textfilter))
    textfilter.test_first_character()
