from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

def load_parts():
    parts = []
    csv_path = os.path.join(os.path.dirname(__file__), 'data\\robot_parts_store.csv')
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert price to int if needed, id to int, etc.
            row['id'] = int(row['id'])
            row['price'] = int(row['price'])
            parts.append(row)
    return parts

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

if __name__ == '__main__':
    app.run(debug=True)