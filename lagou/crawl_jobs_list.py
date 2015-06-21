#! /usr/bin/env python
#coding=utf-8

'''
@author:fangwang
@date:2015-06-21
@desc 抓取拉勾网上给定职位的列表，保存在 mongodb 中
'''

import sys
sys.path.append('../')
import pymongo
import requests
import pickle
import json
import urllib
from common.chinese_cities import cities
from conf.mongodb_conf import mongodb_conf
import time


REQUEST_URL = 'http://www.lagou.com/jobs/positionAjax.json?'
TIME_SLEEP = 5
CRESCENT_LIST = ['2k以下','2k-5k','5k-10k','10k-15k','15k-25k','25k-50k','50k以上']

def load_positions_dict():
    '''
    load 之前保存的拉勾上的所有岗位信息
    '''

    with open('jobs_dict.pickle', 'rb') as f:
        positions_dict = pickle.load(f)

    return positions_dict


def get_mongo_collection():
    '''
    获取 mongodb collection
    '''

    client = pymongo.MongoClient(mongodb_conf['host'], mongodb_conf['port'])
    db = client[mongodb_conf['db']]
    conllection = db[mongodb_conf['con']]

    return conllection


def crawl_positions_list_by_type(position_type):

    positions_dict = load_positions_dict()
    if position_type not in positions_dict.keys():
        print 'position type %s not in positions_dict, please check again'
        return

    for each_city in cities:
        try:
            if each_city == '北京':
                continue
            elif '(' in each_city:
                each_city = each_city[:each_city.find('(')]

            position_type = position_type.lower()
            crawl_positions_by_city(each_city, position_type)

        except Exception, e:
            print 'crawl city %s error %s' % (each_city, str(e))
            continue



def crawl_positions_by_city(city_name, position_type):
    mongo_con = get_mongo_collection()

    request_url = REQUEST_URL + 'city=' + urllib.quote(city_name)

    next_page = True
    page_no = 1

    while next_page:
        time.sleep(TIME_SLEEP)
        if page_no == 1:
            first_flag = 'true'
        else:
            first_flag = 'false'

        post_dict = {
            'first':first_flag,
            'pn':page_no,
            'kd':position_type
        }

        req = requests.post(request_url, data = post_dict)
        content = req.text.encode('utf-8')
        positions_list, next_page, total_count = parse_positions_list(content, position_type)

        if total_count == 450:
            crawl_positions_by_city_and_crescent(city_name, position_type)
            return

        if positions_list != []:
            mongo_con.insert(positions_list)
        print 'crawl %s posttions for city %s at page %s' % (len(positions_list), \
            city_name, page_no)
        page_no += 1

    return


def crawl_positions_by_city_and_crescent(city_name, position_type):
    mongo_con = get_mongo_collection()

    request_url = REQUEST_URL + 'city=' + urllib.quote(city_name)

    for each_crescent in CRESCENT_LIST:
        each_request_url = request_url + '&yx=' + urllib.quote(each_crescent)

        next_page = True
        page_no = 1

        while next_page:
            time.sleep(TIME_SLEEP)
            if page_no == 1:
                first_flag = 'true'
            else:
                first_flag = 'false'

            post_dict = {
                'first':first_flag,
                'pn':page_no,
                'kd':position_type
            }

            req = requests.post(each_request_url, data = post_dict)
            content = req.text.encode('utf-8')
            positions_list, next_page, total_count = parse_positions_list(content, position_type)
            if positions_list != []:
                mongo_con.insert(positions_list)
            print 'crawl %s posttions for city %s in yx %s at page %s' % (len(positions_list), \
                city_name, each_crescent, page_no)
            page_no += 1

    return



def parse_positions_list(content, position_type):
    '''
    解析抓到的页面，处理成可以直接插入 mongodb 的列表格式
    '''
    positions_list = []
    next_page = False
    total_count = 0

    try:
        content_json = json.loads(content)
        temp_result = content_json['content']['result']
        total_count = content_json['content']['totalCount']
    except Exception, e:
        print 'parse page failed', str(e)
        return positions_list, next_page, total_count

    temp_result = content_json['content']['result']
    if len(temp_result) == 15:
        next_page = True

    for each_position in temp_result:
        each_position['position_type'] = position_type
        each_position['site_source'] = 'lagou'
        positions_list.append(each_position)

    return positions_list, next_page, total_count



if __name__ == '__main__':
    #get_mongo_conllection()
    crawl_positions_list_by_type('C++')
    #print len(cities)
    #crawl_positions_by_city('上海', 'python')
    #crawl_positions_by_city_and_crescent('北京', 'python')
