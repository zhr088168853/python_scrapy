import urllib, urllib.request
from bs4 import BeautifulSoup

myurl = 'http://www.fundiving.com/photo/65393'
htmsrc = urllib.request.urlopen(myurl).read()
htmsrc = htmsrc.decode('UTF-8')
mysoup = BeautifulSoup(htmsrc, 'html.parser')
myimglist = mysoup.find_all("img", width = "700") # 同一页面上所有的照片往往都具有某种共性，除了标
                                                                                     #签都是“img”外，本例页面上所有的摄影作品尺寸都规格化为宽度700像素，故可以根据“width = "700"”这一共性特征来实现批量抓取。
count = 0
for photo in myimglist:
    imgurl = photo.get('src') # 获取照片的源URL
    print(imgurl)
    print(len(imgurl))
    photodata = urllib.request.urlopen(imgurl).read() # 由于网页源码中的照片是以图片链接的形式存储的，故这里在提取了照片的源链接URL
                                                                                       #后，还要用urllib.request库进行二次请求，才能最终获得照片数据。
    myfile = open("D:\picture\imgurl[-8: -4].jpg", "wb") # 把图片的URL如http://cdn.fundiving.com/wp-content/uploads/2018/08/1-18.jpg的倒数第八至倒数第五个字符获取出来
    myfile.write(photodata) # 写入图片数据
    count += 1 # 计数
    myfile.close() # 关闭文件
print("共抓取 " + str(count) + " 张照片") # 输出统计信息
