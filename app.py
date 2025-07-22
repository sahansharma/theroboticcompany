from flask import Flask, render_template, request, jsonify
import csv
import os

app = Flask(__name__)

# ---- Load Parts Function ----
def load_parts():
    parts = []
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'robot_parts_store.csv')
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['id'] = int(row['id'])
            row['price'] = float(row['price'])
            parts.append(row)
    return parts

# ---- Basic AI response logic (Replace with your actual LLM or RAG backend) ----
def answer_question(query, parts_data):
    query = query.lower()

    for part in parts_data:
        if part['name'].lower() in query:
            return f"Yes, we have {part['name']} from {part['brand']} priced at ${part['price']}."

    if "delivery" in query or "shipping" in query:
        return "We offer standard shipping across the US. Delivery takes 3-5 business days."

    if "discount" in query or "offer" in query:
        return "Currently, we offer a 10% discount for bulk orders above $500."

    return "Sorry, I couldn't find a clear answer to your question. Can you rephrase?"

# ---- Routes ----
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/parts')
def parts_list():
    search_query = request.args.get('q', '')
    parts = load_parts()
    filtered_parts = [p for p in parts if search_query.lower() in p['name'].lower()] if search_query else parts
    return render_template('parts.html', parts=filtered_parts)

@app.route('/parts/<int:part_id>')
def part_detail(part_id):
    parts = load_parts()
    part = next((p for p in parts if p['id'] == part_id), None)
    if not part:
        return "Part not found", 404
    return render_template('part_detail.html', part=part)

# ---- AI Ask Route ----
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    parts = load_parts()
    response = answer_question(question, parts)
    return jsonify({"answer": response})

if __name__ == '__main__':
    app.run(debug=True)
