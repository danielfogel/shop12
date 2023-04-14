from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import mysql.connector
import requests
import xlsxwriter
from scrapy.selector import Selector



from flaskext.mysql import MySQL
import urllib.request
import time
from datetime import datetime

import requests
app = Flask(__name__)


CORS(app)


@app.route("/<path:path>")
def index(path=None):
     
     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
     response = requests.get(request.url.rstrip("?")[22:], headers=headers)
     
     print(response.content)
     h = []
     p = []
     pt = []
     products = []
     sel = Selector(text=response.content)
     
     heads = sel.xpath("//*[@class='s-item__wrapper clearfix']")

     for head in heads:
        h=head.xpath(".//*[@class='s-item__title']/span/text()").extract_first()
        p=head.xpath(".//*[@class='s-item__price']//text()").extract_first()
        pt=head.xpath(".//*[@class='s-item__image-wrapper image-treatment']/img/@src").extract_first()
        products.append({"head": h, "price": p, "image":pt})
     return jsonify(products)


@app.route('/api/tasks')
def tasks():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM tasks")
    data = cursor.fetchall()
    users = []
    for row in data:
        users.append({"id": row[0], "name": row[1], "content":row[2],"date":row[3],"status":row[4]})
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)