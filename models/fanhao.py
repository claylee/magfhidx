import os
import sqlite3
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import json
import datetime
import shelve
import codecs

class Cast():
    castpath = "data/fanhao"
    filename = "casts"

    def __init__(self):
        pass

    def load_casts(self):
        jsondata = shelve.open(self.castpath + "/{}.binjson".format(self.filename))
        return jsondata['data']

    def search(self, words):
        cast_data = self.load_casts()
        casts = []
        for l in cast_data:
            if l.find(words) > -1:
                casts.append(cast_data[l])

        return casts

    def load_casts_page(self, page, pagesize):
        jsondata = shelve.open(self.castpath + "/{}.binjson".format(self.filename))
        cast_list = jsondata['data'].values()
        #print(cast_list)
        #cast_sort = cast_list.sort(key=lambda k: (k.get('hot', 0)))
        cast_sort = sorted(cast_list, key=lambda d: int(d['hot']), reverse = True)
        #print(cast_sort)
        return cast_sort[(page-1)*pagesize:(page-1)*pagesize + pagesize],len(jsondata['data'])

    def load_casts_year(self, value, page, pagesize):
        return self.load_casts_filter('castdate', value, page, pagesize)

    def load_casts_tag(self, value, page, pagesize):
        return self.load_casts_filter('tags', value, page, pagesize)
        pass

    def load_casts_filter(self, key, value, page, pagesize):
        jsondata = self.load_casts()
        #castlist[(page-1)*pagesize:(page-1)*pagesize + pagesize]
        array_s_idx = (page-1)*pagesize
        array_e_idx = (page-1)*pagesize + pagesize
        totals = 0
        tag_list =[]
        for k, v in jsondata.items():
            if value in v[key] >-1:
                totals = totals+1
                if totals <= array_s_idx:
                    continue
                if totals > array_e_idx:
                    continue
                tag_list.append(v)
        return tag_list,totals

    def convert_to_shelve(self):
        file = codecs.open("data/casts.json",'r',encoding='utf-8')
        jsondata = json.loads(file.read()) # list
        castdict = {}
        castdict['data'.encode('utf-8')] = {}
        for jd in jsondata:
            castdict['data'.encode('utf-8')][jd['name'.encode('utf-8')]]=jd
        #castdict['data'.encode('utf-8')] = jsondata

        binjsondata = shelve.open(self.castpath + "/{}.binjson".format(self.filename))
        binjsondata.update(castdict)
        binjsondata.close()

class Fanhao():
    castpath = "data/fanhao"
    filename = "fanhao"

    def __init__(self):
        pass

    def load_fanhao(self):
        jsondata = shelve.open(self.castpath + "/{}.binjson".format(self.filename))
        return jsondata

    def load_fanhao_page(self, page, pagesize):
        jsondata = shelve.open(self.castpath + "/{}.binjson".format(self.filename))
        sortedData = jsondata['data'].values()
        sortedData = sorted(sortedData, key=lambda d: int(d["hot"]), reverse = True)
        return sortedData[(page-1)*pagesize:(page-1)*pagesize + pagesize], len(jsondata['data'])

    def load_fanhao_year(self, value, page, pagesize):
        return self.load_fanhao_idxfilter('issuedate', value, page, pagesize)

    def load_fanhao_tag(self, value, page, pagesize):
        return self.load_fanhao_filter('tags', value, page, pagesize)

    def load_fanhao_publisher(self, value, page, pagesize):
        return self.load_fanhao_filter('publisher', value, page, pagesize)

    def load_fanhao_filter(self, key, value, page, pagesize):
        jsondata = self.load_fanhao()['data']
        #castlist[(page-1)*pagesize:(page-1)*pagesize + pagesize]
        array_s_idx = (page-1)*pagesize
        array_e_idx = (page-1)*pagesize + pagesize
        totals = 0
        tag_list =[]
        for k,v in jsondata.items():
            if value in v[key] >-1:
                totals = totals+1
                if totals <= array_s_idx:
                    continue
                if totals > array_e_idx:
                    continue
                tag_list.append(v)
        return tag_list,totals

    def load_fanhao_idxfilter(self, key, value, page, pagesize):
        jsondict = self.load_fanhao()
        data = jsondict['data']
        idx = jsondict[key]
        #castlist[(page-1)*pagesize:(page-1)*pagesize + pagesize]
        array_s_idx = (page-1)*pagesize
        array_e_idx = (page-1)*pagesize + pagesize
        totals = 0
        tag_list =[]
        sortedData = self.sortedData(data, idx[value])
        for d in sortedData:
            totals = totals+1
            if totals <= array_s_idx:
                continue
            if totals > array_e_idx:
                break
            tag_list.append(d)
        '''
        for k in idx[value]:
            totals = totals+1
            if totals <= array_s_idx:
                continue
            if totals > array_e_idx:
                break
            tag_list.append(data[k])
        '''

        return tag_list,len(idx[value])

    def sortedData(self, data, index = None, sortField = 'hot'):
        dataFilter = data
        if index:
            dataFilter = self.FetchAll(data, index)
        return sorted(dataFilter, key=lambda d: int(d[sortField]), reverse = True)


    def FetchAll(self, data, idx):
        result = []
        for k in idx:
            result.append(data[k])
        return result


    def convert_to_shelve(self):
        binjsondata = shelve.open(self.castpath + "/{}.binjson".format(self.filename))
        fh_list = {}
        idx_cast = {}
        idx_year = {}
        idx_publisher = {}
        if 'data' in binjsondata:
            fh_list = binjsondata['data'.encode('utf-8')]

        for (root, dirs, files) in os.walk("data/fanhao"):
            for filename in files:
                if filename.find('.json') < 0:
                    continue
                filename = os.path.join(root , filename)
                file = codecs.open(filename,'r',encoding='utf-8')
                jsondata = json.loads(file.read())
                for jd in jsondata:
                    fh_list[jd['no']] = jd

                    #add index
                    for c in jd['cast']:
                        if not c in idx_cast:
                            idx_cast[c] = []
                        idx_cast[c].append(jd['no'])

                    if len(jd['issuedate']) > 4:
                        year = jd['issuedate'][0:4]
                        if not year in idx_year:
                            idx_year[year] = []
                        idx_year[year].append(jd['no'])

                    if not jd['publisher'] in idx_publisher:
                        idx_publisher[jd['publisher']] = []
                    idx_publisher[jd['publisher']].append(jd['no'])

        print("len(fh_list)")
        print(len(fh_list))
        binjsondata['data'.encode('utf-8')] = fh_list
        binjsondata['cast'.encode('utf-8')] = idx_cast
        binjsondata['issuedate'.encode('utf-8')] = idx_year
        binjsondata['publisher'.encode('utf-8')] = idx_publisher
        binjsondata.close()
