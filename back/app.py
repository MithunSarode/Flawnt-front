from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import base64
from PIL import Image
import io
from sklearn.cluster import KMeans
import json

app = Flask(__name__)
CORS(app)

def extract_skin_tone(image_data):
    # Convert base64 to image
    image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes))
    
    # Convert to numpy array
    img_array = np.array(image)
    
    # Convert to RGB if image is in BGR format
    if len(img_array.shape) == 3 and img_array.shape[2] == 3:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    
    # Get center region of the image (face area)
    height, width = img_array.shape[:2]
    center_x, center_y = width // 2, height // 2
    sample_size = min(width, height) // 4
    
    start_x = max(0, center_x - sample_size // 2)
    start_y = max(0, center_y - sample_size // 2)
    end_x = min(width, center_x + sample_size // 2)
    end_y = min(height, center_y + sample_size // 2)
    
    face_region = img_array[start_y:end_y, start_x:end_x]
    
    # Reshape for clustering
    pixels = face_region.reshape(-1, 3)
    
    # Use K-means to find dominant colors
    kmeans = KMeans(n_clusters=5, random_state=42)
    kmeans.fit(pixels)
    
    # Get the dominant colors
    colors = kmeans.cluster_centers_
    
    # Calculate average RGB values
    avg_r = np.mean(colors[:, 0])
    avg_g = np.mean(colors[:, 1])
    avg_b = np.mean(colors[:, 2])
    
    # Calculate ratios for undertone determination
    red_green_ratio = avg_r / avg_g if avg_g != 0 else 1
    red_blue_ratio = avg_r / avg_b if avg_b != 0 else 1
    
    # Determine undertone
    if red_green_ratio > 1.1 and red_blue_ratio > 1.1:
        undertone = "Warm"
        undertone_desc = "Your skin has warm undertones with golden or peachy hues."
        color_palette = {
            "primary": ["#FFD700", "#FFA500", "#FF8C00"],
            "secondary": ["#8B4513", "#A0522D", "#CD853F"],
            "accent": ["#FF4500", "#FF6347", "#FF7F50"],
            "makeup": {
                "foundation": ["Warm Beige", "Golden", "Honey"],
                "blush": ["Peach", "Coral", "Warm Pink"],
                "lipstick": ["Coral", "Terracotta", "Warm Red"]
            }
        }
    elif red_green_ratio < 0.9 and red_blue_ratio < 0.9:
        undertone = "Cool"
        undertone_desc = "Your skin has cool undertones with pink or blue hues."
        color_palette = {
            "primary": ["#4169E1", "#1E90FF", "#00BFFF"],
            "secondary": ["#9370DB", "#8A2BE2", "#9400D3"],
            "accent": ["#FF69B4", "#FF1493", "#C71585"],
            "makeup": {
                "foundation": ["Cool Beige", "Porcelain", "Ivory"],
                "blush": ["Rose", "Berry", "Plum"],
                "lipstick": ["Berry", "Fuchsia", "Cool Red"]
            }
        }
    else:
        undertone = "Neutral"
        undertone_desc = "Your skin has neutral undertones, balancing warm and cool tones."
        color_palette = {
            "primary": ["#808080", "#A9A9A9", "#D3D3D3"],
            "secondary": ["#2F4F4F", "#556B2F", "#6B8E23"],
            "accent": ["#B8860B", "#DAA520", "#CD853F"],
            "makeup": {
                "foundation": ["Neutral Beige", "Sand", "Nude"],
                "blush": ["Soft Pink", "Mauve", "Rose"],
                "lipstick": ["Nude", "Rose", "Mauve"]
            }
        }
    
    return {
        "undertone": undertone,
        "undertoneDesc": undertone_desc,
        "colorPalette": color_palette,
        "rgbValues": {
            "r": int(avg_r),
            "g": int(avg_g),
            "b": int(avg_b)
        }
    }

@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        data = request.json
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({"error": "No image data provided"}), 400
        
        result = extract_skin_tone(image_data)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 