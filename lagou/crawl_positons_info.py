#! /usr/bin/env python
#coding=utf-8


import sys
sys.path.append('../')
import requests
from conf.mongodb_conf import mongodb_conf,mongodb_conf2
import pymongo
import time


def get_mongo_collection():
    '''
    获取 mongodb collection
    '''

    client = pymongo.MongoClient(mongodb_conf2['host'], mongodb_conf2['port'])
    db = client[mongodb_conf2['db']]
    collection = db[mongodb_conf2['con']]

    return collection


def get_distinct_position_id():
    client = pymongo.MongoClient(mongodb_conf['host'], mongodb_conf['port'])
    db = client[mongodb_conf['db']]
    collection = db[mongodb_conf['con']]

    position_id_list = []
    return list(collection.distinct('positionId'))


def crawl_position_info_by_id(position_id):
    url = 'http://www.lagou.com/jobs/%s.html' % position_id

    req = requests.get(url)
    content = req.text.encode('utf-8')

    con = get_mongo_collection()
    if len(content) > 10000:
        con.insert([{'position_id':position_id, 'content':content}])

    return


def crawl_all():
    position_id_list = get_distinct_position_id()
    for each_position_id in position_id_list:
        time.sleep(5)
        crawl_position_info_by_id(each_position_id)

    return

if __name__ == '__main__':
    #get_distinct_position_id()
    #crawl_position_info_by_id('637513')
    flag = sys.argv[1]
    if flag = 'crawl':
        crawl_all()
    elif flag == 'parse':
        parse_position_info()
    else:
        print 'usage print crawl_positions_info.py flag=crawl/parse'
