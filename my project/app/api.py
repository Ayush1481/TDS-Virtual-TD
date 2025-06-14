from flask import Blueprint, request, jsonify
import base64
from app.ocr_utils import extract_text_from_base64
from app.embedding_utils import get_top_k_chunks
from app.openai_utils import ask_openai

api = Blueprint('api', __name__)

@api.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    image_base64 = data.get("image")

    if image_base64:
        image_text = extract_text_from_base64(image_base64)
        question += f"\nImage text: {image_text}"

    top_chunks = get_top_k_chunks(question)
    answer, links = ask_openai(question, top_chunks)

    return jsonify({
        "answer": answer,
        "links": links
    })
