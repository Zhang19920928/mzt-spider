# -*- coding: UTF-8 –*-
import requests,time,parsel,json,lxml,re,random,os,threading
from bs4 import BeautifulSoup

 
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

headers={
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Referer': 'https://www.mmzztt.com/photo/'
}
# 配置代理服务器

proxy = {

'http': 'http://127.0.0.1:7890',

'https': 'http://127.0.0.1:7890'

}

# 创建浏览器对象
def creat_chrome_driver(*, headless=False):
    options = webdriver.ChromeOptions()
    service = Service(executable_path=r'C:\Users\Administrator\.cache\selenium\chromedriver\win32\114.0.5735.90\chromedriver.exe')
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('blink-settings=imagesEnabled=false')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--ignore-certificate-errors")
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(service=service, options=options)
    browser.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument',
        {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'}
    )
    return browser
 
def Download_tu(tu_download,tu_name,folder):#下载一张图片
    tu_pian=requests.get(tu_download,headers=headers)
    #s=r'C:\Users\Administrator\Desktop\test\pic'#设置储存路径
    with open(folder+'\\'+tu_name+'.jpg','wb') as f:
        f.write(tu_pian.content)#写入图片
 
def Download_tuji(url,n):#下载一个图集

    fi=url.rindex('/')
    folder=r'C:\application\img_spider\\' + url[fi+1:]
    if not os.path.exists(folder):
        os.mkdir(folder)
        driver1 = creat_chrome_driver()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver1.maximize_window()
        driver1.get(url)
        #html=driver1.page_source
        #print(html)
        response=requests.get(url,headers=headers)#发送网络请求
        #print(response.text)
        neirong=parsel.Selector(response.text)#解析网页
        print(neirong.xpath('//article[@class="uk-article uk-padding-small uk-background-default m-article"]/progress/@max').get())
        #ye_shu=int(neirong.xpath('//article[@class="uk-article uk-padding-small uk-background-default m-article"]/progress/@max').get())#获取图片最大页数
        for i in range(20):
            time.sleep(1)#设置下载延时
            html=driver1.page_source
            nei_rong=parsel.Selector(html)
            tu_download=nei_rong.xpath('//figure[@class="uk-inline"]/img/@src').get()#获取图片下载地址
            tu_name0=nei_rong.xpath('//figure[@class="uk-inline"]/img/@src').get()#提取图片名字
            ri=tu_name0.rindex('/')
            tu_name=tu_name0[ri+1:]
            #print(f'正在下载第{i+1}张：{tu_name}，此系列共有张{ye_shu}图片,总共下载了{n}张')
            button = driver1.find_element('xpath','//*[@action="next"]')
            button.click()
            #huan_ye=nei_rong.xpath('//figure[@class="uk-inline"]/img/@src').get()#获取换页地址
            print(tu_download,tu_name)
            Download_tu(tu_download,tu_name,folder)      
            #url=huan_ye#换一页
            #response=requests.get(url,headers=headers,proxies=proxy)#换请求新页面
            #nei_rong=parsel.Selector(response.text)
            n+=1#计数
    return n
 
 
def Download_yiye(url):#下载整页图
    #response=requests.get(url,headers=headers)
    #print(response.content)
    #nei_rong=parsel.Selector(response.text)
    #urls=nei_rong.xpath('//*[@class="uk-card-media-top"]/a/@href').getall()
    #urls=re.findall('<img referrerpolicy="no-referrer" src="(.*?)"',response.text,re.S)
    #print(urls)
    for j in range(59):
        time.sleep(1)#设置下载延时
        response=requests.get(url,headers=headers)
        nei_rong=parsel.Selector(response.text)
        urls=nei_rong.xpath('//*[@class="uk-inline u-thumb-v"]/@href').getall()
        print(urls)
        n=1
        for url in urls:
            print(url)#打印要下载的图集地址
            n=Download_tuji(url,n)#下载图片
        url=nei_rong.xpath('//*[@class="uk-pagination uk-flex-center uk-margin-remove uk-visible@s"]/li/a/@href').getall()
        url=url[-1]
        print(url)
        j+=1

    
    n=1#获取当前页面不同类型图集的链接
    for url in urls:
        print(url)#打印要下载的图集地址
        n=Download_tuji(url,n)#下载图片
 
url='https://www.mmzztt.com/photo/'#要爬取的网址
Download_yiye(url)
