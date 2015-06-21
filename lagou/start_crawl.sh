type=$1
#如果抓取具体的某一个类型 type 为该类型，如果抓取所有类型 type 为 ALL
nohup python -u crawl_jobs_list.py $type > lagou.log &
