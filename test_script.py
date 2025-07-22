import pandas as pd
import os
import requests
import json
import subprocess
import shutil
import time
import logging
import zipfile
import tempfile
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
BASE_DIR = r"C:\Users\sahan\one_dr_file\Documents\GitHub\000_openqquantify_ex"
DATA_FILE = os.path.join(BASE_DIR, "data", "robot_parts_store.csv")
ASSETS_DIR = os.path.join(BASE_DIR, "static", "assets", "3d")
BLENDER_PATH = "blender"
GLTFPACK_PATH = "gltfpack"

# Ensure assets directory exists
os.makedirs(ASSETS_DIR, exist_ok=True)

# API Configuration
SKETCHFAB_API_TOKEN = os.getenv('SKETCHFAB_API_TOKEN', 'your_sketchfab_token_here')
BLENDERKIT_API_TOKEN = os.getenv('BLENDERKIT_API_TOKEN', 'your_blenderkit_token_here')

def get_sketchfab_models(category, license_filter="cc0"):
    """Fetch CC0 models from Sketchfab for a given category."""
    url = "https://api.sketchfab.com/v3/models"
    params = {
        "downloadable": True,
        "license": license_filter,
        "q": category,
        "count": 5,
        "sort_by": "-publishedAt"
    }
    headers = {"Authorization": f"Bearer {SKETCHFAB_API_TOKEN}"}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        models = response.json().get("results", [])
        
        valid_models = []
        for model in models:
            # Updated structure: archives > gltf > files > url
            archives = model.get("archives", {})
            gltf_archive = archives.get("gltf", {})
            files = gltf_archive.get("files", [])
            
            if files:
                # Find the highest resolution file
                best_file = max(files, key=lambda x: x.get("size", 0))
                download_url = best_file.get("url")
                
                if download_url:
                    valid_models.append({
                        "uid": model["uid"],
                        "name": model["name"],
                        "download_url": download_url,
                        "source": "sketchfab"
                    })
        return valid_models
    except (requests.RequestException, json.JSONDecodeError) as e:
        logger.error(f"Error fetching Sketchfab models for {category}: {str(e)}")
        return []

def get_poly_pizza_models(category):
    """Fetch CC0 models from Poly Pizza."""
    url = f"https://poly.pizza/search/{category}?license=1"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        models = response.json().get("results", [])
        return [{
            "id": model["id"],
            "name": model["name"],
            "download_url": f"https://api.poly.pizza/v1/asset/{model['id']}/download/glb",
            "source": "poly_pizza"
        } for model in models]
    except (requests.RequestException, json.JSONDecodeError) as e:
        logger.error(f"Error fetching Poly Pizza models for {category}: {str(e)}")
        return []

def get_blenderkit_models(category):
    """Fetch CC0 models from BlenderKit."""
    url = "https://www.blenderkit.com/api/v1/search/"
    params = {
        "query": f"asset_type:model license:cc0 {category}",
        "page_size": 5
    }
    headers = {"Authorization": f"Token {BLENDERKIT_API_TOKEN}"}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        models = response.json().get("results", [])
        return [{
            "id": model["id"],
            "name": model["name"],
            "download_url": model.get("files", [{}])[0].get("download_url"),
            "source": "blenderkit"
        } for model in models if model.get("files")]
    except (requests.RequestException, json.JSONDecodeError) as e:
        logger.error(f"Error fetching BlenderKit models for {category}: {str(e)}")
        return []

def download_model(url, output_path, headers=None):
    """Download a model file from a URL."""
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=60)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logger.info(f"Downloaded model to {output_path}")
        return True
    except requests.RequestException as e:
        logger.error(f"Error downloading model from {url}: {str(e)}")
        return False

def extract_zip(zip_path, output_dir):
    """Extract ZIP file to directory."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        logger.info(f"Extracted ZIP to {output_dir}")
        return True
    except (zipfile.BadZipFile, OSError) as e:
        logger.error(f"Error extracting ZIP {zip_path}: {str(e)}")
        return False

def find_main_gltf(extracted_dir):
    """Find main glTF file in extracted directory."""
    for root, _, files in os.walk(extracted_dir):
        for file in files:
            if file.endswith('.gltf') or file.endswith('.glb'):
                return os.path.join(root, file)
    return None

def convert_to_glb(input_path, output_path):
    """Convert a model to GLB format using Blender."""
    input_path_fixed = input_path.replace("\\", "/")
    output_path_fixed = output_path.replace("\\", "/")

    script = f"""import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=r'{input_path_fixed}')
    bpy.ops.export_scene.gltf(filepath=r'{output_path_fixed}', export_format='GLB')
    """
    script_path = os.path.join(BASE_DIR, "convert.py")
    with open(script_path, "w") as f:
        f.write(script)
    
    try:
        subprocess.run([BLENDER_PATH, "--background", "--python", script_path], 
                       check=True, 
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        logger.info(f"Converted {input_path} to {output_path}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Error converting {input_path} to GLB: {str(e)}")
        return False
    finally:
        if os.path.exists(script_path):
            os.remove(script_path)

def optimize_glb(input_path, output_path):
    """Optimize GLB file using gltfpack."""
    try:
        subprocess.run(
            [GLTFPACK_PATH, "-i", input_path, "-o", output_path, "-cc"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        logger.info(f"Optimized {input_path} to {output_path}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Error optimizing {input_path}: {str(e)}")
        return False

def process_model(model, category):
    """Process a single model from any source."""
    source = model.get("source", "unknown")
    model_id = model.get("uid") or model.get("id") or "unknown"
    model_name = model.get("name", "unnamed").replace(" ", "_")[:50]
    
    # Create temp directory for processing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = os.path.join(temp_dir, f"model_{model_id}")
        final_path = os.path.join(ASSETS_DIR, f"{category}_{source}_{model_id}_{model_name}.glb")
        
        # Skip if file already exists
        if os.path.exists(final_path):
            logger.info(f"Skipping existing model: {final_path}")
            return
        
        # Handle different download types
        if model['download_url'].endswith('.zip'):
            # Download ZIP archive
            zip_path = f"{temp_path}.zip"
            if download_model(model['download_url'], zip_path):
                # Extract and find main GLTF file
                if extract_zip(zip_path, temp_dir):
                    gltf_file = find_main_gltf(temp_dir)
                    if gltf_file:
                        # Convert to GLB if needed
                        if gltf_file.endswith('.gltf'):
                            glb_file = f"{temp_path}.glb"
                            if convert_to_glb(gltf_file, glb_file):
                                # Optimize and save
                                if optimize_glb(glb_file, final_path):
                                    logger.info(f"Saved optimized model at {final_path}")
                                else:
                                    shutil.copy(glb_file, final_path)
                                    logger.info(f"Saved unoptimized model at {final_path}")
                        else:
                            # Already GLB format
                            if optimize_glb(gltf_file, final_path):
                                logger.info(f"Saved optimized model at {final_path}")
                            else:
                                shutil.copy(gltf_file, final_path)
                                logger.info(f"Saved unoptimized model at {final_path}")
                    else:
                        logger.error(f"No GLTF/GLB found in downloaded archive for {model_name}")
                else:
                    logger.error(f"Failed to extract ZIP archive for {model_name}")
            else:
                logger.error(f"Failed to download ZIP archive for {model_name}")
        else:
            # Direct GLB download
            glb_file = f"{temp_path}.glb"
            headers = {"Authorization": f"Token {BLENDERKIT_API_TOKEN}"} if source == "blenderkit" else None
            if download_model(model['download_url'], glb_file, headers):
                # Optimize and save
                if optimize_glb(glb_file, final_path):
                    logger.info(f"Saved optimized model at {final_path}")
                else:
                    shutil.copy(glb_file, final_path)
                    logger.info(f"Saved unoptimized model at {final_path}")
            else:
                logger.error(f"Failed to download model for {model_name}")

def process_category(category):
    """Process a single category, fetching and converting models."""
    logger.info(f"Processing category: {category}")
    
    # Fetch models from different sources
    models = []
    models.extend(get_sketchfab_models(category))
    models.extend(get_poly_pizza_models(category))
    models.extend(get_blenderkit_models(category))
    
    logger.info(f"Found {len(models)} models for {category}")
    
    # Process each model
    for i, model in enumerate(models):
        logger.info(f"Processing model {i+1}/{len(models)}: {model.get('name')}")
        process_model(model, category)
        time.sleep(2)  # Rate limiting

def main():
    # Read categories from CSV
    try:
        df = pd.read_csv(DATA_FILE)
        categories = df['Category'].unique().tolist()
        logger.info(f"Found {len(categories)} categories: {categories}")
    except Exception as e:
        logger.error(f"Error reading CSV: {str(e)}")
        return
    
    # Process each category
    for category in categories:
        process_category(category)
        time.sleep(5)  # Category-level rate limiting

if __name__ == "__main__":
    main()