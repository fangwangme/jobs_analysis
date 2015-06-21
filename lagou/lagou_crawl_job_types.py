#! /usr/bin/env python
#coding=utf-8

'''
@author:fangwang
@date:2015-06-21
@desc: crawl all jobs type at lagou.com
'''

import requests
from lxml import html
import pickle

URL = 'http://www.lagou.com/'


def get_jobs_type():
    '''
    抓取 lagou 首页, 解析所有岗位，保存在 pickle 中
    '''

    req = requests.get(URL)
    content = req.text.encode('utf-8')

    jobs_dict = parse_jobs_type(content)

    with open('jobs_dict.pickle','wb') as f:
        pickle.dump(jobs_dict, f)

    return


def parse_jobs_type(content):
    '''
    解析 lagou 首页，得到所有的职位以及链接
    '''

    content = content.decode('utf-8')
    root = html.fromstring(content)

    jobs_dict = {}

    job_type_list = root.find_class('mainNavs')[0].xpath('div')

    for each_job_ele in job_type_list:
        type_name = each_job_ele.xpath('div[1]/h2/text()')[0].strip().encode('utf-8')

        sub_type_list = each_job_ele.xpath('div[@class="menu_sub dn"]/dl')

        for each_sub_type_ele in sub_type_list:
            sub_type_name = each_sub_type_ele.xpath('dt[1]/a[1]/text()')[0].strip().encode('utf-8')

            jobs_ele_list = each_sub_type_ele.xpath('dd[1]/a')

            for each_job_ele in jobs_ele_list:
                each_job_name = each_job_ele.text.strip().encode('utf-8')
                each_job_url = each_job_ele.xpath('@href')[0].strip().encode('utf-8')

                jobs_dict[each_job_name] = {'name':each_job_name,
                    'url':each_job_url, 'sub_type':sub_type_name, 'type':type_name}

    return jobs_dict


if __name__ == '__main__':
    get_jobs_type()
