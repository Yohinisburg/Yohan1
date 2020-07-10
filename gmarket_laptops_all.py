from pymongo import MongoClient
import pprint
import re
import requests
from bs4 import BeautifulSoup
import decimal

client = MongoClient('localhost', 27017)
db = client.test_db
collection = db.gmarket

url = "https://browse.gmarket.co.kr/search?keyword=%EB%85%B8%ED%8A%B8%EB%B6%81"
html = requests.get(url, verify=False)
ret1 = html.text
 
htmlsoup1 = BeautifulSoup(ret1, 'html.parser')
 

num_inc = 0
 
num_inc_max = 101
 
elems = htmlsoup1.find_all('div', re.compile("box__component box__component-itemcard"))

#print ("page 1 elems Len: "+str(len(elems))+"\n")
for elem in elems:
    title = elem.find('span', attrs={'class': 'text__item'})
    title1 = title['title']
 
    price = elem.find('strong', attrs={'class': 'text text__value'})
 
    urls = elem.find('img')
    link = urls['src']
    num_inc += 1
    collection.insert_one(
        {
            "Page num" : "Page #1 Laptops Info",
            "Item nr" : str(num_inc),
            "Item title" : title1,
            "Item price" : "₩" + price.text,
            "Item _img" : link
        })
        
        
 
product_num = 0
page_links_num = 1
 
pnt_class = htmlsoup1.find('li', attrs={'class': 'list-item__tab list-item__tab--active'})
pnt_total = pnt_class.find('span', attrs={'class': 'text__item-count'})
total = str(pnt_total.text).replace(',','')
total1 = int(total)
max_page_links_num = float(total1 / 100)
total_page_num = total1 // 100
#total_page_num = 10
#for cur_page in range(0, total_page_num):
break_flag = False
while page_links_num <= total_page_num:
    page_links_num += 1
    page_num = "Page # " + str(page_links_num) + " Laptops Info "
    page_links = "https://browse.gmarket.co.kr/search?keyword=%eb%85%b8%ed%8a%b8%eb%b6%81&k=32&p=" + str(page_links_num)
    html1= requests.get(page_links, verify=False)
    ret = html1.text
    htmlsoup = BeautifulSoup(ret, 'html.parser')
    elems1 = htmlsoup.find_all('div', re.compile("box__component box__component-itemcard"))
    for ele in elems1:
        titl = ele.find('span', attrs={'class': 'text__item'})
        titl1 = titl['title']
        product_num += 1
 
        pric = ele.find('strong', attrs={'class': 'text text__value'})
 
        ur = ele.find('img')
        lin = ur['src']
        collection.insert_one(
        {
            "Page num" : page_num,
            "Item nr" : str(product_num),
            "Item title" : titl1,
            "Item price" : "₩" + pric.text,
            "Item_img" : lin
        })
        

    if page_links_num == total_page_num and break_flag == False and max_page_links_num % 100 != 0:
        total_page_num += 1
        break_flag = True
    else:
        pass
 

