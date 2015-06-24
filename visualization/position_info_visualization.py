#! /usr/bin/env python
#coding=utf-8


import sys
sys.path.append('../')
from common.mongodb import get_mongo_collection
import operator
import numpy as np
import matplotlib.pyplot as plt
import re
plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB']
plt.rcParams['axes.unicode_minus'] = False
colors = ["#FF6666","#99CC66","#99CCFF","#993399","#66CCCC","#6699FF"]

reload(sys)
sys.setdefaultencoding('utf-8')

num_pat = re.compile(r'(\d+)')

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
        position_info_temp = list(con.find({'position_type': self.position_type }))

        position_info = {}
        for each_position in position_info_temp:
            position_info[each_position['positionId']] = each_position

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
        width = 1 # the width of the bars
        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, position_counts, width, color=colors[0])#, align='edge')#, yerr=menStd)

        # add some text for labels, title and axes ticks
        ax.set_ylabel('positions')
        ax.set_title('%s positions in china by city' % self.position_type)
        ax.set_xticks(ind+0.5)
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
        plt.savefig('%s_positions_city.png' % self.position_type)

        return


    def stat_degree(self):

        education_dict = {}

        for position_id, each_position_info in self.position_info.items():
            if each_position_info['education'] not in education_dict.keys():
                education_dict[each_position_info['education']] = 1
            else:
                education_dict[each_position_info['education']] += 1

        #labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        labels = [each_education.decode('utf-8') for each_education in education_dict.keys()]
        sizes = education_dict.values()
        #colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
        sorted_education_info = sorted(education_dict.items(), key=operator.itemgetter(1), reverse = True)

        #labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        labels = [each_education[0].decode('utf-8') for each_education in sorted_education_info]
        sizes = [each_education[1] for each_education in sorted_education_info]

        plt.pie(sizes, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=90)#,colors=colors,)
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        plt.axis('equal')
        #plt.show()
        plt.savefig('%s_education.png' % self.position_type)

        return


    def stat_work_year(self):

        work_year_dict = {}

        for position_id, each_position_info in self.position_info.items():
            if each_position_info['workYear'] not in work_year_dict.keys():
                work_year_dict[each_position_info['workYear']] = 1
            else:
                work_year_dict[each_position_info['workYear']] += 1

        sorted_workyear_info = sorted(work_year_dict.items(), key=operator.itemgetter(1), reverse = True)

        #labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        labels = [each_year[0].decode('utf-8') for each_year in sorted_workyear_info]
        sizes = [each_year[1] for each_year in sorted_workyear_info]

        porcent = [float(each_size) / sum(sizes) * 100 for each_size in sizes]
        labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(labels, porcent)]

        patches, texts = plt.pie(sizes, colors=colors, startangle=90, radius=1)

        sort_legend = True
        if sort_legend:
            patches, labels, dummy =  zip(*sorted(zip(patches, labels, sizes), \
                key=lambda x: x[2], reverse=True))

        labels = [x.decode('utf-8') for x in labels]
        plt.legend(patches, labels, loc='lower left', bbox_to_anchor=(-0.1, 0.7),
                   fontsize=9)

        #plt.show()
        plt.savefig('%s_work_year.png' % self.position_type)
        return



    def avg_salary_by_city(self):
        stat_salary_dict = self.stat_avg_salart_by_key('city')
        sorted_stat_salary = sorted(stat_salary_dict.items(), key=operator.itemgetter(1), reverse = True)

        N = len(sorted_stat_salary)
        field_name = [x[0].decode('utf-8') for x in sorted_stat_salary]
        avg_salary = [(x[1][0] + x[1][1]) /2  for x in sorted_stat_salary]

        ind = np.arange(N)  # the x locations for the groups
        width = 0.8 # the width of the bars
        fig, ax = plt.subplots()
        fig.set_figheight(10)
        rects1 = ax.bar(ind, avg_salary, width, color=colors[0])#, align='edge')#, yerr=menStd)
        # add some text for labels, title and axes ticks
        #ax.axes.get_yaxis().set_visible(False)
        ax.set_ylabel('各城市平均工资分布，单位 K'.decode('utf-8'))
        ax.set_yticks((0,))
        ax.set_xticks(ind+0.5)
        ax.set_xticklabels(field_name,rotation=90)
        #ax.legend( (rects1[0],), ('单位 K',), )


        def autolabel(rects):
            # attach some text labels
            i = 0
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x()+rect.get_width()/3., 1.01*height, '%.2f~%.2f'% (\
                    sorted_stat_salary[i][1][0], sorted_stat_salary[i][1][1]),
                        ha='left', va='bottom', rotation=90)
                i+=1

        autolabel(rects1)

        #plt.show()
        plt.savefig('%s_city_salary.png' % self.position_type)

        return


    def stat_avg_salart_by_key(self, positon_key, city_name = 'NULL'):
        '''
        根据给定关键字统计平均工资，如城市，领域，工作经验
        '''

        if positon_key == 'city':
            city_name = 'NULL'

        salary_dict = {}

        for each_position, each_position_info in self.position_info.items():
            try:

                if city_name != 'NULL':
                    if each_position_info['city'] != city_name:
                        continue

                salary_text = each_position_info['salary']
                salary_text_list = salary_text.split('-')

                if len(salary_text_list) == 1:
                    min_salary = int(num_pat.findall(salary_text_list[0])[0])
                    max_salary = 0
                else:
                    min_salary = int(num_pat.findall(salary_text_list[0])[0])
                    max_salary = int(num_pat.findall(salary_text_list[1])[0])

                if each_position_info[positon_key] not in salary_dict.keys():
                    salary_dict[each_position_info[positon_key]] = {
                        'min_salary':[min_salary],
                        'max_salary':[max_salary]
                        }

                else:
                    salary_dict[each_position_info[positon_key]]['min_salary'].append(min_salary)
                    salary_dict[each_position_info[positon_key]]['max_salary'].append(max_salary)
            except Exception, e:
                print str(e)
                continue


        position_key_list = salary_dict.keys()

        new_salary_dict = {}
        for each_position_key,each_salary_info in salary_dict.items():
            new_position_key = each_position_key.split('·')[-1].strip()
            if new_position_key not in new_salary_dict:
                new_salary_dict[new_position_key] = each_salary_info
            else:
                new_salary_dict[new_position_key]['min_salary'] += each_salary_info['min_salary']
                new_salary_dict[new_position_key]['max_salary'] += each_salary_info['max_salary']


        stat_salary_dict = {}
        for each_position_key, each_salary_info in new_salary_dict.items():
            min_salary_list = each_salary_info['min_salary']
            max_salary_list = each_salary_info['max_salary']
            min_salary_list = filter(lambda a: a != 0, min_salary_list)
            max_salary_list = filter(lambda a: a != 0, max_salary_list)

            avg_min_salary = sum(min_salary_list) / float(len(min_salary_list))
            avg_max_salary = sum(max_salary_list) / float(len(max_salary_list))
            if len(min_salary_list) == 1 or len(max_salary_list) == 1:
                continue

            stat_salary_dict[each_position_key] = [avg_min_salary, avg_max_salary]

        return stat_salary_dict


    def avg_salary_by_field(self):

        stat_salary_dict = self.stat_avg_salart_by_key('industryField', 'NULL')
        sorted_stat_salary = sorted(stat_salary_dict.items(), key=operator.itemgetter(1), reverse = True)


        N = len(sorted_stat_salary)
        field_name = [x[0].decode('utf-8') for x in sorted_stat_salary]
        avg_salary = [(x[1][0] + x[1][1]) /2  for x in sorted_stat_salary]

        ind = np.arange(N)  # the x locations for the groups
        width = 0.8 # the width of the bars
        fig, ax = plt.subplots()
        fig.set_figheight(10)
        rects1 = ax.bar(ind, avg_salary, width, color=colors[0])#, align='edge')#, yerr=menStd)
        # add some text for labels, title and axes ticks
        #ax.axes.get_yaxis().set_visible(False)
        ax.set_ylabel('各领域工资分布，单位 K'.decode('utf-8'))
        ax.set_yticks((0,))
        ax.set_xticks(ind+0.5)
        ax.set_xticklabels(field_name,rotation=90)
        #ax.legend( (rects1[0],), ('单位 K',), )


        def autolabel(rects):
            # attach some text labels
            i = 0
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x()+rect.get_width()/3., 1.01*height, '%.2f~%.2f'% (\
                    sorted_stat_salary[i][1][0], sorted_stat_salary[i][1][1]),
                        ha='left', va='bottom', rotation=90)
                i+=1

        autolabel(rects1)

        #plt.show()
        plt.savefig('%s_field_salary.png' % self.position_type)

        return


if __name__ == '__main__':
    position_type = 'python'
    v = Visualization(position_type)
    #v.stat_positions_by_city()
    #v.stat_work_year()
    #v.stat_degree()
    #v.stat_avg_salart_by_key('industryField')
    #v.avg_salary_by_field()
    v.avg_salary_by_city()
