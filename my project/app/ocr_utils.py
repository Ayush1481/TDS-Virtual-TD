import openai
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def ask_openai(question, top_chunks):
    context = "\n\n".join(top_chunks)
    messages = [
        {"role": "system", "content": "You are a helpful assistant for the Tools in Data Science course."},
        {"role": "user", "content": f"Answer the question based on the following notes:\n\n{context}\n\nQuestion: {question}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2
    )

    answer = response["choices"][0]["message"]["content"]
    return answer, []  # Add links later if needed
