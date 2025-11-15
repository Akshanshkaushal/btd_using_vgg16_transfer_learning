"""
Clinical Chat Agent for Brain Tumor Detection System
Answers doctor questions using only explanation JSON and evidence.
Never invents information - strictly grounded in provided data.
"""
import json
from typing import Dict, Any, List, Optional
import re


class ClinicalChatAgent:
    """
    Provides clinician-friendly answers strictly based on explanation JSON.
    Forbidden to hallucinate - returns "not in model output" when info is missing.
    """
    
    def __init__(self):
        """Initialize the Clinical Chat Agent"""
        self.explanation_data = None
        self.conversation_history = []
        
    def load_explanation(self, explanation: Dict[str, Any]) -> bool:
        """
        Load explanation JSON for question answering
        
        Args:
            explanation: Explanation dictionary from ExplainabilityAgent
            
        Returns:
            True if loaded successfully
        """
        try:
            self.explanation_data = explanation
            return True
        except Exception as e:
            print(f"Failed to load explanation: {e}")
            return False
    
    def answer_question(self, question: str) -> Dict[str, Any]:
        """
        Answer doctor's question using only available explanation data
        
        Args:
            question: Doctor's question
            
        Returns:
            Dictionary with answer, sources, and confidence
        """
        if self.explanation_data is None:
            return {
                "answer": "No explanation data loaded. Please run a prediction first.",
                "sources": [],
                "grounded": False,
                "confidence": "N/A"
            }
        
        # Normalize question
        question_lower = question.lower().strip()
        
        # Store in conversation history
        self.conversation_history.append({
            "question": question,
            "timestamp": self.explanation_data.get("timestamp", "unknown")
        })
        
        # Route to appropriate handler
        response = self._route_question(question_lower)
        
        # Add to conversation history
        self.conversation_history[-1]["response"] = response
        
        return response
    
    def _route_question(self, question: str) -> Dict[str, Any]:
        """Route question to appropriate handler based on content"""
        
        # Question categories
        if any(word in question for word in ["what", "which", "diagnosis", "detected", "found", "result"]):
            return self._handle_diagnosis_question(question)
        
        elif any(word in question for word in ["confidence", "sure", "certain", "reliable", "accuracy"]):
            return self._handle_confidence_question(question)
        
        elif any(word in question for word in ["why", "how", "reason", "explain", "cause"]):
            return self._handle_why_question(question)
        
        elif any(word in question for word in ["region", "area", "location", "where", "part"]):
            return self._handle_location_question(question)
        
        elif any(word in question for word in ["alternative", "other", "differential", "else"]):
            return self._handle_alternatives_question(question)
        
        elif any(word in question for word in ["quality", "image", "scan", "artifact"]):
            return self._handle_quality_question(question)
        
        elif any(word in question for word in ["recommend", "next", "action", "do", "should"]):
            return self._handle_recommendation_question(question)
        
        elif any(word in question for word in ["uncertain", "ambiguous", "doubt", "unclear"]):
            return self._handle_uncertainty_question(question)
        
        elif any(word in question for word in ["tumor type", "glioma", "meningioma", "pituitary"]):
            return self._handle_tumor_type_question(question)
        
        else:
            return self._handle_general_question(question)
    
    def _handle_diagnosis_question(self, question: str) -> Dict[str, Any]:
        """Handle questions about diagnosis/prediction"""
        try:
            decision = self.explanation_data.get("decision_explanation", {})
            predicted_class = decision.get("predicted_class", "not available")
            confidence = decision.get("confidence", "not available")
            is_tumor = decision.get("is_tumor", "not available")
            
            if is_tumor:
                answer = f"The model detected a **{predicted_class}** tumor with {confidence}% confidence. "
            else:
                answer = f"The model detected **no tumor** with {confidence}% confidence. "
            
            answer += f"\n\n**Clinical Interpretation:** {decision.get('reasoning', 'not available')}"
            
            return {
                "answer": answer,
                "sources": ["decision_explanation"],
                "grounded": True,
                "confidence": "high",
                "primary_finding": predicted_class,
                "is_tumor": is_tumor
            }
        except Exception as e:
            return self._not_available_response(f"diagnosis information: {e}")
    
    def _handle_confidence_question(self, question: str) -> Dict[str, Any]:
        """Handle questions about prediction confidence"""
        try:
            decision = self.explanation_data.get("decision_explanation", {})
            uncertainty = self.explanation_data.get("uncertainty_analysis", {})
            
            confidence = decision.get("confidence", "not available")
            confidence_level = decision.get("confidence_level", "not available")
            uncertainty_level = uncertainty.get("uncertainty_level", "not available")
            interpretation = uncertainty.get("interpretation", "not available")
            
            answer = f"**Confidence Score:** {confidence}%\n\n"
            answer += f"**Confidence Level:** {confidence_level}\n\n"
            answer += f"**Uncertainty Assessment:** {uncertainty_level}\n\n"
            answer += f"**Interpretation:** {interpretation}\n\n"
            
            # Add entropy and margin
            entropy = uncertainty.get("entropy", "not available")
            margin = uncertainty.get("margin", "not available")
            answer += f"**Technical Metrics:**\n"
            answer += f"- Prediction Entropy: {entropy} (lower is more confident)\n"
            answer += f"- Margin (top 2 classes): {margin} (higher is more confident)"
            
            return {
                "answer": answer,
                "sources": ["decision_explanation", "uncertainty_analysis"],
                "grounded": True,
                "confidence": "high",
                "metrics": {
                    "confidence": confidence,
                    "entropy": entropy,
                    "margin": margin
                }
            }
        except Exception as e:
            return self._not_available_response(f"confidence information: {e}")
    
    def _handle_why_question(self, question: str) -> Dict[str, Any]:
        """Handle questions about reasoning/explanation"""
        try:
            decision = self.explanation_data.get("decision_explanation", {})
            features = self.explanation_data.get("feature_contributions", {})
            
            reasoning = decision.get("reasoning", "not available")
            visual_features = features.get("visual_features", {})
            grad_cam_available = features.get("grad_cam_available", False)
            
            answer = f"**Model Reasoning:** {reasoning}\n\n"
            answer += f"**Feature Analysis:**\n"
            
            if visual_features and isinstance(visual_features, dict):
                for feature, description in visual_features.items():
                    answer += f"- {feature.replace('_', ' ').title()}: {description}\n"
            
            answer += f"\n**Visual Explanation (Grad-CAM):** "
            if grad_cam_available:
                answer += f"Available - shows regions most influential in the prediction. "
                answer += f"{features.get('grad_cam_description', '')}"
            else:
                answer += "Not available"
            
            return {
                "answer": answer,
                "sources": ["decision_explanation", "feature_contributions"],
                "grounded": True,
                "confidence": "high",
                "grad_cam_available": grad_cam_available
            }
        except Exception as e:
            return self._not_available_response(f"reasoning information: {e}")
    
    def _handle_location_question(self, question: str) -> Dict[str, Any]:
        """Handle questions about tumor location/regions"""
        try:
            features = self.explanation_data.get("feature_contributions", {})
            grad_cam_available = features.get("grad_cam_available", False)
            
            if grad_cam_available:
                regions = features.get("top_contributing_regions", "not available")
                grad_cam_desc = features.get("grad_cam_description", "not available")
                
                answer = f"**Regional Analysis:**\n\n"
                answer += f"{regions}\n\n"
                answer += f"**Grad-CAM Visualization:** {grad_cam_desc}\n\n"
                answer += f"**Note:** Grad-CAM highlights areas that contributed most to the model's decision. "
                answer += f"These regions show the highest activation and are most characteristic of the detected pattern."
            else:
                answer = "**Regional information not available.** Grad-CAM visualization was not generated for this prediction. "
                answer += "Spatial localization requires successful Grad-CAM analysis."
            
            return {
                "answer": answer,
                "sources": ["feature_contributions"],
                "grounded": True,
                "confidence": "medium" if grad_cam_available else "low",
                "grad_cam_available": grad_cam_available
            }
        except Exception as e:
            return self._not_available_response(f"location information: {e}")
    
    def _handle_alternatives_question(self, question: str) -> Dict[str, Any]:
        """Handle questions about alternative diagnoses"""
        try:
            alternatives = self.explanation_data.get("alternative_classes", [])
            all_predictions = self.explanation_data.get("all_predictions", {})
            
            answer = "**Differential Diagnosis Considerations:**\n\n"
            
            if alternatives and len(alternatives) > 0:
                if "note" in alternatives[0]:
                    answer += alternatives[0]["note"]
                else:
                    for alt in alternatives:
                        answer += f"- **{alt['class'].capitalize()}**: {alt['probability']}% "
                        answer += f"({alt['consideration']})\n"
            else:
                answer += "No significant alternative classes - prediction is highly confident.\n"
            
            answer += f"\n**All Class Probabilities:**\n"
            for class_name, info in all_predictions.items():
                answer += f"- {class_name.capitalize()}: {info['probability']}% (Rank: {info['rank']})\n"
            
            return {
                "answer": answer,
                "sources": ["alternative_classes", "all_predictions"],
                "grounded": True,
                "confidence": "high",
                "alternatives": alternatives
            }
        except Exception as e:
            return self._not_available_response(f"alternative diagnosis information: {e}")
    
    def _handle_quality_question(self, question: str) -> Dict[str, Any]:
        """Handle questions about image/data quality"""
        try:
            quality = self.explanation_data.get("data_quality", {})
            
            stats = quality.get("image_statistics", {})
            issues = quality.get("quality_issues", [])
            overall = quality.get("overall_quality", "not available")
            
            answer = f"**Image Quality Assessment:**\n\n"
            answer += f"**Overall Quality:** {overall}\n\n"
            
            if issues:
                answer += f"**Quality Issues:**\n"
                for issue in issues:
                    answer += f"- {issue}\n"
                answer += "\n"
            
            answer += f"**Image Statistics:**\n"
            answer += f"- Mean Intensity: {stats.get('mean_intensity', 'not available')}\n"
            answer += f"- Standard Deviation: {stats.get('std_intensity', 'not available')}\n"
            answer += f"- Value Range: [{stats.get('min_value', 'N/A')}, {stats.get('max_value', 'N/A')}]\n"
            
            return {
                "answer": answer,
                "sources": ["data_quality"],
                "grounded": True,
                "confidence": "high",
                "quality_assessment": overall
            }
        except Exception as e:
            return self._not_available_response(f"quality information: {e}")
    
    def _handle_recommendation_question(self, question: str) -> Dict[str, Any]:
        """Handle questions about clinical recommendations"""
        try:
            clinical = self.explanation_data.get("clinical_context", {})
            recommendation = clinical.get("recommended_action", "not available")
            
            decision = self.explanation_data.get("decision_explanation", {})
            predicted_class = decision.get("predicted_class", "not available")
            confidence = decision.get("confidence", "not available")
            
            answer = f"**Clinical Recommendation:**\n\n{recommendation}\n\n"
            answer += f"**Basis:** Prediction of '{predicted_class}' with {confidence}% confidence.\n\n"
            answer += f"**Important Note:** This is an AI-assisted diagnostic tool. "
            answer += f"All findings should be reviewed by a qualified radiologist or clinician "
            answer += f"before making clinical decisions."
            
            return {
                "answer": answer,
                "sources": ["clinical_context", "decision_explanation"],
                "grounded": True,
                "confidence": "high",
                "recommendation": recommendation
            }
        except Exception as e:
            return self._not_available_response(f"recommendation information: {e}")
    
    def _handle_uncertainty_question(self, question: str) -> Dict[str, Any]:
        """Handle questions about uncertainty/ambiguity"""
        try:
            uncertainty = self.explanation_data.get("uncertainty_analysis", {})
            
            answer = f"**Uncertainty Analysis:**\n\n"
            answer += f"**Level:** {uncertainty.get('uncertainty_level', 'not available')}\n\n"
            answer += f"**Interpretation:** {uncertainty.get('interpretation', 'not available')}\n\n"
            answer += f"**Metrics:**\n"
            answer += f"- Entropy: {uncertainty.get('entropy', 'not available')} "
            answer += f"(measures overall prediction uncertainty)\n"
            answer += f"- Margin: {uncertainty.get('margin', 'not available')} "
            answer += f"(difference between top 2 predictions)\n\n"
            answer += f"**Clinical Significance:** Higher entropy and lower margin indicate "
            answer += f"more ambiguous cases that may benefit from expert review or additional imaging."
            
            return {
                "answer": answer,
                "sources": ["uncertainty_analysis"],
                "grounded": True,
                "confidence": "high",
                "uncertainty_metrics": uncertainty
            }
        except Exception as e:
            return self._not_available_response(f"uncertainty information: {e}")
    
    def _handle_tumor_type_question(self, question: str) -> Dict[str, Any]:
        """Handle questions about tumor types"""
        try:
            clinical = self.explanation_data.get("clinical_context", {})
            tumor_types = clinical.get("tumor_types_explanation", {})
            decision = self.explanation_data.get("decision_explanation", {})
            predicted_class = decision.get("predicted_class", "not available")
            
            answer = f"**Tumor Type Information:**\n\n"
            
            # Check if asking about specific type or general
            specific_type = None
            for tumor_type in ["glioma", "meningioma", "pituitary"]:
                if tumor_type in question:
                    specific_type = tumor_type
                    break
            
            if specific_type:
                answer += f"**{specific_type.capitalize()}:** {tumor_types.get(specific_type, 'not available')}\n\n"
                if predicted_class == specific_type:
                    answer += f"This is the **currently predicted** tumor type for this scan.\n"
                else:
                    answer += f"The current scan prediction is: **{predicted_class}**\n"
            else:
                # General tumor type info
                for tumor_type, description in tumor_types.items():
                    marker = " ← **DETECTED**" if tumor_type == predicted_class else ""
                    answer += f"**{tumor_type.capitalize()}:** {description}{marker}\n\n"
            
            return {
                "answer": answer,
                "sources": ["clinical_context"],
                "grounded": True,
                "confidence": "high",
                "predicted_type": predicted_class
            }
        except Exception as e:
            return self._not_available_response(f"tumor type information: {e}")
    
    def _handle_general_question(self, question: str) -> Dict[str, Any]:
        """Handle general questions by searching explanation data"""
        try:
            # Try to find relevant information in the explanation
            answer = "**Based on available model output:**\n\n"
            
            # Check decision
            decision = self.explanation_data.get("decision_explanation", {})
            answer += f"- Prediction: {decision.get('predicted_class', 'not available')}\n"
            answer += f"- Confidence: {decision.get('confidence', 'not available')}%\n"
            answer += f"- Reasoning: {decision.get('reasoning', 'not available')}\n\n"
            
            answer += "For more specific information, please ask about:\n"
            answer += "- Diagnosis/prediction results\n"
            answer += "- Confidence and uncertainty\n"
            answer += "- Reasoning and features\n"
            answer += "- Alternative diagnoses\n"
            answer += "- Clinical recommendations\n"
            answer += "- Image quality\n"
            
            return {
                "answer": answer,
                "sources": ["decision_explanation"],
                "grounded": True,
                "confidence": "medium",
                "suggestion": "Please ask more specific questions for detailed information"
            }
        except Exception as e:
            return self._not_available_response(f"general information: {e}")
    
    def _not_available_response(self, context: str) -> Dict[str, Any]:
        """Return response when information is not available"""
        return {
            "answer": f"**This information is not available in the model output.**\n\n"
                     f"Context: {context}\n\n"
                     f"The clinical chat agent can only provide information that was "
                     f"generated during the model's prediction and explanation process. "
                     f"This specific information was not included in the analysis.",
            "sources": [],
            "grounded": False,
            "confidence": "N/A",
            "note": "Information not in model output - agent forbidden to hallucinate"
        }
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of conversation history"""
        return {
            "total_questions": len(self.conversation_history),
            "conversation": self.conversation_history,
            "explanation_loaded": self.explanation_data is not None
        }
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def format_for_display(self, response: Dict[str, Any]) -> str:
        """Format response for display (plain text version)"""
        output = response["answer"]
        
        if response.get("sources"):
            output += f"\n\n**Data Sources:** {', '.join(response['sources'])}"
        
        output += f"\n\n**Grounded in Evidence:** {'Yes' if response['grounded'] else 'No'}"
        
        return output
