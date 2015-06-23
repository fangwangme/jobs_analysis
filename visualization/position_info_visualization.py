#! /usr/bin/env python
#coding=utf-8


import sys
sys.path.append('../')
from common.mongodb import get_mongo_collection
import operator
import numpy as np
import matplotlib.pyplot as plt

reload(sys)
sys.setdefaultencoding('utf-8')

class Visualization():

    def __init__(self, position_type):
        self.position_type = position_type
        self.mongo_db = get_mongo_collection()
        self.position_info = self.get_position_infos()



    def get_position_infos(self):
        '''
        从 mongodb 中获取抓到的页面
        '''
        con = self.mongo_db['lagou_jobs']
        position_info_temp = list(con.find({'position_type': "python" }))

        position_info = {}
        for each_position in position_info_temp:
            position_info[each_position['positionId']] = each_position

        print len(position_info)
        return position_info


    def stat_positions_by_city(self):
        '''
        根据城市统计职位信息
        '''
        stat_info = {}
        for each_position, each_position_info in self.position_info.items():
            if each_position_info['city'] not in stat_info.keys():
                stat_info[each_position_info['city']] = 1
            else:
                stat_info[each_position_info['city']] += 1

        sorted_stat_info = sorted(stat_info.items(), key=operator.itemgetter(1), reverse = True)

        N = len(sorted_stat_info)
        city_name = [x[0].decode('utf-8') for x in sorted_stat_info]
        position_counts = [x[1] for x in sorted_stat_info]

        ind = np.arange(N)  # the x locations for the groups
        width = 1
        plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB']
        plt.rcParams['axes.unicode_minus'] = False      # the width of the bars
        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, position_counts, width, color='#FF9966')#, align='edge')#, yerr=menStd)

        # add some text for labels, title and axes ticks
        ax.set_ylabel('positions')
        ax.set_title('Python positions in china by city')
        ax.set_xticks(ind+0.5)
        '''
        print city_name
        i = 0
        for each_ax in ax.xaxis.get_major_ticks():
            print dir(each_ax.label)
            each_ax.label.set_text(city_name[i])
            i += 1
        '''
        ax.set_xticklabels(city_name,rotation=45)
        ax.legend( (rects1[0],), ('positions',) )

        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x()+rect.get_width()/3., 1.05*height, '%d'%int(height),
                        ha='left', va='bottom')

        autolabel(rects1)
        #plt.show()
        plt.savefig('positions_city.png')

        return



if __name__ == '__main__':
    position_type = 'python'
    v = Visualization(position_type)
    #v.stat_positions_by_city()
