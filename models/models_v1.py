import os
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base,DeclarativeMeta


from flask_admin.contrib.sqla import ModelView
from sqlalchemy.engine.result import RowProxy
import json
import datetime


db = SQLAlchemy()

class SearchHash_v1(db.Model):
    __tablename__ = 'searchhash'

    can_create = False
    can_edit = False
    can_delete = False

    id = Column(Integer, primary_key=True)
    info_hash = Column(String(50))
    category = Column(String(50))
    data_hash = Column(String(50))
    name = Column(String(500))
    extension = Column(String(50))
    classified = Column(Boolean)
    source_ip = Column(String(50))
    tagged = Column(Boolean)
    length = Column(Integer)
    #sensi = Column(Boolean)
    #create_time = Column(DateTime(timezone=True), default=func.now())
    #last_seen = Column(DateTime(timezone=True), default=func.now())
    create_time = Column(String(20))
    last_seen = Column(String(20))
    requests = Column(Integer)
    filescount = Column(Integer)
    files = []

    def rescaleByteSize(self):
        fz = self.length
        sizeUnit = ['B','K','M','G','T']
        ext = "B"
        for unit in sizeUnit:
            ext = unit
            if fz < 1024 or unit == 'T':
                break
            fz = fz / 1024.0
        return "{:.2f}{}".format(fz,ext)

    @staticmethod
    def getall():
        list = SearchHash_v1.query.all()
        return list

    pass



class TORFILES(db.Model):
    """docstring for TORFILES."""
    __tablename__ = 'torfiles'

    tfid = Column(Integer, primary_key=True)
    infohash = Column(String(50))
    filename = Column(String(60))
    filesize = Column(Integer)
    extension = Column(String(20))

    def rescaleByteSize(self):
        fz = self.filesize
        sizeUnit = ['B','K','M','G','T']
        ext = "B"
        for unit in sizeUnit:
            ext = unit
            if fz < 1024 or unit == 'T':
                break
            fz = fz / 1024
        return "{}{}".format(fz,ext)

    @staticmethod
    def BulkCreate(hashcode, files):
        TorList = []
        for z in files:
            TorList.append(TORFILES(
                infohash = hashcode,
                filename = z['path'],
                filesize = z['length'])
            )
        return TorList

    def __init__(self, arg):
        super(TORFILES, self).__init__()
        self.arg = arg




class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):

            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    if isinstance(data, datetime.datetime):
                        data=data.strftime('%Y-%m-%d %H:%M:%S')
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError as ex:
                    fields[field] = None
            return fields

        return json.JSONEncoder.default(self, obj)
