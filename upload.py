import os
from pymongo import MongoClient
from urllib.parse import quote_plus

# Your MongoDB URI (edit this!)
user="Mohit"
password="Mohit@1812"



MONGO_URI = f"mongodb+srv://Mohit:Mohit@1812@cluster0.jhusqxq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["manga_reader"]
collection = db["manga_pages"]

def upload_chapters_from_folder(folder_name):
    title = folder_name.replace(" ", "_").lower()  # e.g., "jujutsu Kaisen" → "jujutsu_kaisen"
    base_path = os.path.join("static/manga", folder_name)

    total = 0

    for chapter_dir in sorted(os.listdir(base_path)):
        chapter_path = os.path.join(base_path, chapter_dir)
        if not os.path.isdir(chapter_path):
            continue

        if not chapter_dir.lower().startswith("ch."):
            continue

        chapter_str = chapter_dir[3:].strip()
        try:
            chapter_num = float(chapter_str.split()[0])
        except ValueError:
            print(f"⚠️ Skipping invalid chapter folder: {chapter_dir}")
            continue

        for i, filename in enumerate(sorted(os.listdir(chapter_path)), 1):
            if not filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                continue

            image_path = f"/static/manga/{title}/{chapter_dir}/{filename}"
            doc = {
                "title": title,
                "chapter": chapter_num,
                "page_number": i,
                "image_path": image_path
            }
            collection.insert_one(doc)
            total += 1

    print(f"✅ Uploaded {total} pages for '{title}'.")

# Example usage
upload_chapters_from_folder("jujutsu Kaisen")