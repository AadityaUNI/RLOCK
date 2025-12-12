from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import logging
import Levenshtein
import requests



app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)



if __name__ == "__main__":
    app.run(debug=True)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def error(message):
    return render_template('error.html', message=message)

@app.route('/')
def index():
    session.clear()
    URL = "http://ipinfo.io/"
    userip = request.remote_addr
    if userip == '127.0.0.1':
        session['country'] = 'in'
    else:
        response = requests.get(f'{URL}{userip}/country/json')
        country = response.json()
        session['country']=(country.get('country')).lower()
        app.logger.debug(country)
    app.logger.debug(session['country'])
    return render_template('index.html', country = session['country'])


    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
def search():
    code = session['country']
    app.logger.debug(code)
    title = request.args.get('q')
    app.logger.debug(title)

    url = f"https://streaming-availability.p.rapidapi.com/shows/{title}"

    querystring = {"series_granularity":"show","output_language":"en", "country":code}

    headers = {
	"x-rapidapi-key": "16fedabe89msh442984c3f406f92p19ea31jsn3308deb49c38",
	"x-rapidapi-host": "streaming-availability.p.rapidapi.com"
            }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    app.logger.debug(data)
    card = {'title': data['title'], 'overview' : data['overview'], 'image': data['imageSet']['verticalPoster']['w360']}
    streaming = []
    try:
        for stream in data['streamingOptions'][code]:
            if stream['type'] != 'subscription':
                streaming.append({'service': stream['service']['name'], 'type': stream['type'], 'price': stream['price']['formatted'], 'link': stream['link']})
            else:
                streaming.append({'service': stream['service']['name'], 'type': stream['type'], 'price': 'Subscription', 'link': stream['link']})
        return render_template('search.html', code = code, streaming = streaming, card = card)
    except:
        return error('No streaming options available at your location ;(. Try out the regional search for finding available locations.')

@app.route('/searchadv', methods = ['GET','POST'])
def searchadv():
    if request.method == 'GET':
        return render_template('searchadv.html')
    elif request.method == 'POST':
        flag = 0
        title = request.form.get('title')
        country = request.form.get('country')
        if not title:
            return error('Entered invalid title')
        if not country:
            code = session['country']
            flag = 1
        if flag == 0:
            url = "https://streaming-availability.p.rapidapi.com/countries"
            querystring = {"output_language":"en"}

            headers = {
	                "x-rapidapi-key": "a59b134055msh9e082972418528fp11b0e2jsn54ad332b218c",
	                "x-rapidapi-host": "streaming-availability.p.rapidapi.com"
                  }

            response = requests.get(url, headers=headers, params=querystring)
            codes = response.json()
            for cntry_key, cntry_value in codes.items():
                if cntry_value['name'] == country.title():
                    code = cntry_value['countryCode']
                    break
            else:
                return error('Where the hell is this country?!')
        url2 = "https://streaming-availability.p.rapidapi.com/shows/search/title"

        querystring2 = {"country": code, "title": title,"series_granularity": "show","output_language": 'en'}
        headers2 = {
	                "x-rapidapi-key": "a59b134055msh9e082972418528fp11b0e2jsn54ad332b218c",
	                "x-rapidapi-host": "streaming-availability.p.rapidapi.com"
                    }

        response2 = requests.get(url2, headers=headers2, params=querystring2)
        list2 = response2.json()
        cards = []
        try:
            title2 = list2[0]['title']
        except:
            return error('Invalid Title')
        img2 = list2[0]['imageSet']['verticalPoster']['w360']
        distance = Levenshtein.distance((title.lower()).strip(), (title2.lower()).strip(), weights = (1,1,2))
        app.logger.debug(distance) 
        if list2[0]['streamingOptions'] == [] or distance > 5:
            return error('Sorry! No Streaming Service available for this title here!')

        try:
            for i in list2[0]['streamingOptions'][code]:
                service = i['service']['name']
                tp = i['type']
                link = i['link']
                if tp == 'rent' or tp == 'buy':
                    price = i['price']['formatted']
                    cards.append({'service': service, 'type': tp, 'price': price, 'link': link})
                else:
                    cards.append({'service': service, 'type': tp, 'link': link})
        except:
            return error('Sorry!  No Streaming Service available for this title here!')
        return render_template('searched.html', cards = cards, title = title2, img2 = img2)
    
@app.route('/searchp', methods=['GET','POST'])
def searchp():
    if request.method == 'GET':
        return render_template('searchp.html')
    else:
        title = request.form.get('title')
        TYPE = request.form.get('TYPE')
        if not TYPE:
            TYPE = 'all'
        url = "https://imdb8.p.rapidapi.com/auto-complete"
        querystring = {"q":title}

        headers = {
	        "x-rapidapi-key": "16fedabe89msh442984c3f406f92p19ea31jsn3308deb49c38",
	        "x-rapidapi-host": "imdb8.p.rapidapi.com"
            }

        response = requests.get(url, headers=headers, params=querystring)
        List = response.json()
        if not List['d']:
            return error('Enter a valid title')
        inner = List['d'][0]
        try:

            card= {'image': inner['i']['imageUrl'], 'id': inner['id'], 'title': inner['l']} 
        except:
            return error('Invalid title')
        
        url = f"https://streaming-availability.p.rapidapi.com/shows/{card['id']}"
        querystring = {"series_granularity":"show","output_language":"en"}
        headers = {
	        "x-rapidapi-key": "16fedabe89msh442984c3f406f92p19ea31jsn3308deb49c38",
	        "x-rapidapi-host": "streaming-availability.p.rapidapi.com"
                }
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        try:
            card['overview'] = data['overview']
        except:
            card['overview'] = ''
        alloptions = {}
        allcodes = []
        try:
            for ccode in data['streamingOptions']: #USE ACCORDIONS HERE FOR EACH COUNTRY
                streams = []
                allcodes.append(ccode)
            
                for streaming in data['streamingOptions'][ccode]:
                    if TYPE == 'all':
                        if streaming['type'] == 'rent' or streaming['type'] == 'buy':
                            streams.append({'type' : streaming['type'], 'service' : streaming['service']['name'], 'price': streaming['price']['formatted'], 'link': streaming['link']})
                        else:
                            streams.append({'type' : streaming['type'], 'service' : streaming['service']['name'], 'price': 'Subscribe', 'link': streaming['link']})
                    elif TYPE == 'buy' or TYPE == 'rent':
                        if streaming['type'] == TYPE:
                            streams.append({'type' : streaming['type'], 'service' : streaming['service']['name'], 'price': streaming['price']['formatted'], 'link': streaming['link']})
                    else:
                        if streaming['type'] == TYPE:
                            streams.append({'type' : streaming['type'], 'service' : streaming['service']['name'], 'price': 'Subscribe', 'link': streaming['link']})
                if streams != []:
                    alloptions[ccode] = streams
                else:
                    allcodes.remove(ccode)
        except:
            return error('Invalid Title')
        app.logger.debug(alloptions)
        app.logger.debug(allcodes)

        return render_template('searchedp.html', title=card['title'], img2=card['image'], overview=card['overview'], alloptions=alloptions, allcodes=allcodes)


@app.route('/feedback', methods=['GET','POST'])
def feedback():
    Type = request.form.get('selectvalue')
    text = request.form.get('text')
    if not Type or not text:
        return error('No text entered')
    file = open('Feedback.txt', 'a')

    file.write(f"Type: {Type} Response: {text}\n")

    file.close()
    return render_template('thanks.html')

    






