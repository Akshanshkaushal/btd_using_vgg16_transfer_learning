# AI Agents Integration - Brain Tumor Detection System

## Overview

This document describes the two AI agents integrated into the brain tumor detection system:

1. **Explainability Agent** - Generates comprehensive, grounded explanations of model predictions
2. **Clinical Chat Agent** - Provides clinician-friendly Q&A based strictly on explanation data

## Architecture

```
User uploads MRI scan
        ↓
Flask Backend (main.py)
        ↓
VGG16 Model Inference
        ↓
ExplainabilityAgent.generate_explanation()
        ↓
Stores explanation JSON + loads into ClinicalChatAgent
        ↓
Frontend displays results + enables chat
```

## 1. Explainability Agent

### Purpose
Takes model outputs and generates structured JSON explanations containing:
- Step-by-step pipeline summary
- Decision reasoning
- Feature contributions (Grad-CAM)
- All class probabilities
- Alternative diagnoses
- Uncertainty analysis
- Data quality assessment
- Clinical recommendations

### Key Features
- **No Hallucination**: Returns "not available" for missing data
- **Comprehensive**: Covers all aspects of the prediction
- **Grounded**: All information derived from actual model outputs
- **Clinical Context**: Includes tumor type explanations and recommendations

### Usage

```python
from agents.explainability_agent import ExplainabilityAgent

# Initialize
agent = ExplainabilityAgent(model, class_labels)

# Generate explanation
explanation = agent.generate_explanation(
    image_path="path/to/mri.jpg",
    img_array=preprocessed_array,
    predictions=model_predictions,
    preprocessing_logs=logs,
    metadata=metadata
)

# Export to JSON
agent.export_to_json(explanation, "explanation.json")
```

### Explanation Structure

```json
{
  "timestamp": "ISO-8601 datetime",
  "image_path": "path/to/image",
  "pipeline_summary": {
    "step_1_input": {...},
    "step_2_preprocessing": {...},
    "step_3_model_inference": {...},
    "step_4_postprocessing": {...}
  },
  "decision_explanation": {
    "predicted_class": "glioma",
    "confidence": 92.5,
    "confidence_level": "very high",
    "reasoning": "Model detected distinct glioma characteristics...",
    "is_tumor": true
  },
  "feature_contributions": {
    "grad_cam_available": true,
    "top_contributing_regions": "...",
    "visual_features": {...}
  },
  "all_predictions": {
    "glioma": {"probability": 92.5, "rank": 1},
    "meningioma": {"probability": 5.2, "rank": 2},
    ...
  },
  "alternative_classes": [...],
  "uncertainty_analysis": {
    "entropy": 0.234,
    "margin": 0.873,
    "uncertainty_level": "low uncertainty - confident prediction"
  },
  "data_quality": {...},
  "clinical_context": {...}
}
```

## 2. Clinical Chat Agent

### Purpose
Answers doctor questions using ONLY the explanation JSON + evidence. Converts technical details into clinician-friendly language.

### Key Features
- **Strictly Grounded**: Only uses data from explanation JSON
- **No Invention**: Says "not in model output" when info is missing
- **Context-Aware**: Routes questions to appropriate handlers
- **Conversational**: Maintains chat history

### Usage

```python
from agents.clinical_chat_agent import ClinicalChatAgent

# Initialize
chat_agent = ClinicalChatAgent()

# Load explanation
chat_agent.load_explanation(explanation_json)

# Ask questions
response = chat_agent.answer_question("What is the diagnosis?")
print(response['answer'])

# Get conversation history
history = chat_agent.get_conversation_summary()
```

### Supported Question Types

1. **Diagnosis Questions**
   - "What is the diagnosis?"
   - "What did the model detect?"
   - "Is there a tumor?"

2. **Confidence Questions**
   - "How confident is the model?"
   - "How sure are you?"
   - "What's the reliability?"

3. **Reasoning Questions**
   - "Why did the model make this decision?"
   - "How does it work?"
   - "Explain the reasoning"

4. **Location Questions**
   - "Where is the tumor located?"
   - "Which regions are affected?"
   - "What areas contributed most?"

5. **Alternative Diagnosis**
   - "What are the alternative diagnoses?"
   - "What else could it be?"
   - "Differential diagnosis?"

6. **Quality Assessment**
   - "Is the image quality good?"
   - "Any quality issues?"
   - "How's the scan quality?"

7. **Clinical Recommendations**
   - "What should I do next?"
   - "What are the recommendations?"
   - "Next steps?"

8. **Uncertainty**
   - "How uncertain is the prediction?"
   - "Is it ambiguous?"
   - "Any doubts?"

### Response Format

```json
{
  "answer": "Formatted markdown-style answer",
  "sources": ["decision_explanation", "uncertainty_analysis"],
  "grounded": true,
  "confidence": "high",
  "additional_metadata": {...}
}
```

## API Endpoints

### 1. GET /api/explain
Returns the full explanation JSON for the last prediction.

**Response:**
```json
{
  "timestamp": "...",
  "decision_explanation": {...},
  "uncertainty_analysis": {...},
  ...
}
```

### 2. POST /api/chat
Processes a clinical question and returns grounded answer.

**Request:**
```json
{
  "question": "What is the diagnosis?"
}
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
Returns conversation history.

### 4. POST /api/chat/clear
Clears conversation history.

## Frontend Integration

### Upload & Analysis
1. User uploads MRI scan via form
2. Flask processes and runs model inference
3. ExplainabilityAgent generates comprehensive explanation
4. Results displayed with summary cards

### Clinical Chat Interface
- Real-time question answering
- Quick question buttons for common queries
- Message history with formatted responses
- Markdown rendering for structured answers

### Full Explanation View
- JSON tree view of complete explanation
- Downloadable for record-keeping
- All technical details accessible

## File Structure

```
btd/
├── agents/
│   ├── __init__.py
│   ├── explainability_agent.py    # Explanation generation
│   └── clinical_chat_agent.py     # Question answering
├── main.py                        # Flask app with API endpoints
├── templates/
│   └── index.html                 # Enhanced UI with chat
├── models/
│   └── model.h5                   # Trained VGG16 model
└── uploads/                       # User uploads
```

## Key Design Principles

### 1. No Hallucination
Both agents are designed to NEVER invent information:
- ExplainabilityAgent returns "not available" for missing data
- ClinicalChatAgent says "not in model output" when info isn't present
- All answers grounded in actual model outputs

### 2. Modular Design
- Agents are separate modules, easily maintainable
- Clean API boundaries
- Can be extended independently

### 3. Clinical Focus
- Language tailored for medical professionals
- Includes clinical context and recommendations
- Uncertainty communicated clearly

### 4. Explainable AI
- Grad-CAM visualization for spatial understanding
- Entropy and margin metrics for uncertainty
- All class probabilities for differential diagnosis

## Example Interactions

### Example 1: Basic Diagnosis Query
**Question:** "What is the diagnosis?"

**Response:**
```
The model detected a **glioma** tumor with 92.5% confidence.

Clinical Interpretation: Model detected distinct glioma characteristics 
with very high confidence based on learned tissue patterns.

Data Sources: decision_explanation
Grounded in Evidence: Yes
```

### Example 2: Confidence Query
**Question:** "How confident is the model?"

**Response:**
```
Confidence Score: 92.5%
Confidence Level: very high
Uncertainty Assessment: low uncertainty - confident prediction

Interpretation: Very confident prediction with clear distinction 
from other classes.

Technical Metrics:
- Prediction Entropy: 0.234 (lower is more confident)
- Margin (top 2 classes): 0.873 (higher is more confident)
```

### Example 3: Missing Information
**Question:** "What was the patient's age?"

**Response:**
```
This information is not available in the model output.

Context: patient demographic information

The clinical chat agent can only provide information that was 
generated during the model's prediction and explanation process.
This specific information was not included in the analysis.

Information not in model output - agent forbidden to hallucinate
```

## Testing

### Test the Agents
```python
# Test script included in test_agents.py
python test_agents.py
```

### Manual Testing
1. Start the Flask app: `python main.py`
2. Navigate to `http://localhost:5000`
3. Upload an MRI scan
4. View results and explanation
5. Ask questions in the chat interface
6. Check API endpoints directly:
   - `http://localhost:5000/api/explain`
   - POST to `http://localhost:5000/api/chat`

## Future Enhancements

1. **Enhanced Visualizations**
   - SHAP value integration
   - Counterfactual explanations
   - Attention maps overlay

2. **Multi-Model Ensemble**
   - Support for ensemble predictions
   - Disagreement analysis
   - Confidence calibration

3. **Advanced Chat Features**
   - Voice input/output
   - Context-aware follow-up questions
   - Multi-turn conversation understanding

4. **Clinical Integration**
   - DICOM support
   - PACS integration
   - Report generation

## Troubleshooting

### Issue: "No prediction available"
**Solution:** Upload an MRI scan first before using chat or viewing explanation.

### Issue: Grad-CAM not available
**Solution:** This is normal for some model architectures. The agent will note this and provide other explanations.

### Issue: Chat response seems generic
**Solution:** Ask more specific questions. The agent routes questions based on keywords.

## Security Considerations

1. **Input Validation**: All user inputs sanitized
2. **File Upload**: Only image files accepted
3. **API Rate Limiting**: Consider adding in production
4. **Data Privacy**: No patient data stored in explanations unless explicitly provided

## Performance Notes

- Explanation generation: ~0.5-1.0 seconds
- Chat responses: <100ms
- Grad-CAM computation: ~0.3-0.5 seconds
- Total inference + explanation: ~1-2 seconds

## License & Disclaimer

This is an AI-assisted diagnostic tool. All findings should be reviewed by a qualified radiologist or clinician before making clinical decisions.

---

**Version:** 1.0  
**Last Updated:** November 15, 2025  
**Authors:** AI Integration Team
