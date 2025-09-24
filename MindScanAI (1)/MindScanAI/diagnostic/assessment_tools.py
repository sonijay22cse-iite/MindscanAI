import streamlit as st
from typing import Dict, List, Any, Optional
import datetime
import math
from diagnostic.conditions_database import ConditionsDatabase

class AssessmentTools:
    """Comprehensive assessment tools for mental health evaluation"""
    
    def __init__(self):
        self.conditions_db = ConditionsDatabase()
        self.scoring_algorithms = self._initialize_scoring_algorithms()
        self.clinical_cutoffs = self._initialize_clinical_cutoffs()
        self.severity_mappings = self._initialize_severity_mappings()
    
    def _initialize_scoring_algorithms(self) -> Dict[str, Any]:
        """Initialize validated scoring algorithms"""
        return {
            'phq9': {
                'name': 'Patient Health Questionnaire-9',
                'domains': ['depression'],
                'questions': ['dep_001', 'dep_002', 'dep_003', 'dep_004', 'dep_005'],
                'scoring': 'sum',
                'max_score': 27,
                'cutoffs': {'mild': 5, 'moderate': 10, 'severe': 15, 'very_severe': 20}
            },
            'gad7': {
                'name': 'Generalized Anxiety Disorder-7',
                'domains': ['anxiety'],
                'questions': ['anx_001', 'anx_002', 'anx_003', 'anx_004', 'anx_005'],
                'scoring': 'sum',
                'max_score': 21,
                'cutoffs': {'mild': 5, 'moderate': 10, 'severe': 15}
            },
            'pcl5': {
                'name': 'PTSD Checklist for DSM-5',
                'domains': ['trauma', 'ptsd'],
                'questions': ['trauma_001', 'trauma_002', 'trauma_003', 'trauma_004'],
                'scoring': 'sum',
                'max_score': 80,
                'cutoffs': {'mild': 25, 'moderate': 38, 'severe': 50}
            },
            'audit': {
                'name': 'Alcohol Use Disorders Identification Test',
                'domains': ['substance_use', 'alcohol'],
                'questions': ['sub_001', 'sub_002', 'sub_003'],
                'scoring': 'sum',
                'max_score': 40,
                'cutoffs': {'low_risk': 7, 'hazardous': 15, 'harmful': 19, 'dependent': 20}
            },
            'psqi': {
                'name': 'Pittsburgh Sleep Quality Index',
                'domains': ['sleep'],
                'questions': ['sleep_001', 'sleep_002', 'sleep_003', 'sleep_004'],
                'scoring': 'weighted_sum',
                'max_score': 21,
                'cutoffs': {'good': 5, 'poor': 6}
            }
        }
    
    def _initialize_clinical_cutoffs(self) -> Dict[str, Dict[str, int]]:
        """Initialize clinical cutoff scores for Indian population"""
        return {
            'depression_severity': {
                'minimal': (0, 4),
                'mild': (5, 9),
                'moderate': (10, 14),
                'moderately_severe': (15, 19),
                'severe': (20, 27)
            },
            'anxiety_severity': {
                'minimal': (0, 4),
                'mild': (5, 9),
                'moderate': (10, 14),
                'severe': (15, 21)
            },
            'trauma_severity': {
                'minimal': (0, 24),
                'mild': (25, 37),
                'moderate': (38, 49),
                'severe': (50, 80)
            },
            'alcohol_risk': {
                'low': (0, 7),
                'moderate': (8, 15),
                'high': (16, 19),
                'very_high': (20, 40)
            },
            'sleep_quality': {
                'good': (0, 5),
                'poor': (6, 21)
            }
        }
    
    def _initialize_severity_mappings(self) -> Dict[str, Dict[str, Any]]:
        """Initialize severity level mappings with interventions"""
        return {
            'minimal': {
                'color': 'green',
                'description': 'Minimal symptoms with little to no functional impairment',
                'interventions': ['Psychoeducation', 'Self-help resources', 'Lifestyle modifications'],
                'monitoring': 'Annual screening',
                'urgency': 'routine'
            },
            'mild': {
                'color': 'yellow',
                'description': 'Mild symptoms with minor functional impairment',
                'interventions': ['Brief counseling', 'Self-guided therapy', 'Support groups'],
                'monitoring': 'Quarterly follow-up',
                'urgency': 'routine'
            },
            'moderate': {
                'color': 'orange',
                'description': 'Moderate symptoms with noticeable functional impairment',
                'interventions': ['Psychotherapy', 'Structured interventions', 'Medication consideration'],
                'monitoring': 'Monthly follow-up',
                'urgency': 'priority'
            },
            'severe': {
                'color': 'red',
                'description': 'Severe symptoms with significant functional impairment',
                'interventions': ['Intensive therapy', 'Medication', 'Case management'],
                'monitoring': 'Weekly follow-up',
                'urgency': 'urgent'
            },
            'very_severe': {
                'color': 'darkred',
                'description': 'Very severe symptoms with major functional impairment',
                'interventions': ['Crisis intervention', 'Hospitalization consideration', 'Intensive treatment'],
                'monitoring': 'Daily contact',
                'urgency': 'emergency'
            }
        }
    
    def analyze_responses(self, responses: Dict[str, Any], assessment_type: str) -> Dict[str, Any]:
        """Comprehensive analysis of assessment responses"""
        
        analysis_results = {
            'assessment_type': assessment_type,
            'timestamp': datetime.datetime.now().isoformat(),
            'domain_scores': {},
            'severity_assessments': {},
            'risk_indicators': [],
            'protective_factors': [],
            'functional_impairment': {},
            'crisis_flags': [],
            'recommendations': [],
            'next_steps': []
        }
        
        # Calculate domain scores
        domain_scores = self._calculate_domain_scores(responses, assessment_type)
        analysis_results['domain_scores'] = domain_scores
        
        # Assess severity levels
        severity_assessments = self._assess_severity_levels(domain_scores)
        analysis_results['severity_assessments'] = severity_assessments
        
        # Identify risk indicators
        risk_indicators = self._identify_risk_indicators(responses)
        analysis_results['risk_indicators'] = risk_indicators
        
        # Identify protective factors
        protective_factors = self._identify_protective_factors(responses)
        analysis_results['protective_factors'] = protective_factors
        
        # Assess functional impairment
        functional_impairment = self._assess_functional_impairment(responses)
        analysis_results['functional_impairment'] = functional_impairment
        
        # Check for crisis indicators
        crisis_flags = self._check_crisis_indicators(responses)
        analysis_results['crisis_flags'] = crisis_flags
        
        # Generate recommendations
        recommendations = self._generate_recommendations(analysis_results)
        analysis_results['recommendations'] = recommendations
        
        # Determine next steps
        next_steps = self._determine_next_steps(analysis_results)
        analysis_results['next_steps'] = next_steps
        
        return analysis_results
    
    def _calculate_domain_scores(self, responses: Dict[str, Any], assessment_type: str) -> Dict[str, float]:
        """Calculate scores for different symptom domains"""
        
        domain_scores = {}
        
        # Define domain mappings
        domain_mappings = {
            'depression': ['gen_001', 'gen_002', 'dep_001', 'dep_002', 'dep_003', 'dep_004', 'dep_005'],
            'anxiety': ['gen_003', 'gen_004', 'anx_001', 'anx_002', 'anx_003', 'anx_004', 'anx_005'],
            'trauma': ['trauma_001', 'trauma_002', 'trauma_003', 'trauma_004'],
            'substance_use': ['sub_001', 'sub_002', 'sub_003', 'sub_004'],
            'sleep': ['sleep_001', 'sleep_002', 'sleep_003', 'sleep_004'],
            'stress': ['gen_005'],
            'coping': ['gen_006']
        }
        
        for domain, question_ids in domain_mappings.items():
            domain_responses = []
            
            for question_id in question_ids:
                if question_id in responses:
                    response = responses[question_id]
                    
                    # Handle different response types
                    if isinstance(response, (int, float)):
                        domain_responses.append(response)
                    elif isinstance(response, str):
                        # Convert string responses to numeric
                        numeric_value = self._convert_string_to_numeric(response, question_id)
                        if numeric_value is not None:
                            domain_responses.append(numeric_value)
                    elif isinstance(response, list):
                        # Handle checkbox responses
                        domain_responses.append(len(response))
            
            if domain_responses:
                # Calculate domain score (normalized to 0-100)
                avg_response = sum(domain_responses) / len(domain_responses)
                max_possible = 4  # Assuming most scales are 0-4
                normalized_score = (avg_response / max_possible) * 100
                domain_scores[domain] = min(100, max(0, normalized_score))
        
        return domain_scores
    
    def _convert_string_to_numeric(self, response: str, question_id: str) -> Optional[float]:
        """Convert string responses to numeric values"""
        
        # Common response mappings
        response_mappings = {
            'never': 0, 'not at all': 0, 'no': 0,
            'rarely': 1, 'several days': 1, 'yes': 1,
            'sometimes': 2, 'more than half the days': 2,
            'often': 3, 'nearly every day': 3,
            'always': 4, 'very often': 4
        }
        
        response_lower = response.lower().strip()
        
        # Direct mapping
        if response_lower in response_mappings:
            return response_mappings[response_lower]
        
        # Handle alcohol-specific responses
        if 'monthly' in response_lower:
            return 1
        elif '2-4 times' in response_lower:
            return 2
        elif '2-3 times' in response_lower:
            return 3
        elif '4 or more' in response_lower:
            return 4
        
        # Handle quantity responses
        if '1 or 2' in response_lower:
            return 1
        elif '3 or 4' in response_lower:
            return 2
        elif '5 or 6' in response_lower:
            return 3
        elif '7 to 9' in response_lower:
            return 4
        elif '10 or more' in response_lower:
            return 5
        
        return None
    
    def _assess_severity_levels(self, domain_scores: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
        """Assess severity levels for each domain"""
        
        severity_assessments = {}
        
        for domain, score in domain_scores.items():
            severity_level = self._determine_severity_level(score, domain)
            severity_info = self.severity_mappings.get(severity_level, self.severity_mappings['minimal'])
            
            severity_assessments[domain] = {
                'score': score,
                'level': severity_level,
                'description': severity_info['description'],
                'color': severity_info['color'],
                'interventions': severity_info['interventions'],
                'monitoring': severity_info['monitoring'],
                'urgency': severity_info['urgency']
            }
        
        return severity_assessments
    
    def _determine_severity_level(self, score: float, domain: str) -> str:
        """Determine severity level based on score and domain"""
        
        # Domain-specific thresholds (0-100 scale)
        thresholds = {
            'depression': {'mild': 20, 'moderate': 40, 'severe': 60, 'very_severe': 80},
            'anxiety': {'mild': 25, 'moderate': 45, 'severe': 70},
            'trauma': {'mild': 30, 'moderate': 50, 'severe': 75},
            'substance_use': {'mild': 20, 'moderate': 40, 'severe': 70},
            'sleep': {'mild': 30, 'moderate': 60},
            'stress': {'mild': 25, 'moderate': 50, 'severe': 75},
            'coping': {'mild': 30, 'moderate': 60}  # Note: lower coping scores are worse
        }
        
        domain_thresholds = thresholds.get(domain, thresholds['depression'])
        
        # For coping domain, reverse the logic (lower scores = worse)
        if domain == 'coping':
            score = 100 - score
        
        if score < domain_thresholds.get('mild', 20):
            return 'minimal'
        elif score < domain_thresholds.get('moderate', 40):
            return 'mild'
        elif score < domain_thresholds.get('severe', 60):
            return 'moderate'
        elif score < domain_thresholds.get('very_severe', 80):
            return 'severe'
        else:
            return 'very_severe'
    
    def _identify_risk_indicators(self, responses: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify clinical risk indicators"""
        
        risk_indicators = []
        
        # Suicidal ideation risk
        if responses.get('dep_005', 0) >= 1:
            risk_indicators.append({
                'type': 'suicidal_ideation',
                'severity': 'high',
                'description': 'Thoughts of death or self-harm reported',
                'intervention': 'Immediate crisis assessment required',
                'priority': 1
            })
        
        # Substance use risk
        if responses.get('sub_004') == 'Yes':
            risk_indicators.append({
                'type': 'substance_abuse',
                'severity': 'moderate',
                'description': 'Illegal drug use or prescription misuse reported',
                'intervention': 'Substance abuse evaluation recommended',
                'priority': 2
            })
        
        # Severe anxiety/panic
        if responses.get('anx_001', 0) >= 3:
            risk_indicators.append({
                'type': 'panic_disorder',
                'severity': 'moderate',
                'description': 'Frequent panic episodes reported',
                'intervention': 'Anxiety disorder assessment needed',
                'priority': 3
            })
        
        # Trauma exposure
        if responses.get('trauma_001') in ['Yes, once', 'Yes, multiple times']:
            risk_indicators.append({
                'type': 'trauma_exposure',
                'severity': 'moderate',
                'description': 'Traumatic event exposure reported',
                'intervention': 'Trauma-informed care assessment',
                'priority': 3
            })
        
        # Functional impairment
        high_impairment_responses = [
            responses.get('anx_005', 0),
            responses.get('severity_function_001', 0),
            responses.get('severity_social_001', 0)
        ]
        
        if any(response >= 3 for response in high_impairment_responses if response is not None):
            risk_indicators.append({
                'type': 'functional_impairment',
                'severity': 'moderate',
                'description': 'Significant functional impairment reported',
                'intervention': 'Comprehensive functional assessment',
                'priority': 2
            })
        
        return sorted(risk_indicators, key=lambda x: x['priority'])
    
    def _identify_protective_factors(self, responses: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify protective factors and resilience indicators"""
        
        protective_factors = []
        
        # Good coping skills
        if responses.get('gen_006', 0) >= 3:
            protective_factors.append({
                'type': 'coping_skills',
                'strength': 'high',
                'description': 'Strong confidence in handling personal problems',
                'impact': 'Reduced risk of symptom escalation'
            })
        
        # No substance use
        if responses.get('sub_001') == 'No':
            protective_factors.append({
                'type': 'no_substance_use',
                'strength': 'moderate',
                'description': 'No alcohol use reported',
                'impact': 'Lower risk of substance-related complications'
            })
        
        # Good sleep quality
        if responses.get('sleep_001', 0) <= 1:
            protective_factors.append({
                'type': 'sleep_quality',
                'strength': 'moderate',
                'description': 'Good sleep quality reported',
                'impact': 'Better emotional regulation and cognitive function'
            })
        
        # No trauma exposure
        if responses.get('trauma_001') == 'No':
            protective_factors.append({
                'type': 'no_trauma',
                'strength': 'moderate',
                'description': 'No traumatic event exposure',
                'impact': 'Lower risk of trauma-related disorders'
            })
        
        return protective_factors
    
    def _assess_functional_impairment(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Assess functional impairment across domains"""
        
        impairment_assessment = {
            'work_academic': 0,
            'social_relationships': 0,
            'daily_activities': 0,
            'overall_impairment': 0,
            'severity_level': 'minimal'
        }
        
        # Collect impairment ratings
        impairment_responses = []
        
        if 'anx_005' in responses:
            impairment_responses.append(responses['anx_005'])
        
        if 'severity_function_001' in responses:
            impairment_assessment['work_academic'] = responses['severity_function_001']
            impairment_responses.append(responses['severity_function_001'])
        
        if 'severity_social_001' in responses:
            impairment_assessment['social_relationships'] = responses['severity_social_001']
            impairment_responses.append(responses['severity_social_001'])
        
        # Calculate overall impairment
        if impairment_responses:
            overall_impairment = sum(impairment_responses) / len(impairment_responses)
            impairment_assessment['overall_impairment'] = overall_impairment
            
            # Determine severity level
            if overall_impairment <= 1:
                impairment_assessment['severity_level'] = 'minimal'
            elif overall_impairment <= 2:
                impairment_assessment['severity_level'] = 'mild'
            elif overall_impairment <= 3:
                impairment_assessment['severity_level'] = 'moderate'
            else:
                impairment_assessment['severity_level'] = 'severe'
        
        return impairment_assessment
    
    def _check_crisis_indicators(self, responses: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for immediate crisis indicators"""
        
        crisis_flags = []
        
        # Suicidal ideation
        if responses.get('dep_005', 0) >= 2:
            crisis_flags.append({
                'type': 'suicidal_ideation',
                'severity': 'high',
                'description': 'Frequent thoughts of death or self-harm',
                'action': 'Immediate safety assessment required',
                'contact': 'Tele MANAS: 1800-891-4416'
            })
        
        # Crisis-level responses from additional questions
        if responses.get('crisis_suicide_001') in ['Often', 'Right now']:
            crisis_flags.append({
                'type': 'active_suicidal_ideation',
                'severity': 'critical',
                'description': 'Active suicidal thoughts reported',
                'action': 'Emergency intervention required',
                'contact': 'Emergency Services: 112, Tele MANAS: 1800-891-4416'
            })
        
        if responses.get('crisis_suicide_002') in ['Specific plan', 'Detailed plan']:
            crisis_flags.append({
                'type': 'suicide_plan',
                'severity': 'critical',
                'description': 'Suicide plan reported',
                'action': 'Immediate psychiatric evaluation',
                'contact': 'Emergency Services: 112'
            })
        
        # Severe functional impairment
        if responses.get('severity_function_001', 0) >= 4 or responses.get('severity_social_001', 0) >= 4:
            crisis_flags.append({
                'type': 'severe_impairment',
                'severity': 'moderate',
                'description': 'Extreme functional impairment',
                'action': 'Urgent clinical evaluation',
                'contact': 'Mental health professional'
            })
        
        return crisis_flags
    
    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate evidence-based recommendations"""
        
        recommendations = []
        domain_scores = analysis_results['domain_scores']
        severity_assessments = analysis_results['severity_assessments']
        
        # Depression recommendations
        if 'depression' in domain_scores and domain_scores['depression'] > 20:
            severity = severity_assessments['depression']['level']
            if severity in ['moderate', 'severe', 'very_severe']:
                recommendations.append({
                    'type': 'treatment',
                    'priority': 'high',
                    'intervention': 'Cognitive Behavioral Therapy (CBT)',
                    'evidence_level': 'Grade A',
                    'description': 'CBT is first-line treatment for moderate to severe depression',
                    'indian_availability': 'Available through NIMHANS network and private practitioners'
                })
                
                if severity in ['severe', 'very_severe']:
                    recommendations.append({
                        'type': 'medication',
                        'priority': 'high',
                        'intervention': 'Antidepressant medication evaluation',
                        'evidence_level': 'Grade A',
                        'description': 'SSRIs or SNRIs for severe depression',
                        'indian_availability': 'Available through psychiatrists in public and private sectors'
                    })
        
        # Anxiety recommendations
        if 'anxiety' in domain_scores and domain_scores['anxiety'] > 25:
            recommendations.append({
                'type': 'treatment',
                'priority': 'high',
                'intervention': 'Exposure and Response Prevention',
                'evidence_level': 'Grade A',
                'description': 'Evidence-based treatment for anxiety disorders',
                'indian_availability': 'Specialized anxiety clinics in major cities'
            })
        
        # Lifestyle recommendations
        if any(score > 30 for score in domain_scores.values()):
            recommendations.extend([
                {
                    'type': 'lifestyle',
                    'priority': 'moderate',
                    'intervention': 'Regular exercise program',
                    'evidence_level': 'Grade B',
                    'description': '30 minutes of moderate exercise, 5 days per week',
                    'indian_availability': 'Yoga and walking groups widely available'
                },
                {
                    'type': 'lifestyle',
                    'priority': 'moderate',
                    'intervention': 'Mindfulness and meditation',
                    'evidence_level': 'Grade B',
                    'description': 'Daily mindfulness practice for stress reduction',
                    'indian_availability': 'Traditional practices widely available, apps in local languages'
                }
            ])
        
        # Crisis recommendations
        if analysis_results['crisis_flags']:
            recommendations.insert(0, {
                'type': 'crisis',
                'priority': 'critical',
                'intervention': 'Immediate crisis intervention',
                'evidence_level': 'Clinical Standard',
                'description': 'Contact crisis helpline or emergency services',
                'indian_availability': 'Tele MANAS 24/7 helpline: 1800-891-4416'
            })
        
        return recommendations
    
    def _determine_next_steps(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Determine appropriate next steps based on assessment"""
        
        next_steps = []
        
        # Crisis response
        if analysis_results['crisis_flags']:
            next_steps.append({
                'step': 'Emergency Response',
                'timeline': 'Immediate',
                'action': 'Contact crisis support services',
                'contact': 'Tele MANAS: 1800-891-4416, Emergency: 112',
                'priority': 1
            })
        
        # Professional evaluation
        high_severity_domains = [
            domain for domain, assessment in analysis_results['severity_assessments'].items()
            if assessment['level'] in ['severe', 'very_severe']
        ]
        
        if high_severity_domains:
            next_steps.append({
                'step': 'Professional Evaluation',
                'timeline': 'Within 1 week',
                'action': 'Schedule appointment with mental health professional',
                'contact': 'NIMHANS helpline: 080-26995000',
                'priority': 2
            })
        
        # Moderate intervention
        moderate_severity_domains = [
            domain for domain, assessment in analysis_results['severity_assessments'].items()
            if assessment['level'] == 'moderate'
        ]
        
        if moderate_severity_domains and not high_severity_domains:
            next_steps.append({
                'step': 'Counseling Services',
                'timeline': 'Within 2 weeks',
                'action': 'Begin counseling or therapy',
                'contact': 'Local mental health centers, private practitioners',
                'priority': 3
            })
        
        # Self-care and monitoring
        if any(score > 15 for score in analysis_results['domain_scores'].values()):
            next_steps.append({
                'step': 'Self-Care Plan',
                'timeline': 'Start immediately',
                'action': 'Implement stress management and self-care strategies',
                'contact': 'Mental health apps, support groups',
                'priority': 4
            })
        
        # Follow-up assessment
        next_steps.append({
            'step': 'Follow-up Assessment',
            'timeline': '2-4 weeks',
            'action': 'Retake assessment to monitor progress',
            'contact': 'This platform or healthcare provider',
            'priority': 5
        })
        
        return sorted(next_steps, key=lambda x: x['priority'])
    
    def get_specialized_assessment(self, condition_id: str) -> List[Dict[str, Any]]:
        """Get specialized assessment questions for specific conditions"""
        
        condition = self.conditions_db.get_condition_by_id(condition_id)
        if not condition:
            return []
        
        # Condition-specific question sets
        specialized_questions = {
            'gad_001': [  # Generalized Anxiety Disorder
                {
                    'id': 'gad_spec_001',
                    'text': 'Do you worry excessively about multiple areas of your life?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 4,
                    'scale_labels': ['Never', 'Rarely', 'Sometimes', 'Often', 'Always']
                },
                {
                    'id': 'gad_spec_002',
                    'text': 'How difficult is it for you to control your worrying?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 4,
                    'scale_labels': ['Very easy', 'Easy', 'Moderate', 'Difficult', 'Very difficult']
                }
            ],
            'mdd_001': [  # Major Depressive Disorder
                {
                    'id': 'mdd_spec_001',
                    'text': 'Have you experienced a period of at least 2 weeks when you felt depressed most of the day, nearly every day?',
                    'type': 'multiple_choice',
                    'options': ['No', 'Yes, once', 'Yes, multiple times']
                },
                {
                    'id': 'mdd_spec_002',
                    'text': 'During your most depressed period, how much did it interfere with your ability to work, study, or manage daily activities?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 4,
                    'scale_labels': ['Not at all', 'Slightly', 'Moderately', 'Considerably', 'Extremely']
                }
            ]
        }
        
        return specialized_questions.get(condition_id, [])
    
    def calculate_comorbidity_risk(self, domain_scores: Dict[str, float]) -> Dict[str, Any]:
        """Calculate risk of comorbid conditions"""
        
        comorbidity_patterns = {
            'depression_anxiety': {
                'conditions': ['depression', 'anxiety'],
                'threshold': 30,
                'risk_multiplier': 1.5,
                'prevalence': 0.6  # 60% comorbidity rate
            },
            'anxiety_substance': {
                'conditions': ['anxiety', 'substance_use'],
                'threshold': 25,
                'risk_multiplier': 1.3,
                'prevalence': 0.3
            },
            'depression_sleep': {
                'conditions': ['depression', 'sleep'],
                'threshold': 35,
                'risk_multiplier': 1.4,
                'prevalence': 0.8
            },
            'trauma_depression': {
                'conditions': ['trauma', 'depression'],
                'threshold': 30,
                'risk_multiplier': 1.6,
                'prevalence': 0.5
            }
        }
        
        comorbidity_risks = {}
        
        for pattern_name, pattern_info in comorbidity_patterns.items():
            conditions = pattern_info['conditions']
            threshold = pattern_info['threshold']
            
            # Check if both conditions exceed threshold
            if all(domain_scores.get(condition, 0) > threshold for condition in conditions):
                risk_score = min(100, max(domain_scores.get(condition, 0) for condition in conditions) * pattern_info['risk_multiplier'])
                
                comorbidity_risks[pattern_name] = {
                    'conditions_involved': conditions,
                    'risk_score': risk_score,
                    'prevalence': pattern_info['prevalence'],
                    'recommendation': f'Comprehensive assessment for {" and ".join(conditions)} needed'
                }
        
        return comorbidity_risks
