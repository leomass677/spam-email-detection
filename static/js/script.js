// Spam Email Classifier JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Single email form submission
    const singleEmailForm = document.getElementById('singleEmailForm');
    const classifyBtn = document.getElementById('classifyBtn');
    const resultDiv = document.getElementById('result');
    const resultContent = document.getElementById('resultContent');

    singleEmailForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const emailText = document.getElementById('emailText').value.trim();

        if (!emailText) {
            showAlert('Please enter some email text to classify.', 'warning');
            return;
        }

        // Show loading
        showLoading('Analyzing email...');
        classifyBtn.disabled = true;

        // Send request
        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email_text: emailText })
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            classifyBtn.disabled = false;

            if (data.error) {
                showAlert(data.error, 'danger');
                return;
            }

            displayResult(data);
        })
        .catch(error => {
            hideLoading();
            classifyBtn.disabled = false;
            showAlert('An error occurred while classifying the email.', 'danger');
            console.error('Error:', error);
        });
    });

    // Batch processing form submission
    const batchForm = document.getElementById('batchForm');
    const processBtn = document.getElementById('processBtn');
    const batchResultDiv = document.getElementById('batchResult');
    const batchResultContent = document.getElementById('batchResultContent');

    batchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];

        if (!file) {
            showAlert('Please select a file to upload.', 'warning');
            return;
        }

        // Show loading
        showLoading('Processing file... This may take a moment.');
        processBtn.disabled = true;

        // Create form data
        const formData = new FormData();
        formData.append('file', file);

        // Send request
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            processBtn.disabled = false;

            if (data.error) {
                showAlert(data.error, 'danger');
                return;
            }

            displayBatchResult(data);
        })
        .catch(error => {
            hideLoading();
            processBtn.disabled = false;
            showAlert('An error occurred while processing the file.', 'danger');
            console.error('Error:', error);
        });
    });

    function displayResult(data) {
        const prediction = data.prediction;
        const confidence = data.confidence;

        let resultHtml = '';

        if (prediction === 'Spam') {
            resultHtml = `
                <div class="alert alert-spam result-spam">
                    <h4 class="alert-heading"><i class="fas fa-exclamation-triangle"></i> 🚨 SPAM DETECTED!</h4>
                    <p>This email has been classified as spam.</p>
                    ${confidence ? `<p><strong>Confidence:</strong> ${confidence.toFixed(1)}%</p>` : ''}
                </div>
            `;
        } else {
            resultHtml = `
                <div class="alert alert-ham result-ham">
                    <h4 class="alert-heading"><i class="fas fa-check-circle"></i> ✅ SAFE EMAIL</h4>
                    <p>This email has been classified as ham (safe).</p>
                    ${confidence ? `<p><strong>Confidence:</strong> ${confidence.toFixed(1)}%</p>` : ''}
                </div>
            `;
        }

        resultContent.innerHTML = resultHtml;
        resultDiv.style.display = 'block';

        // Scroll to result
        resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function displayBatchResult(data) {
        const summary = data.summary;
        const results = data.results;

        let resultHtml = `
            <div class="row mb-4">
                <div class="col-md-4">
                    <div class="metric-card">
                        <div class="metric-value">${summary.total_emails}</div>
                        <div class="metric-label">Total Emails</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="metric-card">
                        <div class="metric-value text-danger">${summary.spam_count}</div>
                        <div class="metric-label">Spam Detected</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="metric-card">
                        <div class="metric-value text-success">${summary.ham_count}</div>
                        <div class="metric-label">Safe Emails</div>
                    </div>
                </div>
            </div>
        `;

        if (results.length > 0) {
            resultHtml += `
                <h5>Results Preview (First 10 emails):</h5>
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Time</th>
                                <th>Subject</th>
                                <th>Prediction</th>
                            </tr>
                        </thead>
                        <tbody>
            `;

            results.slice(0, 10).forEach(row => {
                const predictionClass = row.Prediction === 'Spam' ? 'text-danger' : 'text-success';
                resultHtml += `
                    <tr>
                        <td>${row.Time || 'N/A'}</td>
                        <td>${row.Subject || 'N/A'}</td>
                        <td class="${predictionClass}"><strong>${row.Prediction}</strong></td>
                    </tr>
                `;
            });

            resultHtml += `
                        </tbody>
                    </table>
                </div>
            `;
        }

        batchResultContent.innerHTML = resultHtml;
        batchResultDiv.style.display = 'block';

        // Scroll to result
        batchResultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function showLoading(text) {
        document.getElementById('loadingText').textContent = text;
        const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
        modal.show();
    }

    function hideLoading() {
        const modal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
        if (modal) {
            modal.hide();
        }
    }

    function showAlert(message, type) {
        // Create alert element
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insert at top of container
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);

        // Auto dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    // Add some interactive effects
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // File input feedback
    const fileInput = document.getElementById('fileInput');
    fileInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const fileName = file.name;
            const fileSize = (file.size / 1024 / 1024).toFixed(2);
            showAlert(`Selected file: ${fileName} (${fileSize} MB)`, 'info');
        }
    });
});