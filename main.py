from flask import Flask, render_template, request, send_from_directory, jsonify
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array

import numpy as np
import os
import json
import sys
from datetime import datetime

# Import agents
from agents.explainability_agent import ExplainabilityAgent
from agents.clinical_chat_agent import ClinicalChatAgent

def check_prerequisites():
    """Check if all required files and directories exist before starting"""
    print("=" * 80)
    print("BRAIN TUMOR DETECTION SYSTEM - STARTUP CHECK")
    print("=" * 80)
    
    checks_passed = True
    
    print("\n[1] Checking required files...")
    required_files = [
        ('models/model.h5', 'Trained model'),
        ('templates/index.html', 'Frontend template'),
        ('agents/explainability_agent.py', 'Explainability Agent'),
        ('agents/clinical_chat_agent.py', 'Clinical Chat Agent'),
    ]
    
    for filepath, description in required_files:
        if os.path.exists(filepath):
            print(f"  ✓ {description} found")
        else:
            print(f"  ✗ {description} NOT FOUND: {filepath}")
            checks_passed = False
    
    print("\n[2] Checking directories...")
    required_dirs = [
        ('uploads', 'Uploads directory'),
        ('models', 'Models directory'),
        ('templates', 'Templates directory'),
        ('agents', 'Agents directory'),
    ]
    
    for dirpath, description in required_dirs:
        if os.path.exists(dirpath) and os.path.isdir(dirpath):
            print(f"  ✓ {description} found")
        else:
            print(f"  ✗ {description} NOT FOUND: {dirpath}")
            checks_passed = False
    
    if not checks_passed:
        print("\n" + "=" * 80)
        print("✗ SOME CHECKS FAILED - Please fix the issues above")
        print("=" * 80)
        sys.exit(1)
    
    print("\n" + "=" * 80)
    print("✓ ALL CHECKS PASSED - STARTING APPLICATION")
    print("=" * 80)
    print("\nAccess the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    print("=" * 80 + "\n")

# Run prerequisite checks
check_prerequisites()

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
print("Loading VGG16 model...")
model = load_model('models/model.h5')
print("✓ Model loaded successfully")

# Class labels
class_labels = ['pituitary', 'glioma', 'notumor', 'meningioma']

# Initialize agents
print("Initializing AI agents...")
explainability_agent = ExplainabilityAgent(model, class_labels)
clinical_chat_agent = ClinicalChatAgent()
print("✓ Agents initialized successfully\n")

# Store current explanation globally (for chat context)
current_explanation = None

# Define the uploads folder
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function to predict tumor type with explanation
def predict_tumor_with_explanation(image_path):
    global current_explanation
    
    IMAGE_SIZE = 128
    img = load_img(image_path, target_size=(IMAGE_SIZE, IMAGE_SIZE))
    img_array = img_to_array(img) / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    confidence_score = np.max(predictions, axis=1)[0]

    # Generate explanation using ExplainabilityAgent
    preprocessing_logs = {
        "resize": "128x128",
        "normalization": "pixel values / 255.0",
        "color_space": "RGB",
        "timestamp": datetime.now().isoformat()
    }
    
    metadata = {
        "filename": os.path.basename(image_path),
        "file_path": image_path,
        "upload_time": datetime.now().isoformat()
    }
    
    # Generate comprehensive explanation
    explanation = explainability_agent.generate_explanation(
        image_path=image_path,
        img_array=img_array,
        predictions=predictions,
        preprocessing_logs=preprocessing_logs,
        metadata=metadata
    )
    
    # Store explanation for chat agent
    current_explanation = explanation
    clinical_chat_agent.load_explanation(explanation)

    if class_labels[predicted_class_index] == 'notumor':
        result = "No Tumor"
    else:
        result = f"Tumor: {class_labels[predicted_class_index]}"
    
    return result, confidence_score, explanation

# Route for the main page (index.html)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        file = request.files['file']
        if file:
            # Save the file
            file_location = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_location)

            # Predict the tumor with explanation
            result, confidence, explanation = predict_tumor_with_explanation(file_location)

            # Return result along with image path and explanation summary for display
            return render_template(
                'index.html', 
                result=result, 
                confidence=f"{confidence*100:.2f}%", 
                file_path=f'/uploads/{file.filename}',
                has_explanation=True,
                explanation_summary={
                    'predicted_class': explanation['decision_explanation']['predicted_class'],
                    'confidence_level': explanation['decision_explanation']['confidence_level'],
                    'reasoning': explanation['decision_explanation']['reasoning'],
                    'uncertainty_level': explanation['uncertainty_analysis']['uncertainty_level']
                }
            )

    return render_template('index.html', result=None, has_explanation=False)

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# API endpoint for getting full explanation JSON
@app.route('/api/explain', methods=['GET'])
def get_explanation():
    """
    Returns the full explanation JSON for the last prediction
    """
    global current_explanation
    
    if current_explanation is None:
        return jsonify({
            "error": "No prediction available. Please upload an image first.",
            "status": "no_data"
        }), 404
    
    return jsonify(current_explanation), 200

# API endpoint for clinical chat
@app.route('/api/chat', methods=['POST'])
def clinical_chat():
    """
    Clinical chat endpoint - answers doctor questions based on explanation
    """
    global current_explanation
    
    if current_explanation is None:
        return jsonify({
            "error": "No prediction available. Please upload an image first.",
            "status": "no_data"
        }), 404
    
    data = request.get_json()
    question = data.get('question', '').strip()
    
    if not question:
        return jsonify({
            "error": "No question provided",
            "status": "invalid_input"
        }), 400
    
    # Get answer from clinical chat agent
    response = clinical_chat_agent.answer_question(question)
    
    return jsonify({
        "question": question,
        "response": response,
        "timestamp": datetime.now().isoformat()
    }), 200

# Route to get conversation history
@app.route('/api/chat/history', methods=['GET'])
def get_chat_history():
    """
    Get conversation history
    """
    summary = clinical_chat_agent.get_conversation_summary()
    return jsonify(summary), 200

# Route to clear conversation
@app.route('/api/chat/clear', methods=['POST'])
def clear_chat():
    """
    Clear conversation history
    """
    clinical_chat_agent.clear_conversation()
    return jsonify({
        "status": "success",
        "message": "Conversation history cleared"
    }), 200

if __name__ == '__main__':
    print("\n🧠 Starting Brain Tumor Detection System with AI Agents...")
    print("=" * 80)
    app.run(debug=True, host='0.0.0.0', port=5000)
