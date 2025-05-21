from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

def fetch_swertres_results():
    today = datetime.now().strftime("%B-%d-%Y").lower()  # e.g. may-21-2025
    url = f"https://www.lottopcso.com/swertres-result-today-{today}/"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table')  # first table on the page
        rows = table.find_all('tr')[1:]  # skip the header row

        results = []
        for row in rows:
            cols = row.find_all('td')
            time = cols[0].get_text(strip=True)
            result = cols[1].get_text(strip=True)
            results.append({'time': time, 'result': result})

        return results[:3]  # return only the first 3 results
    except Exception as e:
        return [{'time': 'Error', 'result': str(e)}]

@app.route('/')
def home():
    results = fetch_swertres_results()
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
