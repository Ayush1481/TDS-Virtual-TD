import os
import json
import pickle
import requests
import faiss
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from dotenv import load_dotenv
from dotenv import load_dotenv

# --- Setup --- #
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, max_words=120):
    words = text.split()
    chunks = [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
    return chunks

# --- PART 1: Scrape TDS Notes from GitHub (static content) --- #
#def get_tds_notes():
 #  url = "https://raw.githubusercontent.com/s-anand/tds-notes/main/2025-01.json"
  #  response = requests.get(url)
   #    raise Exception(f"Failed to fetch notes JSON: {response.status_code}")
    #notes_json = response.json()
    #texts = [item['text'] for item in notes_json if 'text' in item]
    #return texts
from bs4 import BeautifulSoup
import requests

def get_tds_notes():
    print("Scraping TDS Notes...")
    url = "https://tds.s-anand.net/#/2025-01/"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch notes HTML: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    notes = []

    # Every note is inside a <div class="content"> in a <section>
    for section in soup.find_all('section'):
        content_div = section.find('div', class_='content')
        if content_div:
            text = content_div.get_text(separator="\n", strip=True)
            if text:
                notes.append(text)

    print(f"Fetched {len(notes)} notes from TDS site.")
    return notes



# --- PART 2: Scrape TDS Discourse Forum Posts --- #
import requests

def get_tds_forum_posts():
    topic_list_url = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34.json"

    headers = {
        "Api-Key": os.getenv("DISCOURSE_API_KEY"),
        "Api-Username": os.getenv("DISCOURSE_USERNAME"),
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(topic_list_url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch forum topic list: {response.status_code}")

    topics = response.json()["topic_list"]["topics"]

    all_posts = []
    for topic in topics[:5]:  # optional: limit to avoid rate-limiting
        topic_id = topic["id"]
        topic_url = f"https://discourse.onlinedegree.iitm.ac.in/t/{topic_id}.json"
        topic_response = requests.get(topic_url, headers=headers)
        if topic_response.status_code == 200:
            data = topic_response.json()
            title = data["title"]
            posts = [post["cooked"] for post in data["post_stream"]["posts"]]
            all_posts.append(title + "\n" + "\n".join(posts))
        else:
            print(f"Failed to fetch topic {topic_id}")

    return all_posts




# --- PART 3: Combine, Chunk, Embed, Index --- #
def build_knowledge_index():
    print("Scraping TDS Notes...")
    notes_texts = get_tds_notes()
    print("Scraping TDS Discourse Forum...")
    forum_texts = get_tds_forum_posts()

    print("Chunking content...")
    all_chunks = []
    for text in notes_texts + forum_texts:
        all_chunks.extend(chunk_text(text))

    print(f"Total chunks: {len(all_chunks)}")

    print("Generating embeddings...")
    embeddings = embedding_model.encode(all_chunks, show_progress_bar=True)

    print("Building FAISS index...")
    dimension = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    print("Saving index and chunks...")
    with open("knowledge_chunks.pkl", "wb") as f:
        pickle.dump(all_chunks, f)

    with open("faiss_index.bin", "wb") as f:
        faiss.write_index(index, f)

    print(" All done! Knowledge base ready.")

if __name__ == "__main__":
    build_knowledge_index()
