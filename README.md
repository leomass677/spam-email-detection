# Spam Email Classification System

.\.venv\Scripts\python.exe -m streamlit run enhanced_app.py

A production-grade machine learning system designed to robustly classify emails as "Spam" or "Ham" (legitimate). This project features a modular pipeline architecture for training and inference, integrated with a modern, beautifully designed web interface for easy interaction.

## 🚀 Key Features

- **Advanced ML Pipeline**: Modular design separating data ingestion, transformation, and model training.
- **Multiple Model Support**: Evaluation of various algorithms including SVM, Logistic Regression, Decision Trees, and Random Forest.
- **Beautiful Web UI**: Enhanced Streamlit interface with custom CSS, animations, and responsive design.
- **MBOX Support**: Native capability to process and classify entire `mbox` email archives.
- **Real-time Classification**: Instant analysis of single emails with confidence scores.
- **Batch Processing**: Process multiple emails from MBOX files with detailed analytics.
- **Detailed Analytics**: Comprehensive logging and performance metrics (Precision, Recall, F1-Score).

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Frontend**: Streamlit with Custom HTML/CSS
- **ML Framework**: Scikit-learn
- **Data Processing**: Pandas, NumPy, BeautifulSoup4
- **Project Management**: `uv` (recommended) or `pip`

## 📂 Project Structure

```
├── enhanced_app.py         # Enhanced Streamlit Web Application with Custom UI
├── streamlit_app.py        # Original Streamlit App
├── flask_app.py           # Flask Web Application (Alternative)
├── requirements.txt        # Project dependencies
├── main.py                 # (Optional) Alternative entry point
├── templates/              # HTML Templates for Flask App
├── static/                 # CSS and JS files
│   ├── css/
│   │   └── style.css       # Custom stylesheets
│   └── js/
│       └── script.js       # JavaScript functionality
├── src/
│   ├── components/         # Core processing modules (Ingestion, Transformation)
│   ├── pipeline/           # Orchestration pipelines (Training, Prediction)
│   ├── config/             # Configuration and parameters
│   └── utils/              # Helper functions, logging, and state management
├── data/                   # Dataset storage (inputs)
├── outputs/                # Training artifacts (models, vectorizers)
└── logs/                   # System runtime logs
```

## ⚡ Installation

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd Spam-Email-Detection
   ```

2. **Set up Environment**
   It is recommended to use a virtual environment.

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🎨 Running the Enhanced Web Application

### Streamlit App (Recommended)

```bash
streamlit run enhanced_app.py
```

### Flask App (Alternative)

```bash
python flask_app.py
```

The application will be available at `http://localhost:8501` (Streamlit) or `http://localhost:5000` (Flask).

## 📊 Usage

### Single Email Classification

1. Navigate to the "Single Email" tab
2. Paste your email content into the text area
3. Click "Classify Email" to get instant results with confidence scores

### Batch Processing

1. Switch to the "Batch Processing" tab
2. Upload an MBOX file exported from your email client
3. Click "Process File" to analyze all emails
4. View summary statistics and download detailed results as CSV

## 🎨 UI Features

- **Modern Design**: Gradient backgrounds, card-based layouts, and smooth animations
- **Responsive**: Works seamlessly on desktop and mobile devices
- **Interactive**: Hover effects, loading animations, and progress indicators
- **Accessible**: Clear visual feedback for spam/ham classifications
- **Professional**: Clean typography and intuitive navigation

## 🔧 Configuration

Model configurations and parameters can be adjusted in `src/config/config.py`:

- **Models**: SVM, Logistic Regression, Decision Trees, KNN, Random Forest
- **Features**: TF-IDF vectorization with customizable parameters
- **Paths**: Configurable input/output directories

## 📈 Model Performance

The system achieves high accuracy through:

- **Feature Engineering**: Text preprocessing, cleaning, and TF-IDF transformation
- **Model Selection**: Cross-validation across multiple algorithms
- **Hyperparameter Tuning**: Grid search optimization
- **Evaluation Metrics**: Precision, Recall, F1-Score analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Streamlit for the web interface
- Machine learning powered by Scikit-learn
- Email processing using Python's mailbox module

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🖥️ Usage

### 1. Running the Web Application

Launch the interactive dashboard to classify emails instantly.

```bash
streamlit run app.py
```

- **Single Email Tab**: Paste email content to get an immediate Spam/Ham prediction with a confidence score.
- **Batch Processing Tab**: Upload an `.mbox` file to process multiple emails at once and download the results as a CSV.

### 2. Training the Model

(Optional) If you wish to retrain the models on new data:

1. Place your dataset in `data/dataset/dataset.csv`.
2. Run the training pipeline:
   ```bash
   python -m src.pipeline.training_pipeline
   ```
3. Artifacts (Model & Vectorizer) will be saved in the `outputs/` directory.
4. **Important**: Update `src/config/config.py` with the new paths to your generated model and vectorizer if they change.

## ⚙️ Configuration

The system is highly configurable via `src/config/config.py`. You can adjust:

- Model hyperparameters (Grid Search configuration)
- Input/Output paths
- Training parameters (Cross-validation folds, etc.)

## 📊 Model Performance

The pipeline automatically evaluates models using 5-fold cross-validation. Metrics including Accuracy, Precision, Recall, and F1-Score are logged for each experiment. By default, the system selects the best performing model (often SVM or Random Forest) for inference.

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
