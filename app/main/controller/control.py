from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import datetime
from datetime import date
import pymongo
from flask import Flask, flash, request, redirect, url_for, render_template, current_app
import pymongo
from app import app

'''
Đầu vào: Dữ liệu các mã cổ phiếu.
Đầu ra: Các file excell được download trực tiếp từ website ứng với từng mã"
'''


@app.route('/', methods=['GET', 'POST'])
def table():
    today = date.today()

    myclient = pymongo.MongoClient("mongodb+srv://ducthangbnn:Oivung1215@cluster0.1rpru.mongodb.net/test",
                                   connect=False)
    mydb = myclient["stocks"]
    mycol = mydb["price_9h_30_ex"]
    b30_stocks = mydb["b30_stock"]

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("chromedriver", chrome_options=options)

    for b30_stock in b30_stocks.find():
        driver.get("https://www.cophieu68.vn/snapshot.php?id={0}".format(b30_stock["code"]))
        time.sleep(3)
        lists = []
        a = driver.find_elements_by_xpath("//*[contains(text(), 'Xem chi tiết giao dịch trong ngày')]")[0]
        a.click()
        time.sleep(1)
        html = driver.page_source
        parse = BeautifulSoup(html, 'html.parser')
        body = parse.find(id="trade_detail")
        rows = body.find_all('tr')[1:]
        lists = []
        for row in rows:
            columns = row.find_all('td')
            list = []
            for column in columns:
                list.append(column.string)
            lists.append(list)
        print(lists)

        min_value_list = []

        for list in lists:
            for i in range(0, len(lists)):
                min_value_list.append(
                    abs(datetime.strptime(lists[i][0] + ":00", '%H:%M:%S') - datetime.strptime('10:00:00', '%H:%M:%S')))

        min_value = min(min_value_list)
        index = min_value_list.index(min_value)
        print(lists[index])

        record = {"code": b30_stock["code"], "date": str(today), "time": lists[index][0] + ":00",
                  "volume": lists[index][3], "price": lists[index][1], 'up_or_down': lists[index][2]}
        mycol.insert_one(record)
        time.sleep(3)
    price_stocks = mycol.find({"date": str(today)})

    return render_template('index.html', cache_timeout=0,
                          price_stocks = price_stocks)







