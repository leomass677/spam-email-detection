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
                    
                    if confidence:
                        st.info(f"Confidence Score: {confidence:.1f}%")
                        
                except Exception as e:
                    st.error(f"Error analyzing email: {str(e)}")
        else:
            st.warning("Please enter some text to classify.")

with tab2:
    st.header("Process MBOX File")
    uploaded_file = st.file_uploader("Upload an MBOX file", type=['mbox', 'txt'])
    
    if uploaded_file is not None:
        if st.button("Process File"):
            with st.spinner("Processing file... this may take a moment"):
                try:
                    # Save uploaded file to temp
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mbox') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    try:
                        # Process file
                        df = pipeline.predict_mbox_file(tmp_path)
                        
                        # Show summary metrics
                        col1, col2 = st.columns(2)
                        spam_count = len(df[df['Prediction'] == 'Spam'])
                        ham_count = len(df[df['Prediction'] == 'Ham'])
                        
                        col1.metric("Total Emails", len(df))
                        col2.metric("Spam Found", spam_count, delta_color="inverse")
                        
                        # Show previews
                        st.subheader("Results Preview")
                        st.dataframe(df[['Time', 'Subject', 'Prediction']].head(10))
                        
                        # Download button
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download Full Results (CSV)",
                            data=csv,
                            file_name=f"predictions_{int(time.time())}.csv",
                            mime="text/csv",
                        )
                        
                    finally:
                        # Cleanup temp file
                        if os.path.exists(tmp_path):
                            try:
                                os.unlink(tmp_path)
                            except:
                                pass # Sometimes file lock prevents deletion on Windows
                                
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
