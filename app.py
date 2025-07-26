from flask import Flask, render_template, request, jsonify, render_template_string
import json
import os
import csv
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from ai_routes import ai_bp

app = Flask(__name__)
app.register_blueprint(ai_bp, url_prefix='/ai')

# Configuration for data directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
STATIC_DIR = BASE_DIR / 'static'
ASSETS_3D_DIR = STATIC_DIR / 'assets' / '3d'

# Create directories if they don't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_3D_DIR.mkdir(parents=True, exist_ok=True)

# Load products from CSV
def load_products():
    csv_path = DATA_DIR / 'robot_parts_store.csv'
    products = []
    
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                product = {
                    "id": row['ProductID'],
                    "name": row['ProductName'],
                    "category": row['Category'].lower(),
                    "brand": row['Brand'],
                    "price": float(row['Price']),
                    "in_stock": int(row['InStock']) > 0,
                    "description": row['Description'],
                    "currency": row['Currency'],
                    # Generated fields for UI compatibility
                    "rating": 4.0 + (i % 5) * 0.2,  # 4.0-5.0
                    "reviews": 50 + (i % 5) * 30,    # 50-200
                    "image": f"/static/images/product_{i % 6 + 1}.jpg",
                    "featured": i < 3  # First 3 items are featured
                }
                products.append(product)
        return products
    except FileNotFoundError:
        print(f"CSV file not found at {csv_path}. Using sample data.")
        # Fallback sample data
        return [
            {
                "id": "RB000001",
                "name": "AutoBotics Series-494",
                "category": "cables",
                "brand": "RoboTech",
                "price": 371.66,
                "in_stock": True,
                "description": "High-quality robotics cable",
                "currency": "USD",
                "rating": 4.8,
                "reviews": 120,
                "image": "/static/images/product_1.jpg",
                "featured": True
            }
        ]

# Load 3D gallery items from directory
def load_gallery_items():
    gallery_items = []
    supported_extensions = ['.glb', '.gltf', '.obj', '.fbx', '.stl']
    
    # Find all 3D model files in the directory
    model_files = [
        f for f in os.listdir(ASSETS_3D_DIR) 
        if os.path.splitext(f)[1].lower() in supported_extensions
    ]
    
    for i, filename in enumerate(model_files):
        name, ext = os.path.splitext(filename)
        gallery_items.append({
            "id": i + 1,
            "title": name.replace('_', ' ').title(),
            "category": "robotics",
            "artist": "3D Artist",
            "model_url": f"/static/assets/3d/{filename}",
            "thumbnail": f"/static/images/3d_thumb_{i % 3 + 1}.jpg",
            "description": f"3D model of {name}",
            "likes": 100 + i * 30,
            "views": 500 + i * 200,
            "featured": i < 3,
            "interactive": True,
            "downloadable": True
        })
    
    return gallery_items or [
        {
            "id": 1,
            "title": "Sample Robotic Arm",
            "category": "industrial",
            "artist": "Design Studio",
            "model_url": "/static/assets/3d/sample_arm.glb",
            "thumbnail": "/static/images/3d_thumb_1.jpg",
            "description": "Sample 3D robotic arm model",
            "likes": 150,
            "views": 850,
            "featured": True,
            "interactive": True,
            "downloadable": True
        }
    ]

# Load data at startup
PRODUCTS = load_products()
GALLERY_ITEMS = load_gallery_items()

def render_gallery_items(items):
    html = "".join([
        render_template("gallery_item.html", item=item) for item in items
    ])
    return html

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/products')
def get_products():
    category = request.args.get('category', 'all').lower()
    search = request.args.get('search', '').lower()
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 12))
    
    filtered_products = PRODUCTS
    
    if category != 'all':
        filtered_products = [p for p in filtered_products if p['category'] == category]
    
    if search:
        filtered_products = [
            p for p in filtered_products 
            if search in p['name'].lower() or search in p['description'].lower()
        ]
    
    # Pagination
    start = (page - 1) * page_size
    end = start + page_size
    paginated_products = filtered_products[start:end]
    total = len(filtered_products)
    
    return jsonify({
        'products': paginated_products,
        'total': total,
        'page': page,
        'page_size': page_size
    })

@app.route('/api/gallery')
def get_gallery():
    category = request.args.get('category', 'all').lower()
    filtered_items = GALLERY_ITEMS
    if category != 'all':
        filtered_items = [item for item in filtered_items if item['category'] == category]
    html = render_gallery_items(filtered_items)
    return jsonify({'html': html})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    
    # Simple AI response simulation
    responses = [
        "Great question! In robotics, this involves understanding the principles of kinematics and control systems...",
        "That's an excellent robotics topic! Let me break this down for you step by step...",
        "This is a fundamental concept in robotics engineering. Here's what you need to know...",
        "Interesting! This relates to several key areas in modern robotics including AI and mechanical design..."
    ]
    
    import random
    response = random.choice(responses)
    
    return jsonify({"response": response})

@app.route('/api/newsletter', methods=['POST'])
def newsletter():
    data = request.get_json()
    email = data.get('email', '')
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    # In a real app, you'd save this to a database
    return jsonify({"message": "Thank you for subscribing!"})

@app.route('/api/demo-request', methods=['POST'])
def demo_request():
    data = request.get_json()
    
    required_fields = ['fullName', 'email']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400
    
    # In a real app, you'd save this to a database
    return jsonify({"message": "Demo request submitted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
