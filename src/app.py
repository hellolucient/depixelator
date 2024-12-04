from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
import os
from analyzer import analyze_pixel_art
from processor import reconstruct_pixel_art
import json

# Create the Flask app with the correct template folder
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')
app = Flask(__name__, template_folder=template_dir)

# Alternative configuration using project root
project_root = os.path.dirname(os.path.dirname(__file__))  # Go up one level from src
app.config['UPLOAD_FOLDER'] = os.path.join(project_root, 'uploads')
app.config['DOWNLOAD_FOLDER'] = os.path.join(project_root, 'downloads')

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    print("Upload folder:", app.config['UPLOAD_FOLDER'])
    print("Download folder:", app.config['DOWNLOAD_FOLDER'])
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Get pixel sizes from form
        pixel_size_x = int(request.form.get('pixel_size_x', 25))
        pixel_size_y = int(request.form.get('pixel_size_y', 25))
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the image with pixel sizes
        result = analyze_pixel_art(filepath, pixel_size=pixel_size_x)  # For now, using X size
        
        if not result or 'analysis' not in result:
            return jsonify({'error': 'Analysis failed to produce valid results'}), 500
            
        print("Analysis result:", result)  # Debug print
        
        # Save files for download
        reconstructed_path = os.path.join(app.config['DOWNLOAD_FOLDER'], f'reconstructed_{filename}')
        reconstructed = reconstruct_pixel_art(result)
        reconstructed.save(reconstructed_path)
        
        # Save analysis JSON
        analysis_path = os.path.join(app.config['DOWNLOAD_FOLDER'], 'detailed_analysis.json')
        with open(analysis_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        # Save pixel data JSON
        pixel_data_path = os.path.join(app.config['DOWNLOAD_FOLDER'], 'pixel_data.json')
        with open(pixel_data_path, 'w') as f:
            json.dump({
                'metadata': result['metadata'],
                'pixels': {coord: list(color) for coord, color in result['pixels'].items()}
            }, f, indent=2)
        
        return jsonify(result)
    except Exception as e:
        print(f"Error during analysis: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

@app.route('/download/reconstructed')
def download_reconstructed():
    # Get the most recent reconstructed image
    files = os.listdir(app.config['DOWNLOAD_FOLDER'])
    reconstructed_files = [f for f in files if f.startswith('reconstructed_')]
    if not reconstructed_files:
        return "No reconstructed image available", 404
    
    latest_file = max(reconstructed_files, key=lambda x: os.path.getctime(
        os.path.join(app.config['DOWNLOAD_FOLDER'], x)))
    return send_file(
        os.path.join(app.config['DOWNLOAD_FOLDER'], latest_file),
        as_attachment=True
    )

@app.route('/download/analysis')
def download_analysis():
    analysis_path = os.path.join(app.config['DOWNLOAD_FOLDER'], 'detailed_analysis.json')
    if not os.path.exists(analysis_path):
        return "Analysis file not found", 404
    return send_file(analysis_path, as_attachment=True)

@app.route('/download/pixel_data')
def download_pixel_data():
    pixel_data_path = os.path.join(app.config['DOWNLOAD_FOLDER'], 'pixel_data.json')
    if not os.path.exists(pixel_data_path):
        return "Pixel data file not found", 404
    return send_file(pixel_data_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5001) 