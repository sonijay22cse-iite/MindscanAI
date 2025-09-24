import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json
import datetime

class SeverityLevel(Enum):
    MINIMAL = "minimal"
    MILD = "mild"
    MODERATE = "moderate"
    MODERATELY_SEVERE = "moderately_severe"
    SEVERE = "severe"

class RiskLevel(Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class AnalysisResult:
    """Structured analysis result"""
    assessment_type: str
    total_score: int
    max_possible_score: int
    severity_level: SeverityLevel
    risk_level: RiskLevel
    domain_scores: Dict[str, int]
    clinical_interpretation: str
    recommendations: List[str]
    red_flags: List[str]
    next_steps: List[str]
    timestamp: str

class CodeBasedAnalysisEngine:
    """
    Code-based analysis engine for mental health assessments
    Uses clinical algorithms and decision trees without external AI models
    """
    
    def __init__(self):
        self.scoring_algorithms = self._initialize_scoring_algorithms()
        self.diagnostic_criteria = self._initialize_diagnostic_criteria()
        self.severity_thresholds = self._initialize_severity_thresholds()
        self.visualization_config = self._initialize_visualization_config()
    
    def _initialize_scoring_algorithms(self) -> Dict[str, Dict]:
        """Initialize clinical scoring algorithms for different assessments"""
        return {
            "Depression Screening": {
                "algorithm": "PHQ-9",
                "questions": [
                    "little_interest", "feeling_down", "sleep_problems", "tired_little_energy",
                    "poor_appetite", "feeling_bad", "trouble_concentrating", "moving_slowly",
                    "suicidal_thoughts"
                ],
                "domains": {
                    "mood": ["little_interest", "feeling_down"],
                    "neurovegetative": ["sleep_problems", "tired_little_energy", "poor_appetite"],
                    "cognitive": ["feeling_bad", "trouble_concentrating"],
                    "psychomotor": ["moving_slowly"],
                    "suicidality": ["suicidal_thoughts"]
                },
                "max_score": 27,
                "cutoffs": {"minimal": (0, 4), "mild": (5, 9), "moderate": (10, 14), "moderately_severe": (15, 19), "severe": (20, 27)}
            },
            "Anxiety Disorders Screening": {
                "algorithm": "GAD-7",
                "questions": [
                    "feeling_nervous", "not_stop_worrying", "worrying_different_things", 
                    "trouble_relaxing", "restless_hard_still", "easily_annoyed", "afraid_awful_happen"
                ],
                "domains": {
                    "worry": ["feeling_nervous", "not_stop_worrying", "worrying_different_things"],
                    "physical_tension": ["trouble_relaxing", "restless_hard_still"],
                    "irritability": ["easily_annoyed"],
                    "apprehension": ["afraid_awful_happen"]
                },
                "max_score": 21,
                "cutoffs": {"minimal": (0, 4), "mild": (5, 9), "moderate": (10, 14), "severe": (15, 21)}
            },
            "Stress & Trauma Assessment": {
                "algorithm": "PSS-10",
                "questions": [
                    "upset_unexpected", "unable_control", "nervous_stressed", "confident_personal",
                    "things_going_way", "could_not_cope", "control_irritations", "on_top_things",
                    "angered_outside_control", "difficulties_piling"
                ],
                "reverse_score": ["confident_personal", "things_going_way", "control_irritations", "on_top_things"],
                "domains": {
                    "perceived_helplessness": ["upset_unexpected", "unable_control", "could_not_cope", "difficulties_piling"],
                    "perceived_self_efficacy": ["confident_personal", "things_going_way", "control_irritations", "on_top_things"],
                    "emotional_distress": ["nervous_stressed", "angered_outside_control"]
                },
                "max_score": 40,
                "cutoffs": {"minimal": (0, 13), "mild": (14, 19), "moderate": (20, 26), "severe": (27, 40)}
            },
            "Sleep Disorders Screening": {
                "algorithm": "PSQI",
                "components": {
                    "sleep_quality": {"question": "sleep_quality", "scoring": "direct"},
                    "sleep_latency": {"questions": ["sleep_latency_minutes", "sleep_latency_difficulty"], "scoring": "component"},
                    "sleep_duration": {"question": "hours_sleep", "scoring": "duration_bands"},
                    "sleep_efficiency": {"questions": ["hours_sleep", "time_in_bed"], "scoring": "efficiency_calc"},
                    "sleep_disturbances": {"questions": ["wake_middle", "bathroom", "breathe", "cough_snore", "cold", "hot", "bad_dreams", "pain", "other_disturb"], "scoring": "disturbance_sum"},
                    "sleep_medication": {"question": "sleep_medication", "scoring": "direct"},
                    "daytime_dysfunction": {"questions": ["trouble_staying_awake", "enthusiasm_problems"], "scoring": "component"}
                },
                "max_score": 21,
                "cutoffs": {"good": (0, 5), "poor": (6, 21)}
            },
            "General Mental Health Screening": {
                "algorithm": "K10",
                "questions": [
                    "tired_no_reason", "nervous", "nervous_nothing_calm", "hopeless",
                    "restless_fidgety", "restless_still", "depressed", "everything_effort",
                    "sad_nothing_cheer", "worthless"
                ],
                "domains": {
                    "anxiety": ["tired_no_reason", "nervous", "nervous_nothing_calm", "restless_fidgety", "restless_still"],
                    "depression": ["hopeless", "depressed", "sad_nothing_cheer", "worthless"],
                    "fatigue": ["everything_effort"]
                },
                "max_score": 50,
                "cutoffs": {"likely_well": (10, 15), "likely_mild": (16, 21), "likely_moderate": (22, 29), "likely_severe": (30, 50)}
            }
        }
    
    def _initialize_diagnostic_criteria(self) -> Dict[str, Dict]:
        """Initialize diagnostic criteria and decision trees"""
        return {
            "major_depression": {
                "core_symptoms": ["mood_low", "anhedonia"],
                "additional_symptoms": ["appetite", "sleep", "psychomotor", "fatigue", "worthlessness", "concentration", "suicidal_ideation"],
                "duration_weeks": 2,
                "functional_impairment": True,
                "exclusions": ["substance_use", "medical_condition"]
            },
            "generalized_anxiety": {
                "core_symptoms": ["excessive_worry", "difficulty_controlling"],
                "additional_symptoms": ["restless", "fatigue", "concentration", "irritability", "muscle_tension", "sleep_disturbance"],
                "duration_months": 6,
                "functional_impairment": True
            },
            "panic_disorder": {
                "core_symptoms": ["panic_attacks", "anticipatory_anxiety"],
                "attack_symptoms": ["palpitations", "sweating", "trembling", "shortness_breath", "choking", "chest_pain", "nausea", "dizziness", "derealization", "fear_losing_control", "fear_dying", "numbness", "chills"],
                "frequency": "recurrent",
                "duration_months": 1
            }
        }
    
    def _initialize_severity_thresholds(self) -> Dict[str, Dict]:
        """Initialize severity level thresholds for different conditions"""
        return {
            "depression": {
                SeverityLevel.MINIMAL: (0, 4),
                SeverityLevel.MILD: (5, 9),
                SeverityLevel.MODERATE: (10, 14),
                SeverityLevel.MODERATELY_SEVERE: (15, 19),
                SeverityLevel.SEVERE: (20, 27)
            },
            "anxiety": {
                SeverityLevel.MINIMAL: (0, 4),
                SeverityLevel.MILD: (5, 9),
                SeverityLevel.MODERATE: (10, 14),
                SeverityLevel.SEVERE: (15, 21)
            },
            "stress": {
                SeverityLevel.MINIMAL: (0, 13),
                SeverityLevel.MILD: (14, 19),
                SeverityLevel.MODERATE: (20, 26),
                SeverityLevel.SEVERE: (27, 40)
            },
            "sleep": {
                SeverityLevel.MINIMAL: (0, 5),
                SeverityLevel.MILD: (6, 8),
                SeverityLevel.MODERATE: (9, 12),
                SeverityLevel.SEVERE: (13, 21)
            }
        }
    
    def _initialize_visualization_config(self) -> Dict[str, Any]:
        """Initialize visualization configurations"""
        return {
            "colors": {
                SeverityLevel.MINIMAL: "#4CAF50",  # Green
                SeverityLevel.MILD: "#FFC107",      # Amber
                SeverityLevel.MODERATE: "#FF9800",  # Orange
                SeverityLevel.MODERATELY_SEVERE: "#FF5722",  # Deep Orange
                SeverityLevel.SEVERE: "#F44336"     # Red
            },
            "risk_colors": {
                RiskLevel.LOW: "#4CAF50",
                RiskLevel.MODERATE: "#FF9800", 
                RiskLevel.HIGH: "#FF5722",
                RiskLevel.CRITICAL: "#9C27B0"
            }
        }
    
    def analyze_assessment(self, assessment_data: Dict[str, Any]) -> AnalysisResult:
        """
        Main analysis function that processes assessment data
        Returns comprehensive analysis without external AI calls
        """
        
        assessment_type = assessment_data.get("assessment_type", "General Mental Health Screening")
        responses = assessment_data.get("responses", {})
        
        # Calculate scores using clinical algorithms
        total_score, domain_scores = self._calculate_scores(assessment_type, responses)
        
        # Determine severity level
        severity_level = self._determine_severity(assessment_type, total_score)
        
        # Assess risk level
        risk_level = self._assess_risk_level(assessment_type, responses, total_score)
        
        # Generate clinical interpretation
        clinical_interpretation = self._generate_interpretation(
            assessment_type, total_score, domain_scores, severity_level
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(assessment_type, severity_level, domain_scores)
        
        # Apply diagnostic decision trees
        provisional_diagnoses = self._apply_diagnostic_criteria(responses, domain_scores)
        
        # Identify red flags
        red_flags = self._identify_red_flags(responses, domain_scores)
        
        # Generate next steps
        next_steps = self._generate_next_steps(severity_level, risk_level, red_flags)
        
        # Get max possible score
        max_score = self.scoring_algorithms.get(assessment_type, {}).get("max_score", 100)
        
        return AnalysisResult(
            assessment_type=assessment_type,
            total_score=total_score,
            max_possible_score=max_score,
            severity_level=severity_level,
            risk_level=risk_level,
            domain_scores=domain_scores,
            clinical_interpretation=clinical_interpretation,
            recommendations=recommendations,
            red_flags=red_flags,
            next_steps=next_steps,
            timestamp=datetime.datetime.now().isoformat()
        )
    
    def _calculate_scores(self, assessment_type: str, responses: Dict[str, Any]) -> Tuple[int, Dict[str, int]]:
        """Calculate total and domain scores using validated clinical algorithms"""
        
        algorithm_config = self.scoring_algorithms.get(assessment_type, {})
        
        # Handle different assessment types with their specific scoring rules
        if assessment_type == "Depression Screening":
            return self._calculate_phq9_scores(responses, algorithm_config)
        elif assessment_type == "Anxiety Disorders Screening":
            return self._calculate_gad7_scores(responses, algorithm_config)
        elif assessment_type == "Stress & Trauma Assessment":
            return self._calculate_pss10_scores(responses, algorithm_config)
        elif assessment_type == "Sleep Disorders Screening":
            return self._calculate_psqi_scores(responses, algorithm_config)
        elif assessment_type == "General Mental Health Screening":
            return self._calculate_k10_scores(responses, algorithm_config)
        else:
            # Fallback to simple summation for unknown types
            questions = algorithm_config.get("questions", [])
            total_score = sum(self._extract_response_value(responses.get(q, 0)) for q in questions)
            return min(total_score, algorithm_config.get("max_score", 100)), {}
    
    def _calculate_phq9_scores(self, responses: Dict[str, Any], config: Dict[str, Any]) -> Tuple[int, Dict[str, int]]:
        """Calculate PHQ-9 scores (Depression Screening) using validated algorithm"""
        questions = config.get("questions", [])
        domains = config.get("domains", {})
        
        # Calculate total score (simple sum, no weighting)
        total_score = 0
        for question in questions:
            score = self._extract_response_value(responses.get(question, 0))
            total_score += score
        
        # Cap at validated maximum
        total_score = min(total_score, 27)
        
        # Calculate domain scores (simple sums within domains)
        domain_scores = {}
        for domain_name, domain_questions in domains.items():
            domain_score = sum(self._extract_response_value(responses.get(q, 0)) for q in domain_questions)
            domain_scores[domain_name] = domain_score
        
        return total_score, domain_scores
    
    def _calculate_gad7_scores(self, responses: Dict[str, Any], config: Dict[str, Any]) -> Tuple[int, Dict[str, int]]:
        """Calculate GAD-7 scores (Anxiety Screening) using validated algorithm"""
        questions = config.get("questions", [])
        domains = config.get("domains", {})
        
        # Calculate total score (simple sum, no weighting)
        total_score = 0
        for question in questions:
            score = self._extract_response_value(responses.get(question, 0))
            total_score += score
        
        # Cap at validated maximum
        total_score = min(total_score, 21)
        
        # Calculate domain scores
        domain_scores = {}
        for domain_name, domain_questions in domains.items():
            domain_score = sum(self._extract_response_value(responses.get(q, 0)) for q in domain_questions)
            domain_scores[domain_name] = domain_score
        
        return total_score, domain_scores
    
    def _calculate_pss10_scores(self, responses: Dict[str, Any], config: Dict[str, Any]) -> Tuple[int, Dict[str, int]]:
        """Calculate PSS-10 scores (Stress Assessment) with proper reverse scoring"""
        questions = config.get("questions", [])
        reverse_score = config.get("reverse_score", [])
        domains = config.get("domains", {})
        
        total_score = 0
        for question in questions:
            raw_score = self._extract_response_value(responses.get(question, 0))
            
            # Apply reverse scoring for specific items (0->4, 1->3, 2->2, 3->1, 4->0)
            if question in reverse_score:
                score = 4 - raw_score
            else:
                score = raw_score
            
            total_score += score
        
        # Cap at validated maximum
        total_score = min(total_score, 40)
        
        # Calculate domain scores with reverse scoring applied
        domain_scores = {}
        for domain_name, domain_questions in domains.items():
            domain_score = 0
            for q in domain_questions:
                raw_score = self._extract_response_value(responses.get(q, 0))
                if q in reverse_score:
                    domain_score += 4 - raw_score
                else:
                    domain_score += raw_score
            domain_scores[domain_name] = domain_score
        
        return total_score, domain_scores
    
    def _calculate_psqi_scores(self, responses: Dict[str, Any], config: Dict[str, Any]) -> Tuple[int, Dict[str, int]]:
        """Calculate PSQI scores (Sleep Assessment) using component scoring"""
        components = config.get("components", {})
        domain_scores = {}
        
        # Calculate each PSQI component (each scored 0-3)
        for component_name, component_config in components.items():
            component_score = self._calculate_psqi_component(component_name, component_config, responses)
            domain_scores[component_name] = component_score
        
        # Total PSQI score is sum of all components (0-21)
        total_score = sum(domain_scores.values())
        total_score = min(total_score, 21)
        
        return total_score, domain_scores
    
    def _calculate_psqi_component(self, component_name: str, config: Dict[str, Any], responses: Dict[str, Any]) -> int:
        """Calculate individual PSQI component score"""
        scoring_method = config.get("scoring", "direct")
        
        if scoring_method == "direct":
            question = config.get("question", "")
            return min(self._extract_response_value(responses.get(question, 0)), 3)
        
        elif scoring_method == "component":
            questions = config.get("questions", [])
            total = sum(self._extract_response_value(responses.get(q, 0)) for q in questions)
            # Convert to 0-3 scale
            if total == 0:
                return 0
            elif total <= 2:
                return 1
            elif total <= 4:
                return 2
            else:
                return 3
        
        elif scoring_method == "duration_bands":
            hours = self._extract_response_value(responses.get("hours_sleep", 7))
            if hours >= 7:
                return 0
            elif hours >= 6:
                return 1
            elif hours >= 5:
                return 2
            else:
                return 3
        
        elif scoring_method == "efficiency_calc":
            hours_sleep = self._extract_response_value(responses.get("hours_sleep", 7))
            time_in_bed = self._extract_response_value(responses.get("time_in_bed", 8))
            if time_in_bed > 0:
                efficiency = (hours_sleep / time_in_bed) * 100
                if efficiency >= 85:
                    return 0
                elif efficiency >= 75:
                    return 1
                elif efficiency >= 65:
                    return 2
                else:
                    return 3
            return 3
        
        elif scoring_method == "disturbance_sum":
            questions = config.get("questions", [])
            total = sum(self._extract_response_value(responses.get(q, 0)) for q in questions)
            if total == 0:
                return 0
            elif total <= 9:
                return 1
            elif total <= 18:
                return 2
            else:
                return 3
        
        return 0
    
    def _calculate_k10_scores(self, responses: Dict[str, Any], config: Dict[str, Any]) -> Tuple[int, Dict[str, int]]:
        """Calculate K10 scores (General Mental Health) using validated algorithm"""
        questions = config.get("questions", [])
        domains = config.get("domains", {})
        
        # K10 uses 1-5 scale, so we need to adjust our 0-4 scoring
        total_score = 0
        for question in questions:
            raw_score = self._extract_response_value(responses.get(question, 0))
            # Convert 0-4 scale to 1-5 scale for K10
            k10_score = raw_score + 1
            total_score += k10_score
        
        # Cap at validated maximum (10 questions × 5 points = 50 max)
        total_score = min(total_score, 50)
        
        # Calculate domain scores with K10 scaling
        domain_scores = {}
        for domain_name, domain_questions in domains.items():
            domain_score = 0
            for q in domain_questions:
                raw_score = self._extract_response_value(responses.get(q, 0))
                domain_score += raw_score + 1  # Convert to 1-5 scale
            domain_scores[domain_name] = domain_score
        
        return total_score, domain_scores
    
    def _apply_diagnostic_criteria(self, responses: Dict[str, Any], domain_scores: Dict[str, int]) -> List[Dict[str, Any]]:
        """Apply diagnostic decision trees to generate provisional diagnoses"""
        
        provisional_diagnoses = []
        
        # Check each diagnostic criteria
        for condition, criteria in self.diagnostic_criteria.items():
            diagnosis_result = self._evaluate_diagnostic_criteria(condition, criteria, responses, domain_scores)
            if diagnosis_result["meets_criteria"]:
                provisional_diagnoses.append(diagnosis_result)
        
        # Sort by confidence level
        provisional_diagnoses.sort(key=lambda x: x["confidence"], reverse=True)
        
        return provisional_diagnoses
    
    def _evaluate_diagnostic_criteria(self, condition: str, criteria: Dict[str, Any], 
                                    responses: Dict[str, Any], domain_scores: Dict[str, int]) -> Dict[str, Any]:
        """Evaluate specific diagnostic criteria for a condition"""
        
        core_symptoms = criteria.get("core_symptoms", [])
        additional_symptoms = criteria.get("additional_symptoms", [])
        
        # Check core symptoms (must have at least one)
        core_met = 0
        for symptom in core_symptoms:
            if self._extract_response_value(responses.get(symptom, 0)) >= 2:  # Moderate or higher
                core_met += 1
        
        # Check additional symptoms
        additional_met = 0
        for symptom in additional_symptoms:
            if self._extract_response_value(responses.get(symptom, 0)) >= 2:
                additional_met += 1
        
        # Apply condition-specific criteria
        meets_criteria = False
        confidence = 0.0
        rationale = []
        
        if condition == "major_depression":
            # DSM-5: At least 1 core symptom + 4 additional symptoms for 2+ weeks
            if core_met >= 1 and (core_met + additional_met) >= 5:
                meets_criteria = True
                confidence = min(0.9, (core_met * 0.3 + additional_met * 0.1))
                rationale.append(f"Core depressive symptoms present ({core_met}/2)")
                rationale.append(f"Additional symptoms present ({additional_met}/{len(additional_symptoms)})")
            elif core_met >= 1 and (core_met + additional_met) >= 3:
                # Subsyndromal depression
                meets_criteria = True
                confidence = 0.4
                rationale.append("Subsyndromal depression pattern identified")
        
        elif condition == "generalized_anxiety":
            # DSM-5: Excessive worry + 3 additional symptoms for 6+ months
            if core_met >= 1 and additional_met >= 3:
                meets_criteria = True
                confidence = min(0.8, (core_met * 0.4 + additional_met * 0.1))
                rationale.append(f"Excessive worry pattern present ({core_met}/2)")
                rationale.append(f"Physical anxiety symptoms present ({additional_met}/{len(additional_symptoms)})")
        
        elif condition == "panic_disorder":
            # Check for panic attack symptoms
            attack_symptoms = criteria.get("attack_symptoms", [])
            panic_symptoms_met = sum(1 for symptom in attack_symptoms 
                                   if self._extract_response_value(responses.get(symptom, 0)) >= 2)
            
            if core_met >= 1 and panic_symptoms_met >= 4:
                meets_criteria = True
                confidence = min(0.7, (panic_symptoms_met * 0.15))
                rationale.append(f"Panic attack criteria met ({panic_symptoms_met}/13 symptoms)")
        
        return {
            "condition": condition,
            "meets_criteria": meets_criteria,
            "confidence": confidence,
            "rationale": rationale,
            "core_symptoms_met": core_met,
            "additional_symptoms_met": additional_met,
            "total_criteria_met": core_met + additional_met
        }
    
    def _extract_response_value(self, response: Any) -> int:
        """Extract numeric value from various response formats"""
        if isinstance(response, (int, float)):
            return int(response)
        elif isinstance(response, str):
            if response.isdigit():
                return int(response)
            # Handle Likert scale responses
            likert_map = {
                "never": 0, "rarely": 1, "sometimes": 2, "often": 3, "always": 4,
                "not at all": 0, "several days": 1, "more than half": 2, "nearly every day": 3,
                "no difficulty": 0, "somewhat difficult": 1, "very difficult": 2, "extremely difficult": 3,
                "very good": 0, "fairly good": 1, "fairly bad": 2, "very bad": 3,
                "none": 0, "mild": 1, "moderate": 2, "severe": 3, "extreme": 4
            }
            return likert_map.get(response.lower(), 0)
        return 0
    
    def _determine_severity(self, assessment_type: str, total_score: int) -> SeverityLevel:
        """Determine severity level based on total score and assessment-specific cutoffs"""
        
        algorithm_config = self.scoring_algorithms.get(assessment_type, {})
        cutoffs = algorithm_config.get("cutoffs", {})
        
        # Use instrument-specific cutoffs directly
        for severity_name, score_range in cutoffs.items():
            min_score, max_score = score_range
            if min_score <= total_score <= max_score:
                # Map severity names to SeverityLevel enum
                severity_mapping = {
                    "minimal": SeverityLevel.MINIMAL,
                    "mild": SeverityLevel.MILD,
                    "moderate": SeverityLevel.MODERATE,
                    "moderately_severe": SeverityLevel.MODERATELY_SEVERE,
                    "severe": SeverityLevel.SEVERE,
                    "good": SeverityLevel.MINIMAL,  # PSQI
                    "poor": SeverityLevel.MODERATE,  # PSQI
                    "likely_well": SeverityLevel.MINIMAL,  # K10
                    "likely_mild": SeverityLevel.MILD,  # K10
                    "likely_moderate": SeverityLevel.MODERATE,  # K10
                    "likely_severe": SeverityLevel.SEVERE  # K10
                }
                return severity_mapping.get(severity_name, SeverityLevel.MODERATE)
        
        # If score doesn't fit any range, determine based on position relative to max
        max_score = algorithm_config.get("max_score", 100)
        score_percentage = (total_score / max_score) * 100
        
        if score_percentage >= 80:
            return SeverityLevel.SEVERE
        elif score_percentage >= 60:
            return SeverityLevel.MODERATE
        elif score_percentage >= 30:
            return SeverityLevel.MILD
        else:
            return SeverityLevel.MINIMAL
    
    def _assess_risk_level(self, assessment_type: str, responses: Dict[str, Any], total_score: int) -> RiskLevel:
        """Assess overall risk level based on responses and scores"""
        
        # Check for critical risk factors
        critical_responses = ["suicidal_ideation", "self_harm", "substance_abuse", "psychosis"]
        high_risk_responses = ["severe_depression", "panic_attacks", "trauma_symptoms"]
        
        has_critical = any(
            self._extract_response_value(responses.get(item, 0)) >= 2 
            for item in critical_responses
        )
        
        has_high_risk = any(
            self._extract_response_value(responses.get(item, 0)) >= 3
            for item in high_risk_responses
        )
        
        if has_critical:
            return RiskLevel.CRITICAL
        elif has_high_risk or total_score > 20:
            return RiskLevel.HIGH
        elif total_score > 10:
            return RiskLevel.MODERATE
        else:
            return RiskLevel.LOW
    
    def _generate_interpretation(self, assessment_type: str, total_score: int, 
                               domain_scores: Dict[str, int], severity_level: SeverityLevel) -> str:
        """Generate clinical interpretation based on analysis"""
        
        interpretations = {
            SeverityLevel.MINIMAL: f"The {assessment_type} indicates minimal symptoms with little functional impairment. The total score of {total_score} suggests that current symptoms are within the normal range or represent mild, transient concerns that may not require clinical intervention.",
            
            SeverityLevel.MILD: f"The assessment reveals mild symptoms that may warrant attention. With a total score of {total_score}, there are emerging concerns that could benefit from self-care strategies, lifestyle modifications, and monitoring for potential progression.",
            
            SeverityLevel.MODERATE: f"Moderate symptoms are present with a total score of {total_score}, indicating clinically significant concerns that are likely causing noticeable functional impairment. Professional evaluation and intervention are recommended to prevent symptom progression and improve quality of life.",
            
            SeverityLevel.MODERATELY_SEVERE: f"The assessment indicates moderately severe symptoms (score: {total_score}) with significant functional impairment across multiple life domains. Immediate professional intervention is recommended, with consideration for comprehensive treatment planning including therapy and possible medication evaluation.",
            
            SeverityLevel.SEVERE: f"Severe symptoms are present with a total score of {total_score}, indicating substantial functional impairment and significant distress. Urgent professional evaluation is required, with consideration for intensive treatment interventions and close monitoring for safety concerns."
        }
        
        base_interpretation = interpretations.get(severity_level, "Assessment completed with clinical significance requiring professional evaluation.")
        
        # Add domain-specific insights
        if domain_scores:
            highest_domain = max(domain_scores.keys(), key=lambda x: domain_scores[x])
            domain_insight = f"\n\nThe highest scoring domain is '{highest_domain}' with a score of {domain_scores[highest_domain]}, suggesting this area may require particular attention in treatment planning."
            base_interpretation += domain_insight
        
        return base_interpretation
    
    def _generate_recommendations(self, assessment_type: str, severity_level: SeverityLevel, 
                                domain_scores: Dict[str, int]) -> List[str]:
        """Generate evidence-based recommendations"""
        
        recommendations = []
        
        # Severity-based recommendations
        if severity_level in [SeverityLevel.MINIMAL, SeverityLevel.MILD]:
            recommendations.extend([
                "Continue regular self-care practices including adequate sleep, exercise, and stress management",
                "Practice mindfulness and relaxation techniques adapted for Indian cultural context",
                "Maintain social connections and family support systems",
                "Monitor symptoms and seek help if they worsen or persist"
            ])
        
        elif severity_level == SeverityLevel.MODERATE:
            recommendations.extend([
                "Seek professional consultation with a qualified mental health provider",
                "Consider structured therapy such as Cognitive Behavioral Therapy (CBT)",
                "Engage family support while maintaining personal autonomy as per Mental Healthcare Act 2017",
                "Implement lifestyle modifications including regular exercise and sleep hygiene"
            ])
        
        else:  # Moderately severe or severe
            recommendations.extend([
                "Urgent professional evaluation by psychiatrist or clinical psychologist required",
                "Consider comprehensive treatment plan including therapy and medication assessment",
                "Ensure safety planning and crisis support resources are in place",
                "Contact Tele MANAS (1800-891-4416) for immediate professional guidance",
                "Involve trusted family members in treatment planning with patient consent"
            ])
        
        # Domain-specific recommendations (using correct domain keys)
        if domain_scores:
            # Suicidality concerns (PHQ-9)
            if "suicidality" in domain_scores and domain_scores["suicidality"] > 2:
                recommendations.insert(0, "URGENT: Immediate safety assessment required due to concerning responses about self-harm thoughts")
            
            # Sleep disturbances (PSQI components or general sleep concerns)
            sleep_domains = ["sleep_quality", "sleep_duration", "sleep_disturbances", "daytime_dysfunction"]
            if any(domain in domain_scores and domain_scores[domain] > 2 for domain in sleep_domains):
                recommendations.append("Address sleep disturbances through sleep hygiene education and possible sleep study evaluation")
            
            # Anxiety symptoms (GAD-7 or K10)
            anxiety_domains = ["worry", "physical_tension", "anxiety"]
            if any(domain in domain_scores and domain_scores[domain] > 6 for domain in anxiety_domains):
                recommendations.append("Consider anxiety-specific interventions including relaxation training and gradual exposure techniques")
            
            # Depression symptoms (PHQ-9)
            if "mood" in domain_scores and domain_scores["mood"] > 4:
                recommendations.append("Address mood symptoms through structured therapy and lifestyle modifications")
            
            # Stress and coping concerns (PSS-10)
            if "perceived_helplessness" in domain_scores and domain_scores["perceived_helplessness"] > 8:
                recommendations.append("Focus on stress management and building coping skills through therapy")
            
            # Cognitive concerns
            cognitive_domains = ["cognitive", "trouble_concentrating"]
            if any(domain in domain_scores and domain_scores[domain] > 3 for domain in cognitive_domains):
                recommendations.append("Address concentration and cognitive concerns through cognitive rehabilitation techniques")
        
        return recommendations
    
    def _identify_red_flags(self, responses: Dict[str, Any], domain_scores: Dict[str, int]) -> List[str]:
        """Identify critical red flags requiring immediate attention"""
        
        red_flags = []
        
        # Suicidality screening
        suicidal_indicators = ["suicidal_ideation", "death_wishes", "self_harm"]
        for indicator in suicidal_indicators:
            if self._extract_response_value(responses.get(indicator, 0)) >= 1:
                red_flags.append("Suicidal ideation or self-harm thoughts reported - immediate safety assessment required")
                break
        
        # Substance use concerns
        substance_indicators = ["alcohol_use", "drug_use", "substance_problems"]
        if any(self._extract_response_value(responses.get(item, 0)) >= 2 for item in substance_indicators):
            red_flags.append("Concerning substance use patterns identified requiring specialized assessment")
        
        # Psychotic symptoms
        psychotic_indicators = ["hallucinations", "delusions", "paranoia", "reality_distortion"]
        if any(self._extract_response_value(responses.get(item, 0)) >= 1 for item in psychotic_indicators):
            red_flags.append("Possible psychotic symptoms requiring urgent psychiatric evaluation")
        
        # Severe functional impairment
        if domain_scores:
            total_domain_score = sum(domain_scores.values())
            if total_domain_score > 25:
                red_flags.append("Severe functional impairment across multiple life domains")
        
        # Trauma indicators
        trauma_indicators = ["trauma_exposure", "ptsd_symptoms", "dissociation"]
        if any(self._extract_response_value(responses.get(item, 0)) >= 2 for item in trauma_indicators):
            red_flags.append("Trauma-related symptoms requiring specialized trauma-informed care")
        
        return red_flags
    
    def _generate_next_steps(self, severity_level: SeverityLevel, risk_level: RiskLevel, 
                           red_flags: List[str]) -> List[str]:
        """Generate specific next steps based on analysis results"""
        
        next_steps = []
        
        # Risk-based immediate steps
        if risk_level == RiskLevel.CRITICAL or red_flags:
            next_steps.extend([
                "IMMEDIATE: Contact emergency services (102) or nearest emergency department if in immediate danger",
                "Contact Tele MANAS helpline: 1800-891-4416 for crisis intervention",
                "Ensure continuous supervision until professional evaluation is completed",
                "Remove access to means of self-harm if suicide risk is present"
            ])
        
        elif risk_level == RiskLevel.HIGH:
            next_steps.extend([
                "Schedule urgent appointment with mental health professional within 24-48 hours",
                "Contact Tele MANAS (1800-891-4416) for immediate guidance and support",
                "Inform trusted family member or friend about current mental health status",
                "Consider taking time off work/studies if functioning is significantly impaired"
            ])
        
        elif risk_level == RiskLevel.MODERATE:
            next_steps.extend([
                "Schedule appointment with mental health professional within 1-2 weeks",
                "Begin implementing recommended self-care strategies immediately",
                "Monitor symptoms daily and seek urgent help if worsening",
                "Access Tele MANAS resources for ongoing support and guidance"
            ])
        
        else:  # Low risk
            next_steps.extend([
                "Continue monitoring symptoms and maintain healthy lifestyle practices",
                "Consider preventive mental health consultation if symptoms persist",
                "Utilize available mental health resources and educational materials",
                "Schedule follow-up assessment if concerns arise"
            ])
        
        # Universal next steps
        next_steps.extend([
            "Save this analysis report for discussion with healthcare provider",
            "Review Mental Healthcare Act 2017 rights and protections available",
            "Consider engaging family support while maintaining personal autonomy",
            "Access additional resources through National Mental Health Programme"
        ])
        
        return next_steps
    
    def create_visual_analysis(self, analysis_result: AnalysisResult) -> Dict[str, Any]:
        """Create comprehensive visual representations of analysis results"""
        
        visualizations = {}
        
        # 1. Overall severity gauge
        visualizations['severity_gauge'] = self._create_severity_gauge(analysis_result)
        
        # 2. Domain scores radar chart
        if analysis_result.domain_scores:
            visualizations['domain_radar'] = self._create_domain_radar(analysis_result)
        
        # 3. Risk assessment visualization
        visualizations['risk_assessment'] = self._create_risk_visualization(analysis_result)
        
        # 4. Score comparison chart
        visualizations['score_comparison'] = self._create_score_comparison(analysis_result)
        
        # 5. Recommendations priority matrix
        visualizations['recommendations_matrix'] = self._create_recommendations_matrix(analysis_result)
        
        return visualizations
    
    def _create_severity_gauge(self, analysis_result: AnalysisResult) -> go.Figure:
        """Create a gauge chart showing severity level"""
        
        # Map severity to numeric scale
        severity_values = {
            SeverityLevel.MINIMAL: 1,
            SeverityLevel.MILD: 2, 
            SeverityLevel.MODERATE: 3,
            SeverityLevel.MODERATELY_SEVERE: 4,
            SeverityLevel.SEVERE: 5
        }
        
        severity_value = severity_values.get(analysis_result.severity_level, 3)
        color = self.visualization_config["colors"][analysis_result.severity_level]
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = severity_value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"Severity Level: {analysis_result.severity_level.value.title()}"},
            delta = {'reference': 2.5},
            gauge = {
                'axis': {'range': [None, 5]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 1], 'color': self.visualization_config["colors"][SeverityLevel.MINIMAL]},
                    {'range': [1, 2], 'color': self.visualization_config["colors"][SeverityLevel.MILD]},
                    {'range': [2, 3], 'color': self.visualization_config["colors"][SeverityLevel.MODERATE]},
                    {'range': [3, 4], 'color': self.visualization_config["colors"][SeverityLevel.MODERATELY_SEVERE]},
                    {'range': [4, 5], 'color': self.visualization_config["colors"][SeverityLevel.SEVERE]}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 4
                }
            }
        ))
        
        fig.update_layout(
            title=f"Mental Health Assessment Results - Total Score: {analysis_result.total_score}/{analysis_result.max_possible_score}",
            font={'size': 14}
        )
        
        return fig
    
    def _create_domain_radar(self, analysis_result: AnalysisResult) -> go.Figure:
        """Create radar chart for domain scores"""
        
        domains = list(analysis_result.domain_scores.keys())
        scores = list(analysis_result.domain_scores.values())
        
        # Normalize scores for radar chart (0-10 scale)
        max_domain_score = max(scores) if scores else 1
        normalized_scores = [(score/max_domain_score) * 10 for score in scores]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=normalized_scores + [normalized_scores[0]],  # Close the shape
            theta=domains + [domains[0]],
            fill='toself',
            name='Current Scores',
            line_color='rgba(255, 99, 132, 1)',
            fillcolor='rgba(255, 99, 132, 0.25)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=True,
            title="Domain Analysis Profile"
        )
        
        return fig
    
    def _create_risk_visualization(self, analysis_result: AnalysisResult) -> go.Figure:
        """Create risk level visualization"""
        
        risk_levels = ['Low', 'Moderate', 'High', 'Critical']
        risk_values = [0, 0, 0, 0]
        
        # Set current risk level
        current_risk_index = {
            RiskLevel.LOW: 0,
            RiskLevel.MODERATE: 1,
            RiskLevel.HIGH: 2, 
            RiskLevel.CRITICAL: 3
        }
        
        risk_values[current_risk_index[analysis_result.risk_level]] = 1
        
        colors = ['#4CAF50', '#FF9800', '#FF5722', '#9C27B0']
        
        fig = go.Figure(data=[
            go.Bar(
                x=risk_levels,
                y=risk_values,
                marker_color=colors,
                text=[f'{level} Risk' if val else '' for level, val in zip(risk_levels, risk_values)],
                textposition='inside'
            )
        ])
        
        fig.update_layout(
            title=f"Current Risk Level: {analysis_result.risk_level.value.title()}",
            yaxis_title="Risk Indicator",
            xaxis_title="Risk Levels",
            showlegend=False
        )
        
        return fig
    
    def _create_score_comparison(self, analysis_result: AnalysisResult) -> go.Figure:
        """Create score comparison visualization"""
        
        categories = ['Current Score', 'Threshold Score', 'Maximum Possible']
        values = [
            analysis_result.total_score,
            analysis_result.max_possible_score * 0.6,  # Typical clinical threshold
            analysis_result.max_possible_score
        ]
        
        colors = ['#FF6384', '#36A2EB', '#4BC0C0']
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=values,
                marker_color=colors,
                text=values,
                textposition='inside'
            )
        ])
        
        fig.update_layout(
            title="Score Analysis Comparison",
            yaxis_title="Score",
            showlegend=False
        )
        
        return fig
    
    def _create_recommendations_matrix(self, analysis_result: AnalysisResult) -> go.Figure:
        """Create recommendations priority matrix"""
        
        # Categorize recommendations by urgency and importance
        urgent_important = []
        urgent_not_important = []
        not_urgent_important = []
        not_urgent_not_important = []
        
        for rec in analysis_result.recommendations:
            if any(word in rec.lower() for word in ['urgent', 'immediate', 'crisis']):
                if any(word in rec.lower() for word in ['professional', 'treatment', 'evaluation']):
                    urgent_important.append(rec[:50] + "...")
                else:
                    urgent_not_important.append(rec[:50] + "...")
            else:
                if any(word in rec.lower() for word in ['professional', 'treatment', 'therapy']):
                    not_urgent_important.append(rec[:50] + "...")
                else:
                    not_urgent_not_important.append(rec[:50] + "...")
        
        # Create matrix data
        matrix_data = [
            ['High Urgency<br>High Importance', 'High Urgency<br>Low Importance'],
            ['Low Urgency<br>High Importance', 'Low Urgency<br>Low Importance']
        ]
        
        fig = go.Figure(data=go.Heatmap(
            z=[[2, 1], [1, 0]],
            x=['Low Importance', 'High Importance'],
            y=['High Urgency', 'Low Urgency'],
            colorscale=[[0, '#4CAF50'], [1, '#F44336']],
            showscale=False,
            text=matrix_data,
            texttemplate="%{text}",
            textfont={"size": 12}
        ))
        
        fig.update_layout(
            title="Recommendations Priority Matrix",
            xaxis_title="Importance Level",
            yaxis_title="Urgency Level"
        )
        
        return fig

    def display_comprehensive_analysis(self, analysis_result: AnalysisResult):
        """Display comprehensive analysis with visualizations in Streamlit"""
        
        st.header("📊 Comprehensive Analysis Results")
        
        # Executive Summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Score", 
                f"{analysis_result.total_score}/{analysis_result.max_possible_score}",
                delta=f"{((analysis_result.total_score/analysis_result.max_possible_score)*100):.1f}%"
            )
        
        with col2:
            severity_color = self.visualization_config["colors"][analysis_result.severity_level]
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; border-radius: 5px; background-color: {severity_color}20; border: 2px solid {severity_color};">
                <h4 style="color: {severity_color}; margin: 0;">Severity Level</h4>
                <p style="color: {severity_color}; margin: 0; font-weight: bold;">{analysis_result.severity_level.value.title()}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            risk_color = self.visualization_config["risk_colors"][analysis_result.risk_level]
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; border-radius: 5px; background-color: {risk_color}20; border: 2px solid {risk_color};">
                <h4 style="color: {risk_color}; margin: 0;">Risk Level</h4>
                <p style="color: {risk_color}; margin: 0; font-weight: bold;">{analysis_result.risk_level.value.title()}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.metric(
                "Assessment Type",
                analysis_result.assessment_type,
                delta="Completed"
            )
        
        # Create and display visualizations
        visualizations = self.create_visual_analysis(analysis_result)
        
        # Display severity gauge
        st.subheader("🎯 Severity Assessment")
        st.plotly_chart(visualizations['severity_gauge'], use_container_width=True)
        
        # Display domain analysis if available
        if analysis_result.domain_scores:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Domain Analysis")
                st.plotly_chart(visualizations['domain_radar'], use_container_width=True)
            
            with col2:
                st.subheader("🔄 Score Comparison")
                st.plotly_chart(visualizations['score_comparison'], use_container_width=True)
        
        # Risk assessment visualization
        st.subheader("⚠️ Risk Assessment")
        st.plotly_chart(visualizations['risk_assessment'], use_container_width=True)
        
        # Clinical interpretation
        st.subheader("🏥 Clinical Interpretation")
        st.info(analysis_result.clinical_interpretation)
        
        # Red flags section
        if analysis_result.red_flags:
            st.subheader("🚨 Important Alerts")
            for flag in analysis_result.red_flags:
                st.error(f"⚠️ **ALERT**: {flag}")
        
        # Recommendations
        st.subheader("💡 Recommendations")
        for i, rec in enumerate(analysis_result.recommendations, 1):
            st.markdown(f"**{i}.** {rec}")
        
        # Next steps
        st.subheader("📋 Next Steps")
        for i, step in enumerate(analysis_result.next_steps, 1):
            if "IMMEDIATE" in step or "URGENT" in step:
                st.error(f"**{i}.** {step}")
            else:
                st.markdown(f"**{i}.** {step}")
        
        # Domain scores breakdown
        if analysis_result.domain_scores:
            st.subheader("📊 Detailed Domain Scores")
            domain_data = {
                'Domain': list(analysis_result.domain_scores.keys()),
                'Score': list(analysis_result.domain_scores.values())
            }
            domain_df = pd.DataFrame(domain_data)
            st.dataframe(domain_df, use_container_width=True)
        
        # Compliance and legal information
        st.subheader("⚖️ Important Legal Information")
        st.warning("""
        **Mental Healthcare Act 2017 Compliance**: This analysis is generated using evidence-based clinical algorithms 
        and is intended for screening and educational purposes only. All results require validation by qualified 
        mental health professionals. This tool does not replace professional medical diagnosis or treatment.
        
        **Data Protection**: Your assessment data is processed in compliance with DPDPA 2023 regulations and 
        is encrypted for security.
        """)
        
        # Contact information
        st.info("""
        **Professional Support Available**:
        - **Tele MANAS**: 1800-891-4416 (24/7 Mental Health Support)
        - **Emergency Services**: 102 (Police) | 108 (Ambulance)
        - **DPO Contact**: dpo@mentalhealthplatform.gov.in
        """)