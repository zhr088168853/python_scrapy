import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import random


def getHTMLText(url, headers):
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        # print(r.text)
        return r.text
    except:
        return "爬取失败"


def parsehtml(namelist, urllist, html):
    url = 'http://www.tom61.com/'
    soup = BeautifulSoup(html, 'html.parser')
    t = soup.find('dl', attrs={'class': 'txt_box'})
    # print(t)
    if t:
        i = t.find_all('a')
        # print(i)
        for link in i:
            urllist.append(url + link.get('href'))
            namelist.append(link.get('title'))
    else:
        pass



def parsehtml2(html):
    text = []
    soup = BeautifulSoup(html, 'html.parser')
    # t = soup.find('div', class_='t_news_txt')
    t = soup.find('div', attrs={'class': 't_news_txt'})
    if t:
        link = t.find_all('p')
        for i in link:
            text.append(i.text)
        # print(text)
        return "\n".join(text)
    else:
        pass


def sendemail(url, headers):
    
    msg_from = '3365661250@qq.com'  # 发送方邮箱
    passwd = 'zzlusvjyytspdadf'  # 填入发送方邮箱的授权码
    receivers = ['2796493713@qq.com']  # 收件人邮箱

    subject = '今日份的睡前小故事'  # 主题
    html = getHTMLText(url, headers)
    content = parsehtml2(html)  # 正文
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = ','.join(receivers)
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg['To'].split(','), msg.as_string())
        print("发送成功")
    except:
        print("发送失败")
    finally:
        s.quit()


def main():
    count = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        }

    urllist = []
    namelist = []
    for i in range(1, 2):  #网站一共有10页，这里先爬取一页
        if i == 1:
            url = 'http://www.tom61.com/ertongwenxue/shuiqiangushi/index.html'
        else:
            url = 'http://www.tom61.com/ertongwenxue/shuiqiangushi/index_' + str(i) + '.html'
        print("正在爬取第%s页的故事链接：" % (i))
        print(url + '\n')
        html = getHTMLText(url, headers)
        parsehtml(namelist, urllist, html)  #获取故事标题和故事链接
    print("爬取链接完成")

    for i in urllist:
        html = getHTMLText(i,headers)  #根据每一个故事链接获取故事网页
        content = parsehtml2(html) #根据故事网页提取出故事内容
        if content:  #如果内容不为空
            print(content)  #输出每篇故事的内容 
            count+=1
            print('\n')
        else:
            pass
    print('一共有%s个故事\n' %count)

    sendemail(random.choice(urllist), headers)  #随机选取一篇故事进行推送


if __name__ == '__main__':
    main()
