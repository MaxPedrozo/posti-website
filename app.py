from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[-\s]+', '-', text).strip('-')

@app.route('/publish', methods=['POST'])
def publish():
    data = request.json
    title = data['title']
    category = data['category']
    excerpt = data['excerpt']
    content_html = data['content']
    
    # Fix: Ensure forward slashes for cross-platform image paths
    image_url = data['image'].replace('\\', '/')
    
    slug = slugify(title)
    filename = f"{slug}.html"
    
    # Fix: Define date_str and post_id before creating the new_post object
    date_str = datetime.now().strftime("%Y-%m-%d")
    post_id = datetime.now().strftime("%Y%m%d%H%M%S")

    # Dynamic HTML Template for the Post
    post_template = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"><title>{title} | POSTI Journal</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            .glass {{ background: rgba(255,255,255,0.8); backdrop-filter: blur(10px); }}
            .article-content p {{ margin-bottom: 1.5rem; line-height: 1.8; color: #475569; }}
            .article-content ul {{ list-style-type: disc; margin-left: 2rem; margin-bottom: 1.5rem; }}
            .article-content h2 {{ font-size: 1.5rem; font-weight: bold; margin-top: 2rem; margin-bottom: 1rem; }}
        </style>
    </head>
    <body class="bg-white">
        <nav class="fixed w-full z-50 glass border-b border-slate-300">
            <div class="max-w-6xl mx-auto px-6 h-24 flex items-center justify-between">
                <a href="../index.html" class="flex items-center gap-2 group">
                    <img src="../assets/logo.png" alt="POSTI Logo" class="h-12 md:h-20 w-auto group-hover:opacity-80 transition-opacity">
                    <span class="text-4xl font-bold tracking-tighter text-slate-900 group-hover:text-blue-600 transition-colors">POSTI</span>
                </a>
                <a href="../blog.html" class="text-sm font-bold text-blue-600 hover:text-blue-800 flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
                    Back to Journal
                </a>
            </div>
        </nav>
        
        <main class="max-w-3xl mx-auto pt-40 pb-20 px-6">
            <span class="text-blue-600 font-bold text-xs uppercase tracking-widest">{category}</span>
            <h1 class="text-4xl md:text-5xl font-bold mt-4 mb-10 tracking-tight text-slate-900">{title}</h1>
            <img src="../{image_url}" class="w-full rounded-[2.5rem] shadow-2xl mb-12 border border-slate-100">
            <div class="article-content text-lg">
                {content_html}
            </div>
        </main>
    </body>
    </html>"""

    os.makedirs('posts', exist_ok=True)
    with open(f"posts/{filename}", "w", encoding="utf-8") as f:
        f.write(post_template)

    db_path = 'data.json'
    posts = []
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding="utf-8") as f:
            posts = json.load(f)

    new_post = {
        "id": post_id,
        "title": title,
        "category": category,
        "date": date_str,
        "excerpt": excerpt,
        "image": image_url,
        "url": f"posts/{filename}"
    }
    posts.insert(0, new_post)

    with open(db_path, 'w', encoding="utf-8") as f:
        json.dump(posts, f, indent=4)

    return jsonify({"message": "Success", "url": f"posts/{filename}"})

if __name__ == '__main__':
    app.run(debug=True)