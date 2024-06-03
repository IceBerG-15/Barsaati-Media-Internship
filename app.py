from flask import Flask, render_template, request, redirect, url_for
from twitter_scrapping import main as run_scraper
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv(".env")

app = Flask(__name__)

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI'))
db = client.twitter_trends
collection = db.trends

@app.route('/')
def index():
    # Retrieve data from MongoDB
    trending_data = collection.find(sort=[('date', -1)], projection={'_id': False})
    return render_template('index.html',trend=trending_data[0])

@app.route('/scrape', methods=['POST'])
def scrape():
    if request.method == 'POST':
        run_scraper()
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
