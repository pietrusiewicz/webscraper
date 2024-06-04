from flask import Flask, render_template, request
from redis import Redis
import asyncio
import httpx
from bs4 import BeautifulSoup
import scrapersol, scraper
import json
import time

app = Flask(__name__)
r = Redis(host='redis', port=6379)

"""
@app.route('/')
def hello():
    redis.incr('hits')
    counter = str(redis.get('hits'),'utf-8')
    return "This webpage has been viewed "+counter+" time(s)"
"""


@app.route('/home', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        url = request.form['url']
        if url[-1]=='/':
            url = url[:-1]
        ahl = asyncio.run(scraper.main(url))[1:]
        for i in range(len(ahl)):
            if ahl[i]==None:
                ahl[i]=''
        
        print(ahl)
        return render_template('index.html',url=url, addresses=ahl[0],headers=ahl[1],links=ahl[2], footer=ahl[3])
    return render_template('index.html')
#@app.route('/home')
#def home():
    #return render_template('index.html')
    
@app.route('/sol')
def sol():
    strony = asyncio.run(scrapersol.main())
    """crypto com"""
    cc = strony[0]
    #gemini
    cg = strony[1]
    r.rpush("cc",json.dumps({f'{time.strftime("%D-%H:%M")}': cc}))
    r.rpush("cg",json.dumps({f'{time.strftime("%D-%H:%M")}': cg}))

    
    print(type(r.lrange('cc', 0, -1)))
    return render_template('indexsol.html', cryptocom=cc, gemini=cg, cc1=[json.loads(_) for _ in r.lrange('cc', 0, -1)], cg1=[json.loads(_) for _ in r.lrange('cg', 0, -1)])
   
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)