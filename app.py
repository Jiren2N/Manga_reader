from flask import Flask, render_template
from pymongo import MongoClient
import os

app = Flask(__name__)
MONGO_URI = os.environ.get("MONGO_URI")  # Will be set in Render
client = MongoClient(MONGO_URI)
db = client['manga_reader']
collection = db['manga_pages']

@app.route('/<title>/chapter/<int:chapter>')
def show_chapter(title, chapter):
    pages = collection.find({"title": title, "chapter": chapter}).sort("page_number")
    return render_template('reader.html', pages=pages)

if __name__ == '__main__':
    app.run(debug=True)
