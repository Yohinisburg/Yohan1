import re
import requests
from bs4 import BeautifulSoup
 
fileName = open("g-market-laptops" , "w")
 
url = "https://browse.gmarket.co.kr/search?keyword=%EB%85%B8%ED%8A%B8%EB%B6%81"
html = requests.get(url, verify=False)
ret1 = html.text
 
htmlsoup1 = BeautifulSoup(ret1, 'html.parser')
 
fileName.write("Page #1 Laptops Info" + "\n")
 
 
num_inc = 0
 
num_inc_max = 101
 
 
elems = htmlsoup1.find_all('div', re.compile("box__component box__component-itemcard"))
for elem in elems:
    title = elem.find('span', attrs={'class': 'text__item'})
    title1 = title['title']
    num_inc += 1
    fileName.write("Item nr: " + str(num_inc) + "\n")
    fileName.write("Item title: " + title1 + "\n")
 
    price = elem.find('strong', attrs={'class': 'text text__value'})
    fileName.write("Item price: " + "₩" + price.text + "\n")
 
    urls = elem.find('img')
    link = urls['src']
    fileName.write("Item _img: " + link + "\n")
print(elem)
 
product_num = 1
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
    page_num = "Page # " + str(page_links_num) + " Laptops Info " + "\n"
    fileName.write(page_num)
    page_links = "https://browse.gmarket.co.kr/search?keyword=%eb%85%b8%ed%8a%b8%eb%b6%81&k=32&p=" + str(page_links_num)
    html1= requests.get(page_links, verify=False)
    ret = html1.text
    htmlsoup = BeautifulSoup(ret, 'html.parser')
    elems1 = htmlsoup.find_all('div', re.compile("box__component box__component-itemcard"))
    for ele in elems1:
        titl = ele.find('span', attrs={'class': 'text__item'})
        titl1 = titl['title']
        product_num += 1
        fileName.write("Item nr: " + str(product_num) + "\n")
        fileName.write("Item title: "+titl1+"\n")
 
        pric = ele.find('strong', attrs={'class': 'text text__value'})
        fileName.write("Item price: " + "₩" + pric.text + "\n")
 
        ur = ele.find('img')
        lin = ur['src']
        fileName.write("Item_img: " + lin + "\n")

    if page_links_num == total_page_num and break_flag == False and max_page_links_num % 100 != 0:
        total_page_num += 1
        break_flag = True
    else:
        pass
 
      
fileName.close()
 

