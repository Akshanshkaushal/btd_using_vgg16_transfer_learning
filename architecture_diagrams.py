"""
Architecture Diagram for Brain Tumor Detection System with AI Agents

This file provides ASCII art diagrams to visualize the system architecture
"""

SYSTEM_ARCHITECTURE = """
================================================================================
                    BRAIN TUMOR DETECTION SYSTEM ARCHITECTURE
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (Browser)                             │
│                           templates/index.html                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐            │
│  │  Upload Card    │  │  Results Card   │  │  Chat Interface │            │
│  │  - File Select  │  │  - Diagnosis    │  │  - Questions    │            │
│  │  - Analyze Btn  │  │  - Confidence   │  │  - Answers      │            │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘            │
│           │                     │                     │                     │
└───────────┼─────────────────────┼─────────────────────┼─────────────────────┘
            │                     │                     │
            │                     │                     │
            ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FLASK BACKEND (main.py)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                          API ENDPOINTS                               │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │  POST /                - Upload & Predict                           │  │
│  │  GET  /api/explain     - Get Full Explanation JSON                  │  │
│  │  POST /api/chat        - Ask Clinical Question                      │  │
│  │  GET  /api/chat/history - Get Conversation History                  │  │
│  │  POST /api/chat/clear  - Clear Conversation                         │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │              predict_tumor_with_explanation()                        │  │
│  │  1. Load & preprocess image                                         │  │
│  │  2. Run VGG16 model inference                                       │  │
│  │  3. Generate explanation ──────────────────────────┐                │  │
│  │  4. Store & load into chat agent                  │                │  │
│  └────────────────────────────────────────────────────┼────────────────┘  │
│                                                        │                   │
└────────────────────────────────────────────────────────┼───────────────────┘
                                                         │
                    ┌────────────────────────────────────┼────────────────┐
                    │                                    ▼                │
                    │        ┌────────────────────────────────────────┐  │
                    │        │    EXPLAINABILITY AGENT                │  │
                    │        │    agents/explainability_agent.py      │  │
                    │        ├────────────────────────────────────────┤  │
                    │        │  generate_explanation()                │  │
                    │        │   ├─ Pipeline Summary (4 steps)        │  │
                    │        │   ├─ Decision Explanation              │  │
                    │        │   ├─ Confidence Analysis               │  │
                    │        │   ├─ Grad-CAM Generation               │  │
                    │        │   ├─ All Predictions                   │  │
                    │        │   ├─ Alternative Classes               │  │
                    │        │   ├─ Uncertainty Metrics               │  │
                    │        │   ├─ Quality Assessment                │  │
                    │        │   └─ Clinical Recommendations          │  │
                    │        └────────────────┬───────────────────────┘  │
                    │                         │                          │
                    │                         │ Explanation JSON         │
                    │                         │                          │
                    │                         ▼                          │
                    │        ┌────────────────────────────────────────┐  │
                    │        │    CLINICAL CHAT AGENT                 │  │
                    │        │    agents/clinical_chat_agent.py       │  │
                    │        ├────────────────────────────────────────┤  │
                    │        │  load_explanation()                    │  │
                    │        │  answer_question()                     │  │
                    │        │   ├─ Route to handler                  │  │
                    │        │   ├─ Extract from explanation          │  │
                    │        │   ├─ Format for clinician              │  │
                    │        │   └─ Return grounded answer            │  │
                    │        │                                        │  │
                    │        │  Question Handlers:                    │  │
                    │        │   • Diagnosis                          │  │
                    │        │   • Confidence                         │  │
                    │        │   • Reasoning                          │  │
                    │        │   • Location                           │  │
                    │        │   • Alternatives                       │  │
                    │        │   • Quality                            │  │
                    │        │   • Recommendations                    │  │
                    │        │   • Uncertainty                        │  │
                    │        │   • Tumor Types                        │  │
                    │        └────────────────────────────────────────┘  │
                    │                                                    │
                    └────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          ML MODEL & DEPENDENCIES                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐               │
│  │  VGG16 Model   │  │  TensorFlow    │  │  OpenCV        │               │
│  │  model.h5      │  │  Keras         │  │  Grad-CAM      │               │
│  └────────────────┘  └────────────────┘  └────────────────┘               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
"""

DATA_FLOW = """
================================================================================
                              DATA FLOW DIAGRAM
================================================================================

USER                    FLASK                 EXPLAINABILITY         CHAT
ACTION                  BACKEND               AGENT                  AGENT
  │                       │                      │                      │
  │  1. Upload MRI        │                      │                      │
  ├──────────────────────>│                      │                      │
  │                       │                      │                      │
  │                       │  2. Load & Preprocess│                      │
  │                       ├──────────┐           │                      │
  │                       │          │           │                      │
  │                       │<─────────┘           │                      │
  │                       │                      │                      │
  │                       │  3. Model Inference  │                      │
  │                       ├──────────┐           │                      │
  │                       │          │           │                      │
  │                       │<─────────┘           │                      │
  │                       │   (predictions)      │                      │
  │                       │                      │                      │
  │                       │  4. Generate         │                      │
  │                       │     Explanation      │                      │
  │                       ├─────────────────────>│                      │
  │                       │                      │                      │
  │                       │                      │ • Pipeline summary   │
  │                       │                      │ • Decision reasoning │
  │                       │                      │ • Grad-CAM          │
  │                       │                      │ • Uncertainty       │
  │                       │                      │ • Quality           │
  │                       │                      │                      │
  │                       │  5. Explanation JSON │                      │
  │                       │<─────────────────────┤                      │
  │                       │                      │                      │
  │                       │  6. Load Explanation │                      │
  │                       ├──────────────────────┼─────────────────────>│
  │                       │                      │                      │
  │  7. Display Results   │                      │                      │
  │<──────────────────────┤                      │                      │
  │   • Diagnosis         │                      │                      │
  │   • Confidence        │                      │                      │
  │   • Reasoning         │                      │                      │
  │                       │                      │                      │
  │  8. Ask Question      │                      │                      │
  ├──────────────────────>│                      │                      │
  │   "What is the        │  9. Forward Question │                      │
  │    diagnosis?"        ├──────────────────────┼─────────────────────>│
  │                       │                      │                      │
  │                       │                      │   10. Process:       │
  │                       │                      │   • Route question   │
  │                       │                      │   • Extract from     │
  │                       │                      │     explanation      │
  │                       │                      │   • Format answer    │
  │                       │                      │   • Cite sources     │
  │                       │                      │                      │
  │                       │  11. Grounded Answer │                      │
  │                       │<─────────────────────┼──────────────────────┤
  │  12. Display Answer   │                      │                      │
  │<──────────────────────┤                      │                      │
  │   • Answer text       │                      │                      │
  │   • Sources           │                      │                      │
  │   • Grounded status   │                      │                      │
  │                       │                      │                      │

"""

EXPLANATION_STRUCTURE = """
================================================================================
                        EXPLANATION JSON STRUCTURE
================================================================================

{
  "timestamp": "2025-11-15T10:30:00",
  
  "pipeline_summary": {
    "step_1_input": {
      "description": "MRI image loaded and validated",
      "status": "completed",
      "details": {...}
    },
    "step_2_preprocessing": {
      "description": "Image resized to 128x128, normalized",
      "status": "completed",
      "details": {"resize": "128x128", "normalization": "0-1"}
    },
    "step_3_model_inference": {
      "description": "VGG16-based transfer learning",
      "status": "completed"
    },
    "step_4_postprocessing": {
      "description": "Softmax probabilities computed",
      "status": "completed"
    }
  },
  
  "decision_explanation": {
    "predicted_class": "glioma",
    "confidence": 85.5,
    "confidence_level": "high",
    "reasoning": "Model identified glioma features...",
    "is_tumor": true
  },
  
  "feature_contributions": {
    "grad_cam_available": true,
    "grad_cam_description": "Heatmap shows regions...",
    "top_contributing_regions": "Central brain regions...",
    "visual_features": {
      "texture_patterns": "detected by VGG16",
      "spatial_structure": "captured by filters",
      "edge_detection": "early layers"
    }
  },
  
  "all_predictions": {
    "glioma":     {"probability": 85.5, "rank": 1},
    "meningioma": {"probability": 8.2,  "rank": 2},
    "pituitary":  {"probability": 4.1,  "rank": 3},
    "notumor":    {"probability": 2.2,  "rank": 4}
  },
  
  "alternative_classes": [
    {
      "class": "meningioma",
      "probability": 8.2,
      "rank": 2,
      "consideration": "low probability alternative"
    }
  ],
  
  "uncertainty_analysis": {
    "entropy": 0.456,
    "margin": 0.773,
    "uncertainty_level": "low uncertainty - confident",
    "interpretation": "Very confident prediction..."
  },
  
  "data_quality": {
    "image_statistics": {
      "mean_intensity": 0.4521,
      "std_intensity": 0.2341
    },
    "quality_issues": [],
    "overall_quality": "acceptable"
  },
  
  "clinical_context": {
    "tumor_types_explanation": {...},
    "recommended_action": "Glioma tumor detected..."
  }
}
"""

CHAT_QUESTION_FLOW = """
================================================================================
                         CHAT QUESTION PROCESSING FLOW
================================================================================

DOCTOR QUESTION
      ▼
┌─────────────────┐
│ Normalize Text  │  (lowercase, trim)
└────────┬────────┘
         ▼
┌─────────────────┐
│  Route Question │
│  Based on       │
│  Keywords       │
└────────┬────────┘
         │
         ├─── "what/diagnosis"  ──> Diagnosis Handler
         │                            ├─ Extract predicted_class
         │                            ├─ Extract confidence
         │                            ├─ Extract reasoning
         │                            └─ Format for display
         │
         ├─── "confident/sure"  ──> Confidence Handler
         │                            ├─ Extract confidence metrics
         │                            ├─ Extract uncertainty analysis
         │                            └─ Include entropy/margin
         │
         ├─── "why/how"         ──> Reasoning Handler
         │                            ├─ Extract decision reasoning
         │                            ├─ Extract feature contributions
         │                            └─ Include Grad-CAM info
         │
         ├─── "region/where"    ──> Location Handler
         │                            ├─ Extract Grad-CAM regions
         │                            └─ Describe contributing areas
         │
         ├─── "alternative"     ──> Alternatives Handler
         │                            ├─ Extract alternative_classes
         │                            └─ Include all_predictions
         │
         ├─── "quality/image"   ──> Quality Handler
         │                            ├─ Extract data_quality
         │                            └─ List quality issues
         │
         ├─── "recommend"       ──> Recommendation Handler
         │                            ├─ Extract recommended_action
         │                            └─ Add clinical context
         │
         ├─── "uncertain"       ──> Uncertainty Handler
         │                            ├─ Extract uncertainty_analysis
         │                            └─ Interpret metrics
         │
         └─── "tumor type"      ──> Tumor Type Handler
                                      ├─ Extract tumor_types_explanation
                                      └─ Compare with prediction
         
         ▼
┌─────────────────┐
│ Format Response │
│  - Answer text  │
│  - Sources      │
│  - Grounded     │
│  - Confidence   │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Return to User  │
└─────────────────┘

GROUNDING CHECK AT EVERY STEP:
  ✓ Data exists in explanation → Use it
  ✗ Data missing             → Return "not available"
"""

if __name__ == "__main__":
    print(SYSTEM_ARCHITECTURE)
    print("\n\n")
    print(DATA_FLOW)
    print("\n\n")
    print(EXPLANATION_STRUCTURE)
    print("\n\n")
    print(CHAT_QUESTION_FLOW)
