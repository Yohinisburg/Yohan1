import sqlite3
from pymongo import MongoClient
import pprint
con = sqlite3.connect('gmarketlaptops.db')
cur = con.cursor()
client = MongoClient('localhost', 27017)
db = client.test_db
collection = db.gmarket
import re
import requests
from bs4 import BeautifulSoup



url = "https://browse.gmarket.co.kr/search?keyword=%EB%85%B8%ED%8A%B8%EB%B6%81"
html = requests.get(url, verify=False)
ret1 = html.text
 
htmlsoup1 = BeautifulSoup(ret1, 'html.parser')
 
num_inc = 0
 
num_inc_max = 101
 
elems = htmlsoup1.find_all('div', re.compile("box__component box__component-itemcard"))

cur.execute('''DROP TABLE laptops_all''')
cur.execute('''CREATE TABLE laptops_all
              (Page_num, Item_num, Item_title, Item_price, Item_img)''')

con.commit()

#("page 1 elems Len: "+str(len(elems))+"\n")
for elem in elems:
    title = elem.find('span', attrs={'class': 'text__item'})
    title1 = title['title']
 
    price = elem.find('strong', attrs={'class': 'text text__value'})
 
    urls = elem.find('img')
    link = urls['src']
    num_inc += 1

    cur.execute("insert into laptops_all values (?, ?, ?, ?, ?)",
        ("Page #1 Laptops Info", str(num_inc), title1, "₩" + price.text, link)
    )
    con.commit()

product_num = 100
page_links_num = 1
pnt_class = htmlsoup1.find('li', attrs={'class': 'list-item__tab list-item__tab--active'})
pnt_total = pnt_class.find('span', attrs={'class': 'text__item-count'})
total = str(pnt_total.text).replace(',','')
total1 = int(total)
max_page_links_num = float(total1 / 100)
total_page_num = total1 // 100
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
        
        cur.execute("insert into laptops_all values (?, ?, ?, ?, ?)",
            (page_num, str(product_num), titl1, "₩" + pric.text, lin)
        )

        con.commit()
        

    if page_links_num == total_page_num and break_flag == False and max_page_links_num % 100 != 0:
        total_page_num += 1
        break_flag = True
    else:
        pass

print ("------------All done-------------")
#cur.execute("SELECT * FROM laptops_all")      
#result = cur.fetchall()

