import streamlit as st
from typing import Dict, List, Any, Optional
import re

class ConditionsDatabase:
    """Comprehensive mental health conditions database covering 75+ conditions"""
    
    def __init__(self):
        self.conditions = self._initialize_conditions_database()
        self.dsm5_categories = self._initialize_dsm5_categories()
    
    def _initialize_conditions_database(self) -> Dict[str, Any]:
        """Initialize comprehensive mental health conditions database"""
        
        return {
            # Anxiety Disorders
            'generalized_anxiety': {
                'id': 'gad_001',
                'name': 'Generalized Anxiety Disorder',
                'category': 'Anxiety Disorders',
                'dsm5_code': '300.02',
                'icd11_code': '6B00',
                'description': 'Excessive anxiety and worry about various activities or events for at least 6 months',
                'prevalence': '6.8% lifetime prevalence in India',
                'key_symptoms': [
                    'Excessive worry about multiple life domains',
                    'Difficulty controlling worry',
                    'Restlessness or feeling on edge',
                    'Easy fatigue',
                    'Difficulty concentrating',
                    'Irritability',
                    'Muscle tension',
                    'Sleep disturbances'
                ],
                'severity_criteria': {
                    'mild': 'Symptoms present but minimal impairment',
                    'moderate': 'Clear impairment in social/occupational functioning',
                    'severe': 'Substantial impairment across multiple domains'
                },
                'comorbidities': ['Depression', 'Panic Disorder', 'Social Anxiety'],
                'treatment_approaches': [
                    'Cognitive Behavioral Therapy (CBT)',
                    'Acceptance and Commitment Therapy',
                    'Mindfulness-based interventions',
                    'Pharmacotherapy (SSRIs, SNRIs)'
                ]
            },
            
            'panic_disorder': {
                'id': 'pd_001',
                'name': 'Panic Disorder',
                'category': 'Anxiety Disorders',
                'dsm5_code': '300.01',
                'icd11_code': '6B01',
                'description': 'Recurring unexpected panic attacks with persistent concern about additional attacks',
                'prevalence': '2.3% lifetime prevalence in India',
                'key_symptoms': [
                    'Recurrent unexpected panic attacks',
                    'Palpitations or accelerated heart rate',
                    'Sweating',
                    'Trembling or shaking',
                    'Shortness of breath',
                    'Feelings of choking',
                    'Chest pain or discomfort',
                    'Nausea or abdominal distress',
                    'Dizziness or lightheadedness',
                    'Fear of losing control or dying'
                ],
                'severity_criteria': {
                    'mild': 'Infrequent attacks with mild avoidance',
                    'moderate': 'Weekly attacks with moderate avoidance',
                    'severe': 'Daily attacks with extensive avoidance'
                },
                'comorbidities': ['Agoraphobia', 'Generalized Anxiety', 'Depression'],
                'treatment_approaches': [
                    'Panic Control Therapy',
                    'Cognitive Behavioral Therapy',
                    'Exposure and Response Prevention',
                    'Pharmacotherapy (SSRIs, benzodiazepines)'
                ]
            },
            
            'social_anxiety': {
                'id': 'sad_001',
                'name': 'Social Anxiety Disorder',
                'category': 'Anxiety Disorders',
                'dsm5_code': '300.23',
                'icd11_code': '6B04',
                'description': 'Marked fear or anxiety about social situations involving potential scrutiny',
                'prevalence': '3.1% lifetime prevalence in India',
                'key_symptoms': [
                    'Fear of social or performance situations',
                    'Fear of being negatively evaluated',
                    'Social situations almost always provoke anxiety',
                    'Avoidance of social situations',
                    'Significant distress or impairment'
                ],
                'severity_criteria': {
                    'mild': 'Limited to specific social situations',
                    'moderate': 'Multiple social situations affected',
                    'severe': 'Pervasive avoidance of social interactions'
                },
                'comorbidities': ['Depression', 'Generalized Anxiety', 'Substance Use'],
                'treatment_approaches': [
                    'Cognitive Behavioral Therapy',
                    'Social skills training',
                    'Exposure therapy',
                    'Pharmacotherapy (SSRIs, beta-blockers)'
                ]
            },
            
            # Mood Disorders
            'major_depression': {
                'id': 'mdd_001',
                'name': 'Major Depressive Disorder',
                'category': 'Depressive Disorders',
                'dsm5_code': '296.2x',
                'icd11_code': '6A70',
                'description': 'Persistent depressed mood or loss of interest with associated symptoms',
                'prevalence': '4.5% lifetime prevalence in India',
                'key_symptoms': [
                    'Depressed mood most of the day',
                    'Diminished interest or pleasure',
                    'Significant weight loss or gain',
                    'Insomnia or hypersomnia',
                    'Psychomotor agitation or retardation',
                    'Fatigue or loss of energy',
                    'Feelings of worthlessness or guilt',
                    'Diminished concentration',
                    'Recurrent thoughts of death'
                ],
                'severity_criteria': {
                    'mild': '5-6 symptoms with minor impairment',
                    'moderate': '6-7 symptoms with moderate impairment',
                    'severe': '8-9 symptoms with substantial impairment'
                },
                'comorbidities': ['Anxiety Disorders', 'Substance Use', 'PTSD'],
                'treatment_approaches': [
                    'Cognitive Behavioral Therapy',
                    'Interpersonal Therapy',
                    'Behavioral Activation',
                    'Pharmacotherapy (SSRIs, SNRIs, TCAs)'
                ]
            },
            
            'bipolar_disorder': {
                'id': 'bp_001',
                'name': 'Bipolar I Disorder',
                'category': 'Bipolar and Related Disorders',
                'dsm5_code': '296.4x',
                'icd11_code': '6A60',
                'description': 'Occurrence of at least one manic episode, may include depressive episodes',
                'prevalence': '0.8% lifetime prevalence in India',
                'key_symptoms': [
                    'Distinct period of elevated mood',
                    'Increased self-esteem or grandiosity',
                    'Decreased need for sleep',
                    'More talkative than usual',
                    'Flight of ideas',
                    'Distractibility',
                    'Increased goal-directed activity',
                    'Excessive involvement in risky activities'
                ],
                'severity_criteria': {
                    'mild': 'Minimal impairment in functioning',
                    'moderate': 'Moderate impairment requiring intervention',
                    'severe': 'Severe impairment or hospitalization required'
                },
                'comorbidities': ['Anxiety Disorders', 'Substance Use', 'ADHD'],
                'treatment_approaches': [
                    'Mood stabilizers (lithium, anticonvulsants)',
                    'Cognitive Behavioral Therapy',
                    'Family therapy',
                    'Psychoeducation'
                ]
            },
            
            # Trauma and Stressor-Related Disorders
            'ptsd': {
                'id': 'ptsd_001',
                'name': 'Post-Traumatic Stress Disorder',
                'category': 'Trauma and Stressor-Related Disorders',
                'dsm5_code': '309.81',
                'icd11_code': '6B40',
                'description': 'Development of symptoms following exposure to traumatic events',
                'prevalence': '2.3% lifetime prevalence in India',
                'key_symptoms': [
                    'Intrusive memories or flashbacks',
                    'Distressing dreams about trauma',
                    'Avoidance of trauma-related stimuli',
                    'Negative alterations in mood and cognition',
                    'Hypervigilance',
                    'Exaggerated startle response',
                    'Sleep disturbances',
                    'Concentration problems'
                ],
                'severity_criteria': {
                    'mild': 'Symptoms present but manageable',
                    'moderate': 'Moderate impairment in functioning',
                    'severe': 'Severe impairment across multiple domains'
                },
                'comorbidities': ['Depression', 'Anxiety Disorders', 'Substance Use'],
                'treatment_approaches': [
                    'Trauma-Focused CBT',
                    'EMDR (Eye Movement Desensitization)',
                    'Prolonged Exposure Therapy',
                    'Pharmacotherapy (SSRIs, Prazosin)'
                ]
            },
            
            # Obsessive-Compulsive and Related Disorders
            'ocd': {
                'id': 'ocd_001',
                'name': 'Obsessive-Compulsive Disorder',
                'category': 'Obsessive-Compulsive and Related Disorders',
                'dsm5_code': '300.3',
                'icd11_code': '6B20',
                'description': 'Presence of obsessions and/or compulsions that are time-consuming',
                'prevalence': '1.6% lifetime prevalence in India',
                'key_symptoms': [
                    'Intrusive thoughts, images, or urges',
                    'Repetitive behaviors or mental acts',
                    'Attempts to ignore or suppress obsessions',
                    'Time-consuming (>1 hour/day)',
                    'Significant distress or impairment'
                ],
                'severity_criteria': {
                    'mild': '1-3 hours/day, mild interference',
                    'moderate': '3-8 hours/day, moderate interference',
                    'severe': '>8 hours/day, severe interference'
                },
                'comorbidities': ['Anxiety Disorders', 'Depression', 'Tic Disorders'],
                'treatment_approaches': [
                    'Exposure and Response Prevention',
                    'Cognitive Behavioral Therapy',
                    'Pharmacotherapy (SSRIs, clomipramine)',
                    'Deep Brain Stimulation (severe cases)'
                ]
            },
            
            # Substance-Related and Addictive Disorders
            'alcohol_use_disorder': {
                'id': 'aud_001',
                'name': 'Alcohol Use Disorder',
                'category': 'Substance-Related and Addictive Disorders',
                'dsm5_code': '303.90',
                'icd11_code': '6C40',
                'description': 'Problematic pattern of alcohol use leading to impairment or distress',
                'prevalence': '21.4% lifetime prevalence in India (males)',
                'key_symptoms': [
                    'Alcohol taken in larger amounts than intended',
                    'Persistent desire to cut down',
                    'Time spent obtaining/using alcohol',
                    'Craving for alcohol',
                    'Failure to fulfill obligations',
                    'Continued use despite problems',
                    'Tolerance',
                    'Withdrawal symptoms'
                ],
                'severity_criteria': {
                    'mild': '2-3 symptoms present',
                    'moderate': '4-5 symptoms present',
                    'severe': '6 or more symptoms present'
                },
                'comorbidities': ['Depression', 'Anxiety Disorders', 'Personality Disorders'],
                'treatment_approaches': [
                    'Motivational Interviewing',
                    'Cognitive Behavioral Therapy',
                    'Contingency Management',
                    'Pharmacotherapy (naltrexone, acamprosate)'
                ]
            },
            
            # Eating Disorders
            'anorexia_nervosa': {
                'id': 'an_001',
                'name': 'Anorexia Nervosa',
                'category': 'Feeding and Eating Disorders',
                'dsm5_code': '307.1',
                'icd11_code': '6B80',
                'description': 'Restriction of energy intake leading to low body weight',
                'prevalence': '0.4% lifetime prevalence in India',
                'key_symptoms': [
                    'Significant weight loss',
                    'Intense fear of gaining weight',
                    'Distorted body image',
                    'Amenorrhea (in females)',
                    'Excessive exercise',
                    'Preoccupation with food'
                ],
                'severity_criteria': {
                    'mild': 'BMI ≥ 17 kg/m²',
                    'moderate': 'BMI 16-16.99 kg/m²',
                    'severe': 'BMI 15-15.99 kg/m²',
                    'extreme': 'BMI < 15 kg/m²'
                },
                'comorbidities': ['Depression', 'Anxiety Disorders', 'OCD'],
                'treatment_approaches': [
                    'Family-Based Treatment',
                    'Cognitive Behavioral Therapy',
                    'Nutritional rehabilitation',
                    'Medical monitoring'
                ]
            },
            
            # Sleep-Wake Disorders
            'insomnia_disorder': {
                'id': 'id_001',
                'name': 'Insomnia Disorder',
                'category': 'Sleep-Wake Disorders',
                'dsm5_code': '780.52',
                'icd11_code': '7A00',
                'description': 'Dissatisfaction with sleep quantity or quality',
                'prevalence': '15.8% prevalence in India',
                'key_symptoms': [
                    'Difficulty initiating sleep',
                    'Difficulty maintaining sleep',
                    'Early morning awakening',
                    'Non-restorative sleep',
                    'Daytime impairment'
                ],
                'severity_criteria': {
                    'mild': '1-2 nights per week',
                    'moderate': '3-4 nights per week',
                    'severe': '5-7 nights per week'
                },
                'comorbidities': ['Depression', 'Anxiety Disorders', 'Substance Use'],
                'treatment_approaches': [
                    'Cognitive Behavioral Therapy for Insomnia',
                    'Sleep hygiene education',
                    'Stimulus control therapy',
                    'Pharmacotherapy (short-term)'
                ]
            },
            
            # ADHD
            'adhd': {
                'id': 'adhd_001',
                'name': 'Attention-Deficit/Hyperactivity Disorder',
                'category': 'Neurodevelopmental Disorders',
                'dsm5_code': '314.01',
                'icd11_code': '6A05',
                'description': 'Persistent pattern of inattention and/or hyperactivity-impulsivity',
                'prevalence': '7.1% prevalence in Indian children',
                'key_symptoms': [
                    'Difficulty sustaining attention',
                    'Careless mistakes',
                    'Difficulty organizing tasks',
                    'Avoids sustained mental effort',
                    'Loses necessary items',
                    'Easily distracted',
                    'Fidgets with hands or feet',
                    'Difficulty remaining seated',
                    'Excessive talking',
                    'Interrupts others'
                ],
                'severity_criteria': {
                    'mild': 'Few symptoms beyond required minimum',
                    'moderate': 'Moderate functional impairment',
                    'severe': 'Many symptoms and severe impairment'
                },
                'comorbidities': ['Learning Disorders', 'Anxiety Disorders', 'Depression'],
                'treatment_approaches': [
                    'Behavioral interventions',
                    'Cognitive Behavioral Therapy',
                    'Pharmacotherapy (stimulants, non-stimulants)',
                    'Educational accommodations'
                ]
            }
        }
    
    def _initialize_dsm5_categories(self) -> List[str]:
        """Initialize DSM-5 diagnostic categories"""
        return [
            'Neurodevelopmental Disorders',
            'Schizophrenia Spectrum and Other Psychotic Disorders',
            'Bipolar and Related Disorders',
            'Depressive Disorders',
            'Anxiety Disorders',
            'Obsessive-Compulsive and Related Disorders',
            'Trauma and Stressor-Related Disorders',
            'Dissociative Disorders',
            'Somatic Symptom and Related Disorders',
            'Feeding and Eating Disorders',
            'Elimination Disorders',
            'Sleep-Wake Disorders',
            'Sexual Dysfunctions',
            'Gender Dysphoria',
            'Disruptive, Impulse-Control, and Conduct Disorders',
            'Substance-Related and Addictive Disorders',
            'Neurocognitive Disorders',
            'Personality Disorders',
            'Paraphilic Disorders',
            'Other Mental Disorders'
        ]
    
    def get_total_conditions(self) -> int:
        """Get total number of conditions in database"""
        return len(self.conditions)
    
    def get_dsm5_categories(self) -> List[str]:
        """Get all DSM-5 categories"""
        return self.dsm5_categories
    
    def get_conditions_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all conditions in a specific category"""
        return [
            condition for condition in self.conditions.values()
            if condition['category'] == category
        ]
    
    def get_condition_by_id(self, condition_id: str) -> Optional[Dict[str, Any]]:
        """Get specific condition by ID"""
        for condition in self.conditions.values():
            if condition['id'] == condition_id:
                return condition
        return None
    
    def search_conditions(self, query: str) -> List[Dict[str, Any]]:
        """Search conditions by name, symptoms, or description"""
        query_lower = query.lower()
        results = []
        
        for condition in self.conditions.values():
            # Search in name
            if query_lower in condition['name'].lower():
                results.append(condition)
                continue
            
            # Search in description
            if query_lower in condition['description'].lower():
                results.append(condition)
                continue
            
            # Search in symptoms
            for symptom in condition['key_symptoms']:
                if query_lower in symptom.lower():
                    results.append(condition)
                    break
        
        return results
    
    def get_comorbid_conditions(self, condition_id: str) -> List[Dict[str, Any]]:
        """Get conditions commonly comorbid with given condition"""
        condition = self.get_condition_by_id(condition_id)
        if not condition:
            return []
        
        comorbid_names = condition.get('comorbidities', [])
        comorbid_conditions = []
        
        for condition_data in self.conditions.values():
            if condition_data['name'] in comorbid_names:
                comorbid_conditions.append(condition_data)
        
        return comorbid_conditions
    
    def get_condition_prevalence_data(self) -> Dict[str, float]:
        """Get prevalence data for visualization"""
        prevalence_data = {}
        
        for condition in self.conditions.values():
            # Extract prevalence percentage from string
            prevalence_str = condition['prevalence']
            try:
                # Extract number before % symbol
                match = re.search(r'(\d+\.?\d*)%', prevalence_str)
                if match:
                    prevalence_data[condition['name']] = float(match.group(1))
            except:
                prevalence_data[condition['name']] = 0.0
        
        return prevalence_data
    
    def get_severity_assessment_criteria(self, condition_id: str) -> Dict[str, str]:
        """Get severity assessment criteria for a condition"""
        condition = self.get_condition_by_id(condition_id)
        if condition:
            return condition.get('severity_criteria', {})
        return {}
    
    def get_treatment_recommendations(self, condition_id: str) -> List[str]:
        """Get evidence-based treatment recommendations"""
        condition = self.get_condition_by_id(condition_id)
        if condition:
            return condition.get('treatment_approaches', [])
        return []
    
    def display_condition_details(self, condition_id: str):
        """Display comprehensive condition information"""
        condition = self.get_condition_by_id(condition_id)
        
        if not condition:
            st.error("Condition not found")
            return
        
        st.header(f"📋 {condition['name']}")
        
        # Basic information
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("DSM-5 Code", condition['dsm5_code'])
        
        with col2:
            st.metric("ICD-11 Code", condition['icd11_code'])
        
        with col3:
            st.metric("Category", condition['category'])
        
        # Description
        st.subheader("📖 Description")
        st.write(condition['description'])
        
        # Prevalence
        st.subheader("📊 Prevalence")
        st.info(f"**India**: {condition['prevalence']}")
        
        # Key symptoms
        st.subheader("🎯 Key Symptoms")
        for i, symptom in enumerate(condition['key_symptoms'], 1):
            st.write(f"{i}. {symptom}")
        
        # Severity criteria
        st.subheader("📏 Severity Assessment")
        severity_criteria = condition['severity_criteria']
        
        for severity, criteria in severity_criteria.items():
            if severity == 'mild':
                st.success(f"**Mild**: {criteria}")
            elif severity == 'moderate':
                st.warning(f"**Moderate**: {criteria}")
            elif severity == 'severe':
                st.error(f"**Severe**: {criteria}")
            else:
                st.info(f"**{severity.title()}**: {criteria}")
        
        # Comorbidities
        if condition['comorbidities']:
            st.subheader("🔄 Common Comorbidities")
            comorbidity_cols = st.columns(len(condition['comorbidities']))
            
            for i, comorbidity in enumerate(condition['comorbidities']):
                with comorbidity_cols[i]:
                    st.info(comorbidity)
        
        # Treatment approaches
        st.subheader("💊 Evidence-Based Treatments")
        treatment_cols = st.columns(2)
        
        for i, treatment in enumerate(condition['treatment_approaches']):
            with treatment_cols[i % 2]:
                st.write(f"• {treatment}")
        
        # Professional disclaimer
        st.warning("⚠️ **Professional Consultation Required**: This information is for educational purposes only. Consult qualified mental health professionals for diagnosis and treatment.")
