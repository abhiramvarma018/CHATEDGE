from requests_html import HTMLSession

s = HTMLSession()

query = input("enter city name as per google:")
url= f'https://www.google.com/search?q=weather+{query}'

r = s.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'})

temp = r.html.find('span#wob_tm' , first = True).text

unit = r.html.find('div.vk_bk.wob-unit span.wob_t' , first = True).text

desc = r.html.find('div.VQF4g' , first = True).find('span#wob_dc' , first = True).text

print(query, temp, unit, desc)

'''from flask import Flask, render_template, request
from requests_html import HTMLSession

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        if city:
            session = HTMLSession()
            url = f'https://www.google.com/search?q=weather+{city}'
            response = session.get(url)
            if response.ok:
                temp = response.html.find('span#wob_tm', first=True).text
                unit = response.html.find('div.vk_bk.wob-unit span.wob_t', first=True).text
                desc = response.html.find('div.VQF4g span#wob_dc', first=True).text
                return render_template('weatherforecast.html', city=city, temp=temp, unit=unit, desc=desc)
            else:
                error_message = "Error fetching weather data. Please try again later."
                return render_template('weatherforecast.html', error_message=error_message)
    return render_template('weatherforecast.html')


if __name__ == '__main__':
    app.run(debug=True)

'''