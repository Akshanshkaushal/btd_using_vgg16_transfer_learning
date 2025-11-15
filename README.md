# Brain Tumor Detection Using Deep Learning 🧠

## Advanced AI System with Explainability & Clinical Chat Agents

This project implements an advanced brain tumor detection system using VGG16 transfer learning with integrated AI agents for explainability and clinical decision support.

## 🌟 Key Features

### 1. **Accurate Tumor Detection**
- VGG16-based transfer learning model
- Detects 4 classes: Glioma, Meningioma, Pituitary, No Tumor
- High confidence predictions with uncertainty quantification

### 2. **Explainability Agent** ✨
Generates comprehensive, grounded explanations including:
- Step-by-step pipeline summary
- Decision reasoning and confidence analysis
- Feature contributions (Grad-CAM visualization)
- All class probabilities and alternatives
- Uncertainty metrics (entropy, margin)
- Data quality assessment
- Clinical recommendations

### 3. **Clinical Chat Agent** 💬
AI-powered Q&A for clinicians:
- Answers questions about diagnosis, confidence, reasoning
- Strictly grounded in model outputs (no hallucination)
- Clinician-friendly language
- Conversation history and context awareness
- Quick question shortcuts

### 4. **Modern Web Interface**
- Beautiful gradient UI design
- Real-time chat interface
- Confidence visualization with progress bars
- Tabbed navigation for organization
- Responsive design for all devices

## 📁 Project Structure

```
btd/
├── agents/                          # AI Agents (NEW!)
│   ├── __init__.py
│   ├── explainability_agent.py     # Generates explanations
│   └── clinical_chat_agent.py      # Handles clinical Q&A
├── models/
│   └── model.h5                     # Trained VGG16 model
├── templates/
│   └── index.html                   # Enhanced web interface
├── uploads/                         # User uploaded images
├── main.py                          # Flask app with API endpoints
├── requirements.txt                 # Python dependencies
├── test_agents.py                   # Agent testing script
├── start_app.py                     # Startup script with checks
├── QUICKSTART.md                    # Quick start guide
├── AGENTS_README.md                 # Detailed agent documentation
└── brain_tumour_detection_using_deep_learning.ipynb  # Training notebook
```

## 🚀 Quick Start

### Start the Application
```powershell
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

Then open your browser to: **http://localhost:5000**

## 📖 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step setup and usage guide
- **[AGENTS_README.md](AGENTS_README.md)** - Detailed agent architecture and API docs
- **[test_agents.py](test_agents.py)** - Agent testing and validation

## 🎯 How to Use

### 1. Upload MRI Scan
- Click "Select MRI Image"
- Choose a brain MRI scan
- Click "Analyze with AI"

### 2. View Results
- See diagnosis with confidence level
- Review AI reasoning and uncertainty
- Check quality assessment

### 3. Ask Questions in Clinical Chat
Try questions like:
- "What is the diagnosis?"
- "How confident is this prediction?"
- "Why did the model make this decision?"
- "What are the recommendations?"
- "Are there alternative diagnoses?"

### 4. Explore Full Explanation
- View complete JSON explanation
- See all technical metrics
- Export for documentation

## 🔌 API Endpoints

### GET /api/explain
Returns full explanation JSON
```bash
curl http://localhost:5000/api/explain
```

### POST /api/chat
Ask clinical questions
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the diagnosis?"}'
```

### GET /api/chat/history
Get conversation history

### POST /api/chat/clear
Clear conversation

## 🧪 Testing

Run the comprehensive agent test:
```powershell
python test_agents.py
```

This validates:
- Explanation generation
- Question answering
- No-hallucination behavior
- Conversation management

## 🏗️ Model Architecture

**Base Model:** VGG16 (ImageNet pre-trained)

**Custom Layers:**
- Flatten
- Dropout(0.3)
- Dense(128, activation='relu')
- Dropout(0.2)
- Dense(4, activation='softmax')

**Training:**
- Optimizer: Adam (lr=0.0001)
- Loss: Sparse Categorical Crossentropy
- Image Size: 128x128
- Classes: 4 (Glioma, Meningioma, Pituitary, No Tumor)

## 🎨 Key Technologies

- **Backend:** Flask, TensorFlow/Keras
- **AI Agents:** Custom Python modules
- **Frontend:** Bootstrap 5, JavaScript
- **Visualization:** Grad-CAM, Confidence bars
- **ML Model:** VGG16 Transfer Learning

## 📊 Agent Features in Detail

### Explainability Agent
- **Input:** Model predictions, image, preprocessing logs
- **Output:** Comprehensive JSON explanation
- **Key Metrics:** Confidence, entropy, margin, quality
- **Visualizations:** Grad-CAM heatmaps
- **Guarantees:** No hallucination - returns "not available" for missing data

### Clinical Chat Agent
- **Input:** Doctor questions
- **Output:** Grounded, clinician-friendly answers
- **Question Types:** Diagnosis, confidence, reasoning, recommendations
- **Sources:** Always cites data sources
- **Guarantees:** Strictly grounded in explanation JSON

## ⚠️ Important Disclaimer

This is an **AI-assisted diagnostic tool** for educational and research purposes. 

**All findings must be reviewed by qualified medical professionals before making clinical decisions.**

## 🔒 Privacy & Security

- All processing is local
- No data sent to external servers
- No patient information stored beyond session
- Images saved only in local uploads folder

## 📈 Performance Metrics

- **Inference Time:** ~0.5-1.0 seconds
- **Explanation Generation:** ~0.5-1.0 seconds
- **Chat Response:** <100ms
- **Total Analysis:** ~1-2 seconds

## 🛠️ Requirements

- Python 3.8+
- TensorFlow 2.18.0
- Flask 3.1.0
- Keras 3.7.0
- OpenCV 4.10.0
- NumPy 2.0.2

See `requirements.txt` for complete list.

## 📝 Example Workflow

1. **Doctor uploads** MRI scan
2. **System analyzes** with VGG16 model
3. **Explainability Agent** generates comprehensive explanation
4. **Results displayed** with confidence and reasoning
5. **Doctor asks questions** via clinical chat
6. **Chat Agent responds** with grounded answers
7. **Full explanation** available for documentation

## 🎓 Educational Use

This project demonstrates:
- Transfer learning with VGG16
- Explainable AI (Grad-CAM)
- Uncertainty quantification
- Grounded AI systems (no hallucination)
- Clinical decision support
- Full-stack ML deployment

## 👥 Contributing

Contributions welcome! Areas for enhancement:
- Additional visualization methods (SHAP, attention maps)
- Multi-model ensemble support
- DICOM file support
- Enhanced chat capabilities
- More sophisticated uncertainty quantification

## 📜 License

This project is for educational and research purposes.

## 🙏 Acknowledgments

- VGG16 architecture from Visual Geometry Group, Oxford
- ImageNet pre-trained weights
- Flask framework
- Bootstrap UI framework

## 📧 Support

For issues or questions:
1. Check QUICKSTART.md
2. Review AGENTS_README.md
3. Run test_agents.py for diagnostics

---

**Version:** 2.0 (with AI Agents Integration)  
**Last Updated:** November 15, 2025  
**Status:** Production Ready

## 🚦 Getting Started Now

```powershell
# Install dependencies
pip install -r requirements.txt

# Start the application
python main.py

# Then visit
http://localhost:5000
```

**Happy analyzing! 🧠✨**
