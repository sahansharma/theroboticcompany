import os
from flask import Blueprint, request, jsonify
from openai import OpenAI
from rag.retriever import search as rag_search

ai_bp = Blueprint('ai', __name__)

# Load OpenAI API key from environment variable
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# System prompt for expert robotics/engineering assistant
BASE_SYSTEM_PROMPT = (
    "You are RoboExpert, an advanced AI assistant specialized in robotics and engineering. "
    "Provide clear, accurate, and detailed answers to questions about robotics, automation, control systems, sensors, actuators, AI in robotics, mechanical/electrical/software engineering, and best industry practices. "
    "Assume the user is a robotics engineer, graduate student, or advanced hobbyist. "
    "Cite relevant standards, methodologies, and real-world examples where appropriate. "
    "If a question is outside robotics/engineering, politely redirect to relevant topics.\n"
)

@ai_bp.route('/ask', methods=['POST'])
def ask_ai():
    data = request.get_json()
    user_prompt = data.get('prompt', '').strip()
    print(f"[DEBUG] Received prompt: {user_prompt}")
    if not user_prompt:
        print("[DEBUG] No prompt provided.")
        return jsonify({'error': 'Prompt is required.'}), 400

    # RAG: Retrieve relevant knowledge
    context_snippets = rag_search(user_prompt, k=3)
    print(f"[DEBUG] Retrieved RAG context: {context_snippets}")
    context = "\n---\n".join(context_snippets)
    system_prompt = BASE_SYSTEM_PROMPT + f"\n\nRelevant context:\n{context}\n"
    print(f"[DEBUG] Constructed system prompt: {system_prompt}")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use GPT-4o Mini model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=800,
            temperature=0.3,
            top_p=1.0,
            n=1,
            stop=None
        )
        answer = response.choices[0].message.content.strip()
        print(f"[DEBUG] OpenAI response: {answer}")
        return jsonify({'answer': answer})
    except Exception as e:
        print(f"[DEBUG] Exception occurred: {e}")
        return jsonify({'error': str(e)}), 500
