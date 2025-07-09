import os
from flask import Flask, render_template
from pymongo import MongoClient
from urllib.parse import quote_plus
from flask import redirect, url_for

app = Flask(__name__)
user=os.getenv("Mohit")
password=os.getenv("Mohit@1812")

safe_user = quote_plus(os.environ.get("MONGO_USER", ""))
safe_pass = quote_plus(os.environ.get("MONGO_PASS", ""))


MONGO_URI = f"mongodb+srv://{safe_user}:{safe_pass}@cluster0.jhusqxq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["manga_reader"]
collection = db["manga_pages"]

@app.route("/read/<title>/<chapter>")
def read_chapter(title, chapter):
    try:
        chapter_num = float(chapter)
    except ValueError:
        return "Invalid chapter number", 400

    pages = list(collection.find({"title": title, "chapter": chapter_num}).sort("page_number", 1))
    if not pages:
        return "Chapter not found", 404

    return render_template("read.html", title=title, chapter=chapter, pages=pages)

@app.route("/")
def home():
    return redirect("/read/jujutsu_kaisen/1")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
