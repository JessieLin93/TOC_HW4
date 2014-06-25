# -*- coding: utf-8 -*-
#Name:林思潔
#Student ID: F74004062
#description:
# parse一個實價登錄列表，判斷裡面所有地址包含有"路"、"大道"、"街"、"巷"的地址
#將他們的所有不同交易年月記錄下來
#印出他們之中含有最多不同交易年月的路名及他們的最大交易總價元和最小交易總價元

import sys
import urllib2
import json
import string
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

#取得傳入網址，將網址內容抓下來，存到contentt中
#把content的內容轉成json格式
URL = sys.argv[1]
content = urllib2.urlopen(URL).read()
json_string = json.loads(content)

lengh_of_json = len(json_string)
year_road_list = []
road_name_list= []

#切路名，還有把交易年月和路名黏在一起
for i in range(lengh_of_json):
	road = string.find(json_string[i][u'土地區段位置或建物區門牌'], u'路')
	avenue = string.find(json_string[i][u'土地區段位置或建物區門牌'], u'大道')
	street = string.find(json_string[i][u'土地區段位置或建物區門牌'], u'街')
	
	#如果路或大道或街出現在xx市xx區之中的話
	if road < 6 and road != -1:
		road = string.find(json_string[i][u'土地區段位置或建物區門牌'][6:], u'路')
		road = road + 6
	if avenue < 6 and avenue != -1:
		avenue = string.find(json_string[i][u'土地區段位置或建物區門牌'][6:], u'大道')
		avenue = avenue + 6
	if street < 6 and street != -1:
		street = string.find(json_string[i][u'土地區段位置或建物區門牌'][6:], u'街')
		street = street + 6
	#判斷路大道街是不是找不到，找不到就找巷
	if road == -1 and avenue == -1 and street == -1:
		lane = string.find(json_string[i][u'土地區段位置或建物區門牌'], u'巷')
		#如果也找不到巷，就不需要這一條路
		if lane != -1:
			road_name = str(json_string[i][u'交易年月']) + json_string[i][u'土地區段位置或建物區門牌'][0:lane+1]
		else:
			road_name = ''
	#判斷哪一個的位置在最後面，就是哪一條路大道街
	elif road == -1 and avenue == -1 and street > 0:
		road_name = str(json_string[i][u'交易年月']) + json_string[i][u'土地區段位置或建物區門牌'][0:street+1]
	elif road == -1 and avenue > 0 and street == -1:
		road_name = str(json_string[i][u'交易年月']) + json_string[i][u'土地區段位置或建物區門牌'][0:avenue+2]
	elif road > 0 and avenue == -1 and street == -1:
		road_name = str(json_string[i][u'交易年月']) + json_string[i][u'土地區段位置或建物區門牌'][0:road+1]
	elif road > avenue and road > street:
		road_name = str(json_string[i][u'交易年月']) + json_string[i][u'土地區段位置或建物區門牌'][0:road+1]
	elif avenue > road and avenue > street:
		road_name = str(json_string[i][u'交易年月']) + json_string[i][u'土地區段位置或建物區門牌'][0:avenue+2]
	elif street > road and street > avenut:
		road_name = str(json_string[i][u'交易年月']) + json_string[i][u'土地區段位置或建物區門牌'][0:street+1]
	
	#把不重複的道路名稱＋交易年月記錄下來
	num = year_road_list.count(road_name)
	if road_name != '':
		if num == 0:
			year_road_list.append(road_name)
	#把不重複的道路名稱記錄下來
	num = road_name_list.count(road_name[5:])
	if road_name != '':
		if num == 0:
			road_name_list.append(road_name[5:])

#判斷所有不同道路的交易年月有幾個			
max_num = 0
num_of_road_name = 0
#記錄道路和他所有的交易年月個數
map_of_road_name_and_num = {}
for x in range(len(road_name_list)):
	num_list = 0
	for n in range(len(year_road_list)):
		if road_name_list[x] in year_road_list[n]:
			num_list = num_list + 1
	#把道路和他所有的交易年月個數記錄下來
	map_of_road_name_and_num[road_name_list[x]] = num_list 
	#判斷交易年月個數有沒有大於目前最大值
	if num_list > max_num:
		max_num = num_list
		if num_of_road_name == 0:
			num_of_road_name = 1
	elif num_list == max_num:
		num_of_road_name = num_of_road_name + 1
		
#判斷最大和最小總價元
for y in range(len(road_name_list)):
	road = ''
	max_money = 0
	min_money = 10000000000000
	#如果他所存的交易年月個數和最大交易年月個數一樣的話
	#就把他印出來
	if map_of_road_name_and_num[road_name_list[y]] == max_num:
		road = road_name_list[y]
		for z in range(lengh_of_json):
			if road_name_list[y] in json_string[z][u'土地區段位置或建物區門牌']:
				money = json_string[z][u'總價元']
				
				if money > max_money:
					max_money = money
				if min_money > money:
					min_money = money	
		print road + ', 最高成交價' + str(max_money) + ', 最低成交價' + str(min_money)
	
