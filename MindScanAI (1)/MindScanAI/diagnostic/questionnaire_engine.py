import streamlit as st
from typing import Dict, List, Any, Optional
import random

class QuestionnaireEngine:
    """Intelligent questionnaire engine for mental health assessments"""
    
    def __init__(self):
        self.question_banks = self._initialize_question_banks()
        self.adaptive_algorithms = self._initialize_adaptive_algorithms()
    
    def _initialize_question_banks(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize comprehensive question banks for different assessments"""
        
        return {
            'general_screening': [
                {
                    'id': 'gen_001',
                    'text': 'Over the past 2 weeks, how often have you been bothered by feeling down, depressed, or hopeless?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 3,
                    'scale_labels': ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
                    'domain': 'depression',
                    'weight': 0.8,
                    'follow_up_threshold': 2
                },
                {
                    'id': 'gen_002',
                    'text': 'Over the past 2 weeks, how often have you been bothered by little interest or pleasure in doing things?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 3,
                    'scale_labels': ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
                    'domain': 'depression',
                    'weight': 0.8,
                    'follow_up_threshold': 2
                },
                {
                    'id': 'gen_003',
                    'text': 'Over the past 2 weeks, how often have you been bothered by feeling nervous, anxious, or on edge?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 3,
                    'scale_labels': ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
                    'domain': 'anxiety',
                    'weight': 0.7,
                    'follow_up_threshold': 2
                },
                {
                    'id': 'gen_004',
                    'text': 'Over the past 2 weeks, how often have you been bothered by not being able to stop or control worrying?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 3,
                    'scale_labels': ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
                    'domain': 'anxiety',
                    'weight': 0.7,
                    'follow_up_threshold': 2
                },
                {
                    'id': 'gen_005',
                    'text': 'During the past month, how often have you felt that you were unable to control the important things in your life?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 4,
                    'scale_labels': ['Never', 'Almost never', 'Sometimes', 'Fairly often', 'Very often'],
                    'domain': 'stress',
                    'weight': 0.6,
                    'follow_up_threshold': 3
                },
                {
                    'id': 'gen_006',
                    'text': 'How often during the past month have you felt confident about your ability to handle your personal problems?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 4,
                    'scale_labels': ['Never', 'Almost never', 'Sometimes', 'Fairly often', 'Very often'],
                    'domain': 'coping',
                    'weight': 0.5,
                    'follow_up_threshold': 2,
                    'reverse_scored': True
                }
            ],
            
            'anxiety_screening': [
                {
                    'id': 'anx_001',
                    'text': 'In the last month, how often have you experienced sudden feelings of terror or panic?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 4,
                    'scale_labels': ['Never', 'Rarely', 'Sometimes', 'Often', 'Very often'],
                    'domain': 'panic',
                    'weight': 0.9,
                    'follow_up_threshold': 2
                },
                {
                    'id': 'anx_002',
                    'text': 'How often do you avoid social situations because you fear being judged or embarrassed?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 4,
                    'scale_labels': ['Never', 'Rarely', 'Sometimes', 'Often', 'Very often'],
                    'domain': 'social_anxiety',
                    'weight': 0.8,
                    'follow_up_threshold': 2
                },
                {
                    'id': 'anx_003',
                    'text': 'Do you experience repetitive, unwanted thoughts that you cannot get out of your mind?',
                    'type': 'multiple_choice',
                    'options': ['Never', 'Rarely', 'Sometimes', 'Often', 'Always'],
                    'domain': 'obsessions',
                    'weight': 0.7,
                    'follow_up_threshold': 2
                },
                {
                    'id': 'anx_004',
                    'text': 'Which physical symptoms do you experience when anxious? (Select all that apply)',
                    'type': 'checkbox',
                    'options': [
                        'Rapid heartbeat or palpitations',
                        'Sweating or trembling',
                        'Shortness of breath',
                        'Chest pain or tightness',
                        'Nausea or stomach upset',
                        'Dizziness or lightheadedness',
                        'Muscle tension',
                        'None of the above'
                    ],
                    'domain': 'somatic_anxiety',
                    'weight': 0.6
                },
                {
                    'id': 'anx_005',
                    'text': 'How much do your anxiety symptoms interfere with your daily life?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 4,
                    'scale_labels': ['Not at all', 'Slightly', 'Moderately', 'Considerably', 'Extremely'],
                    'domain': 'functional_impairment',
                    'weight': 0.9,
                    'follow_up_threshold': 2
                }
            ],
            
            'depression_screening': [
                {
                    'id': 'dep_001',
                    'text': 'Over the past 2 weeks, how often have you had trouble falling or staying asleep, or sleeping too much?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 3,
                    'scale_labels': ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
                    'domain': 'sleep',
                    'weight': 0.7,
                    'follow_up_threshold': 2
                },
                {
                    'id': 'dep_002',
                    'text': 'Over the past 2 weeks, how often have you had little energy or felt tired?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 3,
                    'scale_labels': ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
                    'domain': 'energy',
                    'weight': 0.8,
                    'follow_up_threshold': 2
                },
                {
                    'id': 'dep_003',
                    'text': 'Over the past 2 weeks, how often have you had poor appetite or been overeating?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 3,
                    'scale_labels': ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
                    'domain': 'appetite',
                    'weight': 0.6,
                    'follow_up_threshold': 2
                },
                {
                    'id': 'dep_004',
                    'text': 'Over the past 2 weeks, how often have you felt bad about yourself or that you are a failure?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 3,
                    'scale_labels': ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
                    'domain': 'self_worth',
                    'weight': 0.8,
                    'follow_up_threshold': 2
                },
                {
                    'id': 'dep_005',
                    'text': 'Over the past 2 weeks, how often have you had thoughts that you would be better off dead or of hurting yourself?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 3,
                    'scale_labels': ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
                    'domain': 'suicidality',
                    'weight': 1.0,
                    'follow_up_threshold': 1,
                    'crisis_indicator': True
                }
            ],
            
            'trauma_screening': [
                {
                    'id': 'trauma_001',
                    'text': 'Have you ever experienced or witnessed a life-threatening event?',
                    'type': 'multiple_choice',
                    'options': ['No', 'Yes, once', 'Yes, multiple times', 'Prefer not to answer'],
                    'domain': 'trauma_exposure',
                    'weight': 0.8,
                    'follow_up_threshold': 1
                },
                {
                    'id': 'trauma_002',
                    'text': 'Do you have repeated, disturbing memories or dreams about a stressful experience?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 4,
                    'scale_labels': ['Never', 'Rarely', 'Sometimes', 'Often', 'Very often'],
                    'domain': 'intrusions',
                    'weight': 0.9,
                    'follow_up_threshold': 2
                },
                {
                    'id': 'trauma_003',
                    'text': 'Do you avoid activities, places, or people that remind you of a stressful experience?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 4,
                    'scale_labels': ['Never', 'Rarely', 'Sometimes', 'Often', 'Very often'],
                    'domain': 'avoidance',
                    'weight': 0.8,
                    'follow_up_threshold': 2
                },
                {
                    'id': 'trauma_004',
                    'text': 'Are you constantly on guard, watchful, or easily startled?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 4,
                    'scale_labels': ['Never', 'Rarely', 'Sometimes', 'Often', 'Very often'],
                    'domain': 'hypervigilance',
                    'weight': 0.7,
                    'follow_up_threshold': 2
                }
            ],
            
            'substance_screening': [
                {
                    'id': 'sub_001',
                    'text': 'In the past year, have you had a drink containing alcohol?',
                    'type': 'multiple_choice',
                    'options': ['No', 'Yes'],
                    'domain': 'alcohol_use',
                    'weight': 0.5,
                    'screening_question': True
                },
                {
                    'id': 'sub_002',
                    'text': 'How often do you have a drink containing alcohol?',
                    'type': 'multiple_choice',
                    'options': [
                        'Never',
                        'Monthly or less',
                        '2-4 times a month',
                        '2-3 times a week',
                        '4 or more times a week'
                    ],
                    'domain': 'alcohol_frequency',
                    'weight': 0.7,
                    'conditional': {'sub_001': 'Yes'}
                },
                {
                    'id': 'sub_003',
                    'text': 'How many drinks containing alcohol do you have on a typical day when you are drinking?',
                    'type': 'multiple_choice',
                    'options': ['1 or 2', '3 or 4', '5 or 6', '7 to 9', '10 or more'],
                    'domain': 'alcohol_quantity',
                    'weight': 0.8,
                    'conditional': {'sub_001': 'Yes'}
                },
                {
                    'id': 'sub_004',
                    'text': 'In the past year, have you used any illegal drugs or prescription medications for non-medical reasons?',
                    'type': 'multiple_choice',
                    'options': ['No', 'Yes', 'Prefer not to answer'],
                    'domain': 'drug_use',
                    'weight': 0.8,
                    'follow_up_threshold': 1
                }
            ],
            
            'sleep_screening': [
                {
                    'id': 'sleep_001',
                    'text': 'How would you rate your sleep quality overall?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 3,
                    'scale_labels': ['Very good', 'Fairly good', 'Fairly bad', 'Very bad'],
                    'domain': 'sleep_quality',
                    'weight': 0.8,
                    'follow_up_threshold': 2
                },
                {
                    'id': 'sleep_002',
                    'text': 'How long does it usually take you to fall asleep each night?',
                    'type': 'multiple_choice',
                    'options': [
                        'Less than 15 minutes',
                        '15-30 minutes',
                        '31-60 minutes',
                        'More than 60 minutes'
                    ],
                    'domain': 'sleep_latency',
                    'weight': 0.7,
                    'follow_up_threshold': 2
                },
                {
                    'id': 'sleep_003',
                    'text': 'How often do you wake up during the night?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 3,
                    'scale_labels': ['Never', 'Less than once a week', 'Once or twice a week', 'Three or more times a week'],
                    'domain': 'sleep_maintenance',
                    'weight': 0.7,
                    'follow_up_threshold': 2
                },
                {
                    'id': 'sleep_004',
                    'text': 'How often do you feel tired or have little energy during the day?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 3,
                    'scale_labels': ['Never', 'Less than once a week', 'Once or twice a week', 'Three or more times a week'],
                    'domain': 'daytime_dysfunction',
                    'weight': 0.8,
                    'follow_up_threshold': 2
                }
            ]
        }
    
    def _initialize_adaptive_algorithms(self) -> Dict[str, Any]:
        """Initialize adaptive questioning algorithms"""
        return {
            'branching_logic': {
                'depression_followup': {
                    'trigger_conditions': ['dep_005 >= 1'],
                    'additional_questions': [
                        {
                            'id': 'crisis_001',
                            'text': 'Are you currently having thoughts of ending your life?',
                            'type': 'multiple_choice',
                            'options': ['No', 'Sometimes', 'Often', 'Right now'],
                            'crisis_indicator': True,
                            'immediate_intervention': True
                        }
                    ]
                },
                'anxiety_followup': {
                    'trigger_conditions': ['anx_001 >= 2'],
                    'additional_questions': [
                        {
                            'id': 'panic_detail_001',
                            'text': 'During these panic episodes, how long do they typically last?',
                            'type': 'multiple_choice',
                            'options': ['Less than 5 minutes', '5-10 minutes', '10-30 minutes', 'More than 30 minutes']
                        }
                    ]
                }
            },
            'severity_escalation': {
                'thresholds': {
                    'mild': {'score_range': [0, 33], 'followup_questions': 2},
                    'moderate': {'score_range': [34, 66], 'followup_questions': 4},
                    'severe': {'score_range': [67, 100], 'followup_questions': 6}
                }
            }
        }
    
    def get_basic_questions(self, assessment_type: str) -> List[Dict[str, Any]]:
        """Get basic questions for assessment type"""
        
        assessment_map = {
            'General Mental Health Screening': 'general_screening',
            'Anxiety Disorders Screening': 'anxiety_screening',
            'Depression Screening': 'depression_screening',
            'Stress & Trauma Assessment': 'trauma_screening',
            'Substance Use Screening': 'substance_screening',
            'Sleep Disorders Screening': 'sleep_screening'
        }
        
        question_key = assessment_map.get(assessment_type, 'general_screening')
        return self.question_banks.get(question_key, [])
    
    def generate_adaptive_questions(self, responses: Dict[str, Any], assessment_type: str) -> List[Dict[str, Any]]:
        """Generate additional questions based on responses"""
        additional_questions = []
        
        # Check for crisis indicators
        crisis_questions = self._check_crisis_indicators(responses)
        if crisis_questions:
            additional_questions.extend(crisis_questions)
        
        # Check branching logic
        branching_questions = self._apply_branching_logic(responses)
        if branching_questions:
            additional_questions.extend(branching_questions)
        
        # Add severity-based questions
        severity_questions = self._generate_severity_questions(responses, assessment_type)
        if severity_questions:
            additional_questions.extend(severity_questions)
        
        return additional_questions
    
    def _check_crisis_indicators(self, responses: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for responses indicating crisis situations"""
        crisis_questions = []
        
        # Check for suicidal ideation
        if responses.get('dep_005', 0) >= 1:
            crisis_questions.append({
                'id': 'crisis_suicide_001',
                'text': 'Are you currently having thoughts of ending your life?',
                'type': 'multiple_choice',
                'options': ['No', 'Sometimes', 'Often', 'Right now'],
                'crisis_indicator': True,
                'immediate_intervention': True
            })
            
            crisis_questions.append({
                'id': 'crisis_suicide_002',
                'text': 'Do you have a plan for how you would end your life?',
                'type': 'multiple_choice',
                'options': ['No', 'Vague thoughts', 'Specific plan', 'Detailed plan'],
                'crisis_indicator': True,
                'immediate_intervention': True
            })
        
        # Check for self-harm
        if any(response >= 2 for key, response in responses.items() 
               if key.startswith(('anx_', 'dep_')) and isinstance(response, (int, float))):
            crisis_questions.append({
                'id': 'crisis_harm_001',
                'text': 'Have you had thoughts of harming yourself in ways other than ending your life?',
                'type': 'multiple_choice',
                'options': ['Never', 'Rarely', 'Sometimes', 'Often'],
                'crisis_indicator': True
            })
        
        return crisis_questions
    
    def _apply_branching_logic(self, responses: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply branching logic based on responses"""
        additional_questions = []
        
        # Panic disorder followup
        if responses.get('anx_001', 0) >= 2:
            additional_questions.extend([
                {
                    'id': 'panic_freq_001',
                    'text': 'How often do you experience these panic attacks?',
                    'type': 'multiple_choice',
                    'options': ['Once a month', 'Weekly', 'Multiple times per week', 'Daily']
                },
                {
                    'id': 'panic_trigger_001',
                    'text': 'Do these panic attacks seem to be triggered by specific situations?',
                    'type': 'multiple_choice',
                    'options': ['No clear trigger', 'Social situations', 'Specific places', 'Physical sensations']
                }
            ])
        
        # OCD screening followup
        if responses.get('anx_003', 0) >= 2:
            additional_questions.append({
                'id': 'ocd_compulsion_001',
                'text': 'Do you feel compelled to perform certain behaviors repeatedly to reduce anxiety?',
                'type': 'multiple_choice',
                'options': ['Never', 'Sometimes', 'Often', 'Always']
            })
        
        # Substance use followup
        if responses.get('sub_001') == 'Yes':
            additional_questions.extend([
                {
                    'id': 'alcohol_problems_001',
                    'text': 'Have you ever felt you should cut down on your drinking?',
                    'type': 'multiple_choice',
                    'options': ['No', 'Yes']
                },
                {
                    'id': 'alcohol_problems_002',
                    'text': 'Have people annoyed you by criticizing your drinking?',
                    'type': 'multiple_choice',
                    'options': ['No', 'Yes']
                }
            ])
        
        return additional_questions
    
    def _generate_severity_questions(self, responses: Dict[str, Any], assessment_type: str) -> List[Dict[str, Any]]:
        """Generate severity-specific questions based on current responses"""
        severity_questions = []
        
        # Calculate preliminary severity
        severity_score = self._calculate_preliminary_severity(responses)
        
        if severity_score >= 70:  # High severity
            severity_questions.extend([
                {
                    'id': 'severity_function_001',
                    'text': 'How much do your symptoms interfere with your work or daily activities?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 4,
                    'scale_labels': ['Not at all', 'Slightly', 'Moderately', 'Considerably', 'Extremely']
                },
                {
                    'id': 'severity_social_001',
                    'text': 'How much do your symptoms interfere with your social relationships?',
                    'type': 'scale',
                    'scale_min': 0,
                    'scale_max': 4,
                    'scale_labels': ['Not at all', 'Slightly', 'Moderately', 'Considerably', 'Extremely']
                }
            ])
        
        return severity_questions
    
    def _calculate_preliminary_severity(self, responses: Dict[str, Any]) -> float:
        """Calculate preliminary severity score from responses"""
        total_score = 0
        max_possible = 0
        
        for question_id, response in responses.items():
            if isinstance(response, (int, float)):
                # Assume max score of 4 for most scales
                total_score += response
                max_possible += 4
        
        if max_possible == 0:
            return 0
        
        return (total_score / max_possible) * 100
    
    def validate_responses(self, responses: Dict[str, Any], questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate questionnaire responses"""
        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'missing_required': []
        }
        
        required_questions = [q for q in questions if q.get('required', True)]
        
        # Check for missing required responses
        for question in required_questions:
            if question['id'] not in responses:
                validation_results['missing_required'].append(question['id'])
                validation_results['valid'] = False
        
        # Check response validity
        for question in questions:
            if question['id'] in responses:
                response = responses[question['id']]
                
                if question['type'] == 'scale':
                    if not isinstance(response, (int, float)):
                        validation_results['errors'].append(f"Invalid response type for {question['id']}")
                        validation_results['valid'] = False
                    elif not (question['scale_min'] <= response <= question['scale_max']):
                        validation_results['errors'].append(f"Response out of range for {question['id']}")
                        validation_results['valid'] = False
                
                elif question['type'] == 'multiple_choice':
                    if response not in question['options']:
                        validation_results['errors'].append(f"Invalid option selected for {question['id']}")
                        validation_results['valid'] = False
                
                elif question['type'] == 'checkbox':
                    if not isinstance(response, list):
                        validation_results['errors'].append(f"Checkbox response must be a list for {question['id']}")
                        validation_results['valid'] = False
                    elif not all(option in question['options'] for option in response):
                        validation_results['errors'].append(f"Invalid options selected for {question['id']}")
                        validation_results['valid'] = False
        
        # Check for potential inconsistencies
        inconsistencies = self._check_response_consistency(responses)
        if inconsistencies:
            validation_results['warnings'].extend(inconsistencies)
        
        return validation_results
    
    def _check_response_consistency(self, responses: Dict[str, Any]) -> List[str]:
        """Check for inconsistent responses that may indicate attention issues"""
        warnings = []
        
        # Check for all extreme responses (potential response bias)
        scale_responses = [v for k, v in responses.items() if isinstance(v, (int, float))]
        if len(scale_responses) > 5:
            if all(r == scale_responses[0] for r in scale_responses):
                warnings.append("All scale responses are identical - please review your answers")
        
        # Check for contradictory responses
        if responses.get('gen_001', 0) == 0 and responses.get('dep_001', 0) >= 2:
            warnings.append("Some responses appear contradictory - please review")
        
        return warnings
    
    def get_question_statistics(self, assessment_type: str) -> Dict[str, Any]:
        """Get statistics about questions for an assessment type"""
        questions = self.get_basic_questions(assessment_type)
        
        stats = {
            'total_questions': len(questions),
            'question_types': {},
            'domains_covered': set(),
            'crisis_indicators': 0,
            'estimated_time_minutes': len(questions) * 0.5  # 30 seconds per question
        }
        
        for question in questions:
            # Count question types
            q_type = question['type']
            stats['question_types'][q_type] = stats['question_types'].get(q_type, 0) + 1
            
            # Collect domains
            if 'domain' in question:
                stats['domains_covered'].add(question['domain'])
            
            # Count crisis indicators
            if question.get('crisis_indicator', False):
                stats['crisis_indicators'] += 1
        
        stats['domains_covered'] = list(stats['domains_covered'])
        
        return stats
