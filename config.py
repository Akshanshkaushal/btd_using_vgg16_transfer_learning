"""
Configuration file for Brain Tumor Detection System
Modify these settings to customize the application behavior
"""

# Application Settings
APP_CONFIG = {
    "debug": True,
    "host": "0.0.0.0",
    "port": 5000,
}

# Model Settings
MODEL_CONFIG = {
    "model_path": "models/model.h5",
    "image_size": 128,
    "class_labels": ['pituitary', 'glioma', 'notumor', 'meningioma'],
}

# Explainability Agent Settings
EXPLAINABILITY_CONFIG = {
    "confidence_threshold": 0.7,  # Threshold for high confidence
    "generate_grad_cam": True,    # Enable/disable Grad-CAM generation
    "include_pipeline_summary": True,
    "include_uncertainty_analysis": True,
    "include_quality_assessment": True,
    "include_clinical_context": True,
    "export_explanations": False,  # Auto-export to JSON files
    "export_directory": "explanations/",
}

# Clinical Chat Agent Settings
CHAT_CONFIG = {
    "max_conversation_history": 50,  # Maximum questions to store
    "enable_quick_questions": True,
    "default_response_format": "markdown",  # 'markdown' or 'plain'
}

# Upload Settings
UPLOAD_CONFIG = {
    "upload_folder": "./uploads",
    "max_file_size": 16 * 1024 * 1024,  # 16MB
    "allowed_extensions": {'.jpg', '.jpeg', '.png', '.gif', '.bmp'},
}

# UI Settings
UI_CONFIG = {
    "show_confidence_bar": True,
    "show_quick_questions": True,
    "show_full_explanation_tab": True,
    "animation_enabled": True,
    "quick_questions": [
        "What is the diagnosis?",
        "How confident is the model?",
        "Why did the model make this decision?",
        "What are the recommendations?"
    ]
}

# API Settings
API_CONFIG = {
    "enable_cors": False,  # Enable if frontend is on different domain
    "rate_limiting": False,  # Enable rate limiting for production
    "requests_per_minute": 60,
}

# Logging Settings
LOGGING_CONFIG = {
    "log_predictions": True,
    "log_explanations": True,
    "log_chat_conversations": True,
    "log_file": "app.log",
    "log_level": "INFO",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
}

# Security Settings
SECURITY_CONFIG = {
    "sanitize_filenames": True,
    "validate_file_type": True,
    "max_concurrent_uploads": 5,
}

# Advanced Settings
ADVANCED_CONFIG = {
    "cache_explanations": True,  # Cache explanations to avoid regeneration
    "cache_timeout": 3600,  # Cache timeout in seconds (1 hour)
    "async_processing": False,  # Enable async for large batches
}

# Clinical Recommendations Templates
CLINICAL_RECOMMENDATIONS = {
    "high_confidence_tumor": (
        "{tumor_type} tumor detected with high confidence. "
        "Recommend immediate specialist consultation and treatment planning."
    ),
    "moderate_confidence_tumor": (
        "{tumor_type} tumor indicated. Recommend specialist review and "
        "potentially additional imaging for confirmation."
    ),
    "low_confidence_tumor": (
        "Possible {tumor_type} tumor but with lower confidence. "
        "Recommend expert radiologist review and additional diagnostic procedures."
    ),
    "high_confidence_no_tumor": (
        "No tumor detected with high confidence. Routine follow-up recommended."
    ),
    "moderate_confidence_no_tumor": (
        "No tumor indicated but with moderate confidence. "
        "Consider additional imaging if symptoms persist."
    ),
}

# Tumor Type Information
TUMOR_TYPES_INFO = {
    "glioma": {
        "description": "Most common malignant brain tumor, arises from glial cells",
        "severity": "high",
        "common_treatment": "Surgery, radiation, chemotherapy",
        "prognosis": "Variable depending on grade"
    },
    "meningioma": {
        "description": "Usually benign tumor arising from meninges",
        "severity": "low to moderate",
        "common_treatment": "Observation or surgery",
        "prognosis": "Generally good for benign cases"
    },
    "pituitary": {
        "description": "Tumor in pituitary gland, often benign but can affect hormones",
        "severity": "moderate",
        "common_treatment": "Medication or surgery",
        "prognosis": "Good with appropriate treatment"
    },
    "notumor": {
        "description": "No tumor detected in the scan",
        "severity": "none",
        "common_treatment": "None required",
        "prognosis": "Excellent"
    }
}

# Confidence Level Thresholds
CONFIDENCE_THRESHOLDS = {
    "very_high": 0.90,
    "high": 0.70,
    "moderate": 0.50,
    "low": 0.0
}

# Uncertainty Thresholds
UNCERTAINTY_THRESHOLDS = {
    "entropy_low": 0.5,
    "entropy_moderate": 1.0,
    "margin_high": 0.5,
    "margin_moderate": 0.3
}

# Grad-CAM Settings
GRADCAM_CONFIG = {
    "enabled": True,
    "save_heatmaps": False,
    "heatmap_directory": "gradcam_outputs/",
    "colormap": "jet",  # OpenCV colormap
}

# Export Settings
EXPORT_CONFIG = {
    "enable_json_download": True,
    "enable_pdf_report": False,  # Future feature
    "include_visualizations": True,
}

def get_config():
    """Return all configuration as a single dictionary"""
    return {
        "app": APP_CONFIG,
        "model": MODEL_CONFIG,
        "explainability": EXPLAINABILITY_CONFIG,
        "chat": CHAT_CONFIG,
        "upload": UPLOAD_CONFIG,
        "ui": UI_CONFIG,
        "api": API_CONFIG,
        "logging": LOGGING_CONFIG,
        "security": SECURITY_CONFIG,
        "advanced": ADVANCED_CONFIG,
        "clinical_recommendations": CLINICAL_RECOMMENDATIONS,
        "tumor_types": TUMOR_TYPES_INFO,
        "confidence_thresholds": CONFIDENCE_THRESHOLDS,
        "uncertainty_thresholds": UNCERTAINTY_THRESHOLDS,
        "gradcam": GRADCAM_CONFIG,
        "export": EXPORT_CONFIG,
    }

def print_config():
    """Print all configuration settings"""
    import json
    config = get_config()
    print(json.dumps(config, indent=2))

if __name__ == "__main__":
    print_config()
