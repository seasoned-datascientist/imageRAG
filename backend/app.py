from flask import Flask, jsonify, request, send_from_directory
import os
import torch
import clip
from PIL import Image, ImageFile
import numpy as np
import faiss
import glob
from flask_cors import CORS

# Set up Flask app
app = Flask(__name__)

# Define dataset path for images
DATASET_PATH = "./images-sample"
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Set PIL to allow truncated images (optional)
ImageFile.LOAD_TRUNCATED_IMAGES = False

# Enable CORS for all routes
CORS(app)

# Function to get image embeddings
def get_image_embeddings(image_paths):
    embeddings = []
    model.eval()
    with torch.no_grad():
        for path in image_paths:
            image = Image.open(path).convert("RGB")
            image_tensor = preprocess(image).unsqueeze(0).to(device)
            embedding = model.encode_image(image_tensor).cpu().numpy()
            embeddings.append(embedding)
    return np.vstack(embeddings) if embeddings else np.array([])

# Load images for retrieval
image_files = glob.glob(os.path.join(DATASET_PATH, "*.jpg"))
valid_image_files = image_files  # All images are considered valid now

# Now get the embeddings for valid images only
image_embeddings = get_image_embeddings(valid_image_files)

def normalize_embeddings(embeddings):
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    return embeddings / norms

# Normalize embeddings and add to FAISS index
if image_embeddings.size > 0:
    image_embeddings = normalize_embeddings(image_embeddings)
    d = image_embeddings.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(image_embeddings.astype("float32"))
else:
    print("No valid images found to process.")

# Serve image files from the dataset folder
@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(DATASET_PATH, filename)

# API endpoint to process text queries
@app.route('/search_by_text', methods=['POST'])
def search_by_text():
    query_text = request.json.get("query_text")
    text_tokens = clip.tokenize([query_text]).to(device)
    with torch.no_grad():
        text_embedding = model.encode_text(text_tokens).cpu().numpy()
    text_embedding = text_embedding / np.linalg.norm(text_embedding, axis=1, keepdims=True)
    distances, indices = index.search(text_embedding.astype("float32"), 5)
    return jsonify([os.path.basename(valid_image_files[i]) for i in indices[0]])

# API endpoint to process image queries
@app.route('/search_by_image', methods=['POST'])
def search_by_image():
    image_file = request.files['image']
    image = Image.open(image_file).convert("RGB")
    image_tensor = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        query_embedding = model.encode_image(image_tensor).cpu().numpy()
    query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
    distances, indices = index.search(query_embedding.astype("float32"), 5)
    return jsonify([os.path.basename(valid_image_files[i]) for i in indices[0]])

# Home route
@app.route('/')
def home():
    return "Welcome to the Flask App!"

if __name__ == '__main__':
    app.run(debug=True)
