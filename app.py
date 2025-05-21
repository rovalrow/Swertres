from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    today = datetime.now().strftime('%B-%d-%Y').lower()  # e.g., may-21-2025
    url = f"https://www.lottopcso.com/swertres-result-today-{today}/"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        rows = soup.select("table tr")[1:4]
        results = []
        for row in rows:
            cols = row.find_all("td")
            time = cols[0].get_text(strip=True)
            result = cols[1].get_text(strip=True)
            results.append({"time": time, "result": result})

    except Exception as e:
        results = [{"time": "Error", "result": "Could not fetch results"}]

    return render_template("index.html", results=results)
