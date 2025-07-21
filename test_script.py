import pandas as pd
import os
import requests
import json
import subprocess
from pathlib import Path
import shutil
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
BASE_DIR = r"C:\Users\sahan\one_dr_file\Documents\GitHub\000_openqquantify_ex"
DATA_FILE = os.path.join(BASE_DIR, "data", "robot_parts_store.csv")
ASSETS_DIR = os.path.join(BASE_DIR, "static", "assets", "3d")
BLENDER_PATH = "blender"  # Update with your Blender executable path if not in PATH
GLTFPACK_PATH = "gltfpack"  # Update with gltfpack path if not in PATH

# Ensure assets directory exists
os.makedirs(ASSETS_DIR, exist_ok=True)

def get_sketchfab_models(category, license_filter="cc0"):
    """Fetch CC0 models from Sketchfab for a given category."""
    url = "https://api.sketchfab.com/v3/models"
    params = {
        "downloadable": True,
        "license": license_filter,
        "q": category,  # Search query
        "count": 10,    # Limit results for testing
        "sort_by": "-publishedAt"
    }
    headers = {"Authorization": "Bearer YOUR_SKETCHFAB_API_TOKEN"}  # Replace with your API token
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        models = response.json().get("results", [])
        return [
            {
                "uid": model["uid"],
                "name": model["name"],
                "download_url": model.get("archives", {}).get("gltf", {}).get("url")
            }
            for model in models if model.get("archives", {}).get("gltf")
        ]
    except requests.RequestException as e:
        logger.error(f"Error fetching Sketchfab models for {category}: {e}")
        return []

def get_poly_pizza_models(category):
    """Fetch CC0 models from Poly Pizza."""
    url = f"https://api.poly.pizza/v1/search?term={category}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        models = response.json().get("results", [])
        return [
            {
                "id": model["id"],
                "name": model["name"],
                "download_url": f"https://api.poly.pizza/v1/asset/{model['id']}/download/glb"
            }
            for model in models
        ]
    except requests.RequestException as e:
        logger.error(f"Error fetching Poly Pizza models for {category}: {e}")
        return []

def get_quaternius_models(category):
    """Placeholder for Quaternius models (no public API, manual download simulation)."""
    # Quaternius doesn't have a public API; you may need to scrape or manually download
    # For demonstration, assume a local mapping or pre-downloaded assets
    logger.warning(f"Quaternius API not available. Please manually download CC0 assets for {category} from quaternius.com")
    return []

def get_kenney_models(category):
    """Placeholder for Kenney.nl models (no public API, manual download simulation)."""
    # Kenney.nl provides direct downloads; simulate with a static mapping
    logger.warning(f"Kenney.nl API not available. Please manually download CC0 assets for {category} from kenney.nl")
    return []

def get_blenderkit_models(category):
    """Fetch CC0 models from BlenderKit."""
    url = "https://www.blenderkit.com/api/v1/search/"
    params = {
        "query": f"asset_type:model license:cc0 {category}",
        "page_size": 10
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        models = response.json().get("results", [])
        return [
            {
                "id": model["asset_id"],
                "name": model["name"],
                "download_url": model.get("download_url")
            }
            for model in models if model.get("download_url")
        ]
    except requests.RequestException as e:
        logger.error(f"Error fetching BlenderKit models for {category}: {e}")
        return []

def download_model(url, output_path):
    """Download a model file from a URL."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logger.info(f"Downloaded model to {output_path}")
        return True
    except requests.RequestException as e:
        logger.error(f"Error downloading model from {url}: {e}")
        return False

def convert_to_glb(input_path, output_path):
    """Convert a model to GLB format using Blender."""
    script = f"""
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath='{input_path}')
bpy.ops.export_scene.gltf(filepath='{output_path}', export_format='GLB')
"""
    script_path = os.path.join(BASE_DIR, "convert.py")
    with open(script_path, "w") as f:
        f.write(script)
    
    try:
        subprocess.run([BLENDER_PATH, "--background", "--python", script_path], check=True)
        logger.info(f"Converted {input_path} to {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error converting {input_path} to GLB: {e}")
        return False
    finally:
        if os.path.exists(script_path):
            os.remove(script_path)

def optimize_glb(input_path, output_path):
    """Optimize GLB file using gltfpack."""
    try:
        subprocess.run([GLTFPACK_PATH, "-i", input_path, "-o", output_path, "-cc"], check=True)
        logger.info(f"Optimized {input_path} to {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error optimizing {input_path}: {e}")
        return False

def process_category(category):
    """Process a single category, fetching and converting models."""
    logger.info(f"Processing category: {category}")
    models = []
    
    # Fetch models from different sources
    models.extend(get_sketchfab_models(category))
    models.extend(get_poly_pizza_models(category))
    models.extend(get_quaternius_models(category))
    models.extend(get_kenney_models(category))
    models.extend(get_blenderkit_models(category))
    
    for model in models:
        if not model.get("download_url"):
            continue
        
        # Define file paths
        temp_path = os.path.join(ASSETS_DIR, f"temp_{model['id']}.glb")
        final_path = os.path.join(ASSETS_DIR, f"{category}_{model['id']}.glb")
        
        # Download
        if download_model(model["download_url"], temp_path):
            # Optimize
            if optimize_glb(temp_path, final_path):
                logger.info(f"Saved optimized model for {category} at {final_path}")
                os.remove(temp_path)  # Clean up temp file
            else:
                # If optimization fails, use the original
                shutil.move(temp_path, final_path)
                logger.info(f"Saved unoptimized model for {category} at {final_path}")

def main():
    # Read categories from CSV
    try:
        df = pd.read_csv(DATA_FILE)
        categories = df['Category'].unique()
        logger.info(f"Found categories: {categories}")
    except FileNotFoundError as e:
        logger.error(f"CSV file not found: {e}")
        return
    
    # Process each category
    for category in categories:
        process_category(category)
        time.sleep(1)  # Rate limiting to avoid overwhelming APIs

if __name__ == "__main__":
    main()