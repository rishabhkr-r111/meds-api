import requests
import json
import lxml
from bs4 import BeautifulSoup
from flask import Flask,jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/")
def main():
    return "<h1>Hiiiii</h1>"

@app.route("/search/<string:query>")
def search(query= 'corocin'):
    URL = f"https://search.apollo247.com/search?query={query}"

    my_headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9,hi;q=0.8",
        "authorization": "Oeu324WMvfKOj5KMJh2Lkf00eW1",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        # "sec-ch-ua": "\"Google Chrome\";v=\"107\", \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"",
        # "sec-ch-ua-mobile": "?0",
        # "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    r = requests.get(URL, headers=my_headers)
    soup = BeautifulSoup(r.content, 'html5lib')
   

    d = soup.find('body').text
    data = json.loads(d)
    return jsonify(data['data'])

@app.route('/product/<string:url_key>')
def product(url_key = 'crocin-pain-relief-tablet'):
    url = f'https://www.apollopharmacy.in/otc/{url_key}'

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    dom = lxml.etree.HTML(str(soup))
    data = {}


    data['name'] = dom.xpath(
        '//*[@id="__next"]/div/div[2]/div/div[3]/div/div[1]/div[1]/div[3]/div[1]/h1')[0].text
    try :
        data['manufacturer'] = dom.xpath(
            '//*[@id="__next"]/div/div[2]/div/div[3]/div/div[1]/div[1]/div[3]/div[1]/div[1]/p')[0].text
    except :
        data['manufacturer'] =''
    try :
        data['composition'] = dom.xpath(
            '//*[@id="__next"]/div/div[2]/div/div[3]/div/div[1]/div[1]/div[3]/div[1]/div[2]/a/p')[0].text
    except :
        data['composition'] = ''

    try :    
        data['img'] = dom.xpath(
            '//*[@id="__next"]/div/div[2]/div/div[3]/div/div[1]/div[1]/div[1]/div/div/div/div[2]/div[1]/div/div/img/@src')[0]
    except :
        data['img'] = ''

    try :    
        data['description'] = dom.xpath(
            '//*[@id="__next"]/div/div[2]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[1]/div/p')[0].text
    except :
        data['description'] = ' '
    try :
        data['about'] = dom.xpath(
            '//*[@id="__next"]/div/div[2]/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/p[1]')[0].text
    except :
        data['about'] = ''
    data['price'] = dom.xpath(
        '//*[@id="__next"]/div/div[2]/div/div[3]/div/div[2]/div/div/div[1]/div[1]/h2')[0].text

    return jsonify(data)

if __name__ == '__main__':
    app.run(threaded=True)
    