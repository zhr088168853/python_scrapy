##第一次爬取代码，爬取不到，因为网页源代码无歌曲信息
##import requests
##from bs4 import  BeautifulSoup
##res = requests.get('https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w=%E9%82%93%E7%B4%AB%E6%A3%8B')
##bs = BeautifulSoup(res.text,'html.parser')
##list = bs.find_all(class_='songlist__songname_txt')
##for m in list:
##    print(m['title'])
##print(list)#输出为[],因为网页源代码无歌曲信息，使用BeautifulSoup库无法获得歌曲信息


##第二次爬取改进的代码,可通过json代码爬取第一页的数据
##import requests
##import json
###若爬取的信息不在网页源代码，需点击审查元素-Network-XHR查看，找到Size最大的Name分析
###通过XHR爬取数据一般要使用json,格式为：
####res = requests.get(url)
####json=res.json()
####list=json['']['']...
###url为请求头的url(请求头的url由文件路径和Query String Parameters组成，即以？隔开的两部分)
##res = requests.get('https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=64113167330747138&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&w=%E9%82%93%E7%B4%AB%E6%A3%8B&g_tk_new_20200303=5381&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0')
##json = res.json()
##list = json['data']['song']['list']
##for m in list:
##    # 以name为键，查找歌曲名
##    print('歌曲：'+m['name'])
##   # 查找专辑名
##    print('所属专辑：'+m['album']['name'])
##    # 查找播放链接
##    print('播放链接：https://y.qq.com/n/yqq/song/'+m['mid']+'.html\n\n')
    


####第三次爬取改进的代码
####引入params参数，实现指定歌手、多页数的查询
##import requests
##import json
##url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'#这里的url为上一步url中？之前的部分，因为有指定Query String Parameters参数就不要？后面的部分
##name = input('请输入要查询的歌手姓名：')
##page = int(input('请输入需要查询的歌曲页数：'))
##for x in range(page):
##    params = {   #params为请求头下的Query String Parameters参数
##     'ct':'24',
##     'qqmusic_ver': '1298',
##     'new_json':'1',
##     'remoteplace':'sizer.yqq.song_next',
##     'searchid':'64405487069162918',
##     't':'0',
##     'aggr':'1',
##     'cr':'1',
##     'catZhida':'1',
##     'lossless':'0',
##     'flag_qc':'0',
##     'p':str(x+1),#页数
##     'n':'20',
##     'w':name,#歌手名
##     'g_tk':'5381',
##     'loginUin':'0',
##     'hostUin':'0',
##     'format':'json',
##     'inCharset':'utf8',
##     'outCharset':'utf-8',
##     'notice':'0',
##     'platform':'yqq.json',
##     'needNewCode':'0'    
##    }
##    res = requests.get(url,params=params)
##    json = res.json()
##    list = json['data']['song']['list']
##    for music in list:
##        print(music['name'])
##        print('所属专辑：'+music['album']['name'])
##        print('播放链接：https://y.qq.com/n/yqq/song/'+music['mid']+'.html\n\n')



##第四次爬取改进的代码，在第三次爬取的基础上添加存储功能，保存为Excel
import requests,openpyxl
import json
#创建工作薄
wb=openpyxl.Workbook()  
#获取工作薄的活动表
sheet=wb.active 
#工作表重命名
sheet.title='song' 

sheet['A1'] ='歌曲名'     #加表头，给A1单元格赋值
sheet['B1'] ='所属专辑'   #加表头，给B1单元格赋值
sheet['C1'] ='播放链接'   #加表头，给C1单元格赋值
url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
name = input('请输入要查询的歌手姓名：')
page = int(input('请输入需要查询的歌曲页数：'))
for x in range(page):
    params = {
    'ct':'24',
    'qqmusic_ver': '1298',
    'new_json':'1',
    'remoteplace':'sizer.yqq.song_next',
    'searchid':'64405487069162918',
    't':'0',
    'aggr':'1',
    'cr':'1',
    'catZhida':'1',
    'lossless':'0',
    'flag_qc':'0',
    'p':str(x+1),
    'n':'20',
    'w':name,
    'g_tk':'5381',
    'loginUin':'0',
    'hostUin':'0',
    'format':'json',
    'inCharset':'utf8',
    'outCharset':'utf-8',
    'notice':'0',
    'platform':'yqq.json',
    'needNewCode':'0'    
    }
    res = requests.get(url,params=params)
    json = res.json()
    list = json['data']['song']['list']
    for music in list:
        # 以song_name为键，查找歌曲名，把歌曲名赋值给name
        song_name = music['name']
        # 查找专辑名，把专辑名赋给album
        album = music['album']['name']
        # 查找播放链接，把链接赋值给link
        link = 'https://y.qq.com/n/yqq/song/' + str(music['mid']) + '.html\n\n'
        # 把name、album和link写成列表，用append函数多行写入Excel
        sheet.append([song_name,album,link])
        
#最后保存并命名这个Excel文件     
wb.save(name+'个人单曲排行前'+str(page*20)+'清单.xlsx')    #一页有20首歌曲


input('下载成功，按回车键退出！')
