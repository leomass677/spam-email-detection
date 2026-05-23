from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import tempfile
import os
import time
from werkzeug.utils import secure_filename
from src.pipeline.prediction_pipeline import PredictionPipeline

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize pipeline
pipeline = PredictionPipeline(load_models=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    email_text = data.get('email_text', '')

    if not email_text.strip():
        return jsonify({'error': 'Please provide email text'}), 400

    try:
        result = pipeline.predict_single_email(email_text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.lower().endswith(('.mbox', '.txt')):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            df = pipeline.predict_mbox_file(filepath)
            # Convert to dict for JSON response
            results = df.to_dict('records')
            summary = {
                'total_emails': len(df),
                'spam_count': len(df[df['Prediction'] == 'Spam']),
                'ham_count': len(df[df['Prediction'] == 'Ham'])
            }
            return jsonify({'results': results, 'summary': summary})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            # Cleanup
            if os.path.exists(filepath):
                os.remove(filepath)
    else:
        return jsonify({'error': 'Invalid file type. Please upload .mbox or .txt file'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)