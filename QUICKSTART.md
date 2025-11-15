# Quick Start Guide - AI Agents for Brain Tumor Detection

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Verify Directory Structure**
   ```
   btd/
   ├── agents/
   │   ├── __init__.py
   │   ├── explainability_agent.py
   │   └── clinical_chat_agent.py
   ├── models/
   │   └── model.h5
   ├── templates/
   │   └── index.html
   ├── uploads/
   ├── main.py
   └── requirements.txt
   ```

3. **Run Test (Optional)**
   ```powershell
   python test_agents.py
   ```

4. **Start the Application**
   ```powershell
   python main.py
   ```

5. **Open in Browser**
   Navigate to: `http://localhost:5000`

## 🎯 Features Overview

### 1. **Explainability Agent** ✨
Automatically generates comprehensive explanations including:
- ✅ Step-by-step pipeline summary
- ✅ Decision reasoning
- ✅ Confidence levels and uncertainty analysis
- ✅ Feature contributions (Grad-CAM)
- ✅ All class probabilities
- ✅ Alternative diagnoses
- ✅ Data quality assessment
- ✅ Clinical recommendations

### 2. **Clinical Chat Agent** 💬
Answers doctor questions with:
- ✅ Grounded responses (no hallucination)
- ✅ Clinician-friendly language
- ✅ Source citations
- ✅ Conversation history
- ✅ Quick question buttons

## 📱 Using the Web Interface

### Step 1: Upload MRI Scan
1. Click "Select MRI Image"
2. Choose a brain MRI scan (.jpg, .png, etc.)
3. Click "Analyze with AI"

### Step 2: View Results
After analysis, you'll see:
- **Diagnosis**: Tumor type or "No Tumor"
- **Confidence**: Percentage with visual bar
- **Confidence Level**: High, moderate, or low
- **AI Reasoning**: Why the model made this decision
- **Uncertainty Assessment**: How certain the model is

### Step 3: Explore Explainability
Click on different sections to see:
- Pipeline summary
- Feature contributions
- All class probabilities
- Quality assessment

### Step 4: Use Clinical Chat
Ask questions like:
- "What is the diagnosis?"
- "How confident is the model?"
- "Why did the model make this decision?"
- "What are the recommendations?"
- "Are there alternative diagnoses?"
- "How's the image quality?"

**Quick Question Buttons:**
- What is the diagnosis?
- How confident?
- Why this decision?
- Recommendations?

### Step 5: View Full Explanation
Click "View Full Explanation" or switch to the "Full Explanation" tab to see the complete JSON output with all technical details.

## 🔌 API Endpoints

### 1. GET /api/explain
Get full explanation JSON

**cURL Example:**
```bash
curl http://localhost:5000/api/explain
```

**Response:**
```json
{
  "timestamp": "2025-11-15T10:30:00",
  "decision_explanation": {...},
  "uncertainty_analysis": {...},
  ...
}
```

### 2. POST /api/chat
Ask clinical questions

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is the diagnosis?\"}"
```

**Response:**
```json
{
  "question": "What is the diagnosis?",
  "response": {
    "answer": "The model detected a **glioma** tumor...",
    "sources": ["decision_explanation"],
    "grounded": true,
    "confidence": "high"
  },
  "timestamp": "..."
}
```

### 3. GET /api/chat/history
Get conversation history

### 4. POST /api/chat/clear
Clear conversation

## 💡 Example Questions for Clinical Chat

### Diagnosis Questions
- "What is the diagnosis?"
- "Is there a tumor?"
- "What type of tumor was detected?"

### Confidence & Uncertainty
- "How confident is this prediction?"
- "How sure are you?"
- "What's the uncertainty level?"
- "How reliable is this result?"

### Reasoning & Explanation
- "Why did the model make this decision?"
- "How does the AI work?"
- "What features contributed to this?"
- "Which regions are most important?"

### Alternative Diagnoses
- "What are the differential diagnoses?"
- "What else could this be?"
- "Are there alternative possibilities?"

### Clinical Recommendations
- "What should I do next?"
- "What are your recommendations?"
- "What actions are recommended?"

### Quality & Technical
- "Is the image quality good?"
- "Any issues with the scan?"
- "Are there quality concerns?"

### Tumor Information
- "Tell me about glioma"
- "What is meningioma?"
- "Explain pituitary tumors"

## 🎨 Frontend Features

### Beautiful UI Elements
- **Gradient backgrounds** for modern look
- **Animated chat messages** slide in smoothly
- **Confidence bars** with gradient fills
- **Color-coded badges** for tumor types
- **Quick question buttons** for common queries
- **Tabbed interface** for organization

### Responsive Design
- Works on desktop and tablet
- Clean card-based layout
- Professional medical interface theme

## 🧪 Testing the Agents

### Automated Test
```powershell
python test_agents.py
```

This will:
1. Load the model
2. Create mock predictions
3. Test ExplainabilityAgent
4. Test ClinicalChatAgent
5. Verify no-hallucination behavior
6. Export test explanation to JSON

### Manual Testing Checklist

- [ ] Upload an MRI scan
- [ ] Verify diagnosis appears correctly
- [ ] Check confidence level makes sense
- [ ] Ask "What is the diagnosis?" in chat
- [ ] Ask "How confident is the model?"
- [ ] Ask "Why did the model decide this?"
- [ ] Ask "What are the recommendations?"
- [ ] Try a question with unavailable info (e.g., "What is the patient's age?")
- [ ] Verify chat says "not available" for missing info
- [ ] View full explanation JSON
- [ ] Check conversation history

## 🔧 Troubleshooting

### Problem: "Module not found" errors
**Solution:** Install dependencies
```powershell
pip install -r requirements.txt
```

### Problem: "No module named 'agents'"
**Solution:** Make sure you're running from the btd directory
```powershell
cd "c:\Users\aksha\Downloads\btd"
python main.py
```

### Problem: Model file not found
**Solution:** Ensure model.h5 is in the models/ directory

### Problem: Chat returns "No prediction available"
**Solution:** Upload an MRI scan first to generate an explanation

### Problem: Port 5000 already in use
**Solution:** Stop other Flask apps or change port in main.py:
```python
app.run(debug=True, port=5001)
```

### Problem: Grad-CAM not available
**Solution:** This is normal for some models. Other explanations will still work.

## 📊 Understanding the Output

### Confidence Levels
- **Very High (>90%)**: Strong prediction, low ambiguity
- **High (70-90%)**: Confident prediction
- **Moderate (50-70%)**: Some uncertainty
- **Low (<50%)**: Highly uncertain, needs review

### Uncertainty Metrics
- **Entropy**: Lower = more confident (0 to ~1.4)
- **Margin**: Higher = more confident (0 to 1)

### Grounding Status
- **Grounded: Yes** = Answer based on actual model output
- **Grounded: No** = Information not available in explanation

## 🔐 Important Notes

1. **AI-Assisted Tool**: This is not a replacement for professional medical diagnosis
2. **Always Review**: All findings should be reviewed by qualified radiologists
3. **No Hallucination**: Agents never invent information - they say "not available"
4. **Privacy**: No data is stored beyond the session
5. **Local Processing**: Everything runs on your machine

## 📈 Performance

- **Inference Time**: ~0.5-1.0 seconds
- **Explanation Generation**: ~0.5-1.0 seconds
- **Chat Response**: <100ms
- **Total Analysis**: ~1-2 seconds

## 🎓 Learning Resources

- See `AGENTS_README.md` for detailed technical documentation
- Review `test_agents.py` for code examples
- Check the agents source code for implementation details

## 🆘 Support

If you encounter issues:
1. Check this guide's troubleshooting section
2. Review AGENTS_README.md for technical details
3. Check the Flask console for error messages
4. Verify all files are in correct locations

## ✅ Success Checklist

Before deployment, verify:
- [ ] All dependencies installed
- [ ] Model loads without errors
- [ ] Web interface accessible at localhost:5000
- [ ] Can upload and analyze an image
- [ ] Results display correctly
- [ ] Chat responds to questions
- [ ] Full explanation JSON loads
- [ ] No hallucination (tested with unavailable info)
- [ ] API endpoints working

---

## 🎉 You're Ready!

Your AI-powered brain tumor detection system with integrated explainability and clinical chat agents is now fully operational!

**Start the app:**
```powershell
python main.py
```

**Then visit:**
```
http://localhost:5000
```

Happy analyzing! 🧠✨
