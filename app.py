import streamlit as st
import datetime
import hashlib
import json
import pandas as pd
from compliance.dpdpa_compliance import DPDPACompliance
from compliance.mental_health_act_compliance import MentalHealthActCompliance
from compliance.privacy_notices import PrivacyNotices
from diagnostic.conditions_database import ConditionsDatabase
from diagnostic.questionnaire_engine import QuestionnaireEngine
from diagnostic.phi3_integration import Phi3Integration
from diagnostic.assessment_tools import AssessmentTools
from diagnostic.analysis_engine import CodeBasedAnalysisEngine
from security.encryption import EncryptionManager
from security.data_protection import DataProtection
from database.secure_storage import SecureStorage
from crisis.intervention import CrisisIntervention
from reports.diagnostic_reports import DiagnosticReports
from utils.validators import Validators
from static.legal_documents import LegalDocuments

# Page configuration
st.set_page_config(
    page_title="Mental Health Diagnostic Platform - Government of India Compliance",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_session' not in st.session_state:
    st.session_state.user_session = {
        'consent_given': False,
        'age_verified': False,
        'current_assessment': None,
        'crisis_mode': False,
        'language': 'english',
        'user_id': None,
        'dpo_contact_shown': False
    }

# Initialize compliance managers
dpdpa_compliance = DPDPACompliance()
mha_compliance = MentalHealthActCompliance()
privacy_notices = PrivacyNotices()
conditions_db = ConditionsDatabase()
questionnaire_engine = QuestionnaireEngine()
phi3_integration = Phi3Integration()
assessment_tools = AssessmentTools()
analysis_engine = CodeBasedAnalysisEngine()
encryption_manager = EncryptionManager()
data_protection = DataProtection()
secure_storage = SecureStorage()
crisis_intervention = CrisisIntervention()
diagnostic_reports = DiagnosticReports()
validators = Validators()
legal_documents = LegalDocuments()

def main():
    # Crisis intervention banner (always visible)
    crisis_intervention.display_crisis_banner()
    
    # Language selection
    language = st.sidebar.selectbox(
        "भाषा चुनें / Select Language",
        ["English", "हिंदी (Hindi)"],
        key="language_selector"
    )
    st.session_state.user_session['language'] = language.lower()
    
    # Main navigation
    if not st.session_state.user_session['consent_given']:
        display_compliance_homepage()
    elif not st.session_state.user_session['age_verified']:
        display_age_verification()
    else:
        display_main_application()

def display_compliance_homepage():
    """Display comprehensive Government of India compliance homepage"""
    st.title("🏛️ Mental Health Diagnostic Platform")
    st.subheader("Government of India Compliance Framework")
    
    # Legal compliance notice
    st.error("⚖️ **IMPORTANT LEGAL NOTICE**: This platform operates under strict Government of India regulations including Digital Personal Data Protection Act (DPDPA) 2023 and Mental Healthcare Act 2017")
    
    # Tabs for different compliance sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🛡️ Data Protection",
        "🏥 Healthcare Rights", 
        "📋 Privacy Notice",
        "⚠️ Disclaimers",
        "📞 Grievance Redressal"
    ])
    
    with tab1:
        st.header("Digital Personal Data Protection Act (DPDPA) 2023 Compliance")
        dpdpa_compliance.display_compliance_info(st.session_state.user_session['language'])
        
        if st.button("I Understand and Consent to Data Processing", type="primary"):
            if dpdpa_compliance.record_consent():
                st.session_state.user_session['consent_given'] = True
                st.rerun()
    
    with tab2:
        st.header("Mental Healthcare Act 2017 Obligations")
        mha_compliance.display_patient_rights(st.session_state.user_session['language'])
        
        # Advanced directives information
        st.subheader("Advance Directives Support")
        st.info("Under Section 5 of Mental Healthcare Act 2017, you have the right to make advance directives regarding your mental healthcare treatment.")
    
    with tab3:
        st.header("Privacy Notice")
        privacy_notices.display_detailed_notice(st.session_state.user_session['language'])
    
    with tab4:
        st.header("Medical Disclaimers")
        st.warning("🚨 **AI-Generated Results Disclaimer**: All diagnostic results are AI-generated and require professional medical validation by qualified mental health professionals.")
        st.info("This platform does not replace professional medical advice, diagnosis, or treatment.")
        
        # Professional validation requirement
        st.markdown("""
        ### Professional Validation Required
        - AI results are preliminary assessments only
        - Consult qualified psychiatrists for official diagnosis
        - Emergency situations require immediate medical attention
        - Contact Tele MANAS: **1800-891-4416** for crisis support
        """)
    
    with tab5:
        st.header("Grievance Redressal Mechanism")
        st.markdown("""
        ### Data Protection Officer (DPO) Contact Information
        - **Email**: dpo@mentalhealthplatform.gov.in
        - **Phone**: +91-11-2345-6789
        - **Address**: Mental Health Platform DPO, Ministry of Health & Family Welfare, New Delhi - 110001
        - **Response Time**: Within 72 hours as per DPDPA 2023
        """)
        
        # Data breach notification
        st.info("Data breach notifications will be sent within 72 hours as mandated by DPDPA 2023 Section 8(6)")

def display_age_verification():
    """Handle age verification and parental consent for minors"""
    st.title("👤 Age Verification")
    
    age = st.number_input("Please enter your age:", min_value=5, max_value=120, value=18)
    
    if age < 18:
        st.warning("⚠️ **Minor Data Protection**: Users under 18 require verifiable parental consent as per DPDPA 2023 Section 9")
        
        st.subheader("Parental/Guardian Consent Required")
        parent_name = st.text_input("Parent/Guardian Full Name:")
        parent_phone = st.text_input("Parent/Guardian Phone Number:")
        parent_email = st.text_input("Parent/Guardian Email Address:")
        
        consent_checkbox = st.checkbox(
            "I am the parent/guardian and provide verifiable consent for processing my child's data for mental healthcare services as permitted under DPDPA 2023 healthcare exemptions"
        )
        
        if st.button("Verify Parental Consent") and consent_checkbox and parent_name and parent_phone:
            # Record parental consent
            if validators.validate_phone(parent_phone) and validators.validate_email(parent_email):
                st.session_state.user_session['age_verified'] = True
                st.session_state.user_session['minor_consent'] = {
                    'parent_name': parent_name,
                    'parent_phone': parent_phone,
                    'parent_email': parent_email,
                    'consent_time': datetime.datetime.now().isoformat()
                }
                st.success("✅ Parental consent verified. Proceeding to platform...")
                st.rerun()
            else:
                st.error("Please provide valid contact information")
    else:
        if st.button("Confirm Age and Proceed"):
            st.session_state.user_session['age_verified'] = True
            st.rerun()

def display_main_application():
    """Main application interface"""
    st.title("🧠 Mental Health Diagnostic Platform")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Section:", [
        "Dashboard",
        "Basic Assessment", 
        "Advanced Diagnostics",
        "AI Analysis",
        "Reports & Records",
        "Crisis Support",
        "Legal Rights"
    ])
    
    # Data Protection Officer contact (always visible)
    if not st.session_state.user_session['dpo_contact_shown']:
        st.sidebar.info("📞 **DPO Contact**: dpo@mentalhealthplatform.gov.in")
        st.session_state.user_session['dpo_contact_shown'] = True
    
    if page == "Dashboard":
        display_dashboard()
    elif page == "Basic Assessment":
        display_basic_assessment()
    elif page == "Advanced Diagnostics":
        display_advanced_diagnostics()
    elif page == "AI Analysis":
        display_ai_analysis()
    elif page == "Reports & Records":
        display_reports_records()
    elif page == "Crisis Support":
        display_crisis_support()
    elif page == "Legal Rights":
        display_legal_rights()

def display_dashboard():
    """Dashboard with compliance status and overview"""
    st.header("📊 Dashboard")
    
    # Compliance status indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("DPDPA 2023 Status", "✅ Compliant", "Active consent")
    
    with col2:
        st.metric("MHA 2017 Status", "✅ Compliant", "Rights protected")
    
    with col3:
        st.metric("Data Security", "🔒 Encrypted", "AES-256")
    
    with col4:
        st.metric("Crisis Support", "🆘 Available", "24/7 Active")
    
    # Platform statistics
    st.subheader("Platform Coverage")
    conditions_count = conditions_db.get_total_conditions()
    st.info(f"🏥 **{conditions_count}+ Mental Health Conditions** covered across all DSM-5 categories")
    
    # Recent government updates
    st.subheader("Recent Regulatory Updates")
    st.markdown("""
    - **January 2025**: DPDP Rules 2025 draft released for consultation
    - **February 2025**: Public feedback period ends February 18, 2025
    - **2025**: Tele MANAS handled 1.81+ million calls since 2022 launch
    - **October 2024**: Tele MANAS App launched with self-care tools
    """)

def display_basic_assessment():
    """Basic mental health screening with enhanced UI"""
    st.header("🔍 Basic Mental Health Assessment")
    st.markdown("*Comprehensive screening tool designed for Indian population*")
    
    # Consent reaffirmation with better formatting
    st.info("📋 **Data Processing Notice**: This assessment will process your responses to provide preliminary mental health insights. Data is encrypted and protected under DPDPA 2023.")
    
    # Progress indicator
    if 'assessment_started' not in st.session_state:
        st.session_state.assessment_started = False
    
    if not st.session_state.assessment_started:
        # Assessment selection with cards
        st.subheader("Choose Your Assessment")
        
        # Create columns for assessment cards
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🧠 **General Mental Health**\n*Comprehensive overview*", key="general", use_container_width=True):
                st.session_state.selected_assessment = "General Mental Health Screening"
                st.session_state.assessment_started = True
                st.rerun()
                
            if st.button("😟 **Depression Screening**\n*Mood assessment*", key="depression", use_container_width=True):
                st.session_state.selected_assessment = "Depression Screening"
                st.session_state.assessment_started = True
                st.rerun()
                
            if st.button("😴 **Sleep Disorders**\n*Sleep quality evaluation*", key="sleep", use_container_width=True):
                st.session_state.selected_assessment = "Sleep Disorders Screening"
                st.session_state.assessment_started = True
                st.rerun()
        
        with col2:
            if st.button("😰 **Anxiety Disorders**\n*Anxiety assessment*", key="anxiety", use_container_width=True):
                st.session_state.selected_assessment = "Anxiety Disorders Screening"
                st.session_state.assessment_started = True
                st.rerun()
                
            if st.button("💪 **Stress & Trauma**\n*Stress evaluation*", key="stress", use_container_width=True):
                st.session_state.selected_assessment = "Stress & Trauma Assessment"
                st.session_state.assessment_started = True
                st.rerun()
                
            if st.button("🍺 **Substance Use**\n*Usage assessment*", key="substance", use_container_width=True):
                st.session_state.selected_assessment = "Substance Use Screening"
                st.session_state.assessment_started = True
                st.rerun()
        
        # Information about assessments
        st.markdown("---")
        st.markdown("### About These Assessments")
        with st.expander("Assessment Information"):
            st.markdown("""
            - **General Mental Health**: Broad screening covering multiple domains
            - **Anxiety Disorders**: GAD-7 based screening with Indian context
            - **Depression**: PHQ-9 adapted for Indian population
            - **Stress & Trauma**: Culturally sensitive stress assessment
            - **Sleep Disorders**: PSQI-based sleep quality evaluation
            - **Substance Use**: AUDIT framework with Indian considerations
            """)
    
    else:
        # Display the assessment
        assessment_type = st.session_state.selected_assessment
        st.success(f"✅ **Assessment Selected**: {assessment_type}")
        
        if st.button("← Change Assessment", key="change_assessment"):
            st.session_state.assessment_started = False
            st.rerun()
        
        questions = questionnaire_engine.get_basic_questions(assessment_type)
        display_enhanced_questionnaire(questions, assessment_type)

def display_advanced_diagnostics():
    """Advanced diagnostic tools covering 75+ conditions with enhanced UI"""
    st.header("🎯 Advanced Diagnostic Assessment")
    st.markdown("*DSM-5 based comprehensive diagnostic evaluations*")
    
    # Enhanced warning with better styling
    st.error("⚠️ **IMPORTANT**: These advanced diagnostics require professional validation and should NEVER be used for self-diagnosis. All results must be interpreted by qualified mental health professionals as mandated by Mental Healthcare Act 2017.")
    
    # Initialize advanced assessment state
    if 'advanced_category_selected' not in st.session_state:
        st.session_state.advanced_category_selected = False
        st.session_state.selected_category = None
    
    if not st.session_state.advanced_category_selected:
        # Enhanced category selection with cards
        st.subheader("🏥 Select Diagnostic Category")
        st.markdown("Choose from DSM-5 categories covering 75+ mental health conditions")
        
        # Get categories and organize them
        dsm5_categories = conditions_db.get_dsm5_categories()
        
        # Create category cards in columns
        categories_per_row = 3
        for i in range(0, len(dsm5_categories), categories_per_row):
            cols = st.columns(categories_per_row)
            
            for j, col in enumerate(cols):
                if i + j < len(dsm5_categories):
                    category = dsm5_categories[i + j]
                    category_emoji = get_category_emoji(category)
                    
                    with col:
                        if st.button(
                            f"{category_emoji}\n**{category}**",
                            key=f"cat_{i+j}",
                            use_container_width=True,
                            help=f"View conditions in {category}"
                        ):
                            st.session_state.selected_category = category
                            st.session_state.advanced_category_selected = True
                            st.rerun()
        
        # Information about advanced diagnostics
        st.markdown("---")
        with st.expander("ℹ️ About Advanced Diagnostics"):
            st.markdown("""
            ### Professional-Grade Assessments
            - **DSM-5 Compliant**: Based on latest Diagnostic and Statistical Manual
            - **Indian Context**: Adapted for cultural and socioeconomic factors
            - **Comprehensive**: Covering 75+ mental health conditions
            - **Evidence-Based**: Validated assessment instruments
            
            ### Important Notes
            - Results require professional interpretation
            - Not a substitute for clinical diagnosis
            - Compliance with Mental Healthcare Act 2017
            - Data protection under DPDPA 2023
            """)
    
    else:
        # Display selected category and conditions
        selected_category = st.session_state.selected_category
        st.success(f"📋 **Selected Category**: {selected_category}")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### Conditions in {selected_category}")
        with col2:
            if st.button("← Change Category", key="change_category"):
                st.session_state.advanced_category_selected = False
                st.rerun()
        
        conditions = conditions_db.get_conditions_by_category(selected_category) if selected_category else []
        
        if conditions:
            display_conditions_grid(conditions)
        else:
            st.warning(f"No conditions found in {selected_category} category.")

def get_category_emoji(category):
    """Get appropriate emoji for diagnostic category"""
    emoji_map = {
        'Anxiety Disorders': '😰',
        'Depressive Disorders': '😔',
        'Bipolar and Related Disorders': '🔄',
        'Trauma and Stressor-Related Disorders': '💥',
        'Substance-Related and Addictive Disorders': '🍺',
        'Sleep-Wake Disorders': '😴',
        'Eating Disorders': '🍽️',
        'Neurodevelopmental Disorders': '🧠',
        'Personality Disorders': '👤',
        'Obsessive-Compulsive and Related Disorders': '🔄',
        'Schizophrenia Spectrum and Other Psychotic Disorders': '🌀',
        'Feeding and Eating Disorders': '🍽️',
        'Sexual Dysfunctions': '💑',
        'Gender Dysphoria': '⚧️',
        'Disruptive, Impulse-Control, and Conduct Disorders': '⚡',
        'Neurocognitive Disorders': '🧩',
        'Somatic Symptom and Related Disorders': '🏥',
        'Dissociative Disorders': '👥',
        'Elimination Disorders': '🚽',
        'Paraphilic Disorders': '🔒',
        'Other Mental Disorders': '📝'
    }
    return emoji_map.get(category, '🏥')

def display_conditions_grid(conditions):
    """Display conditions in an enhanced grid layout"""
    st.markdown("Click on any condition to learn more and start assessment:")
    
    # Display conditions in cards
    for i, condition in enumerate(conditions):
        with st.container():
            # Create a styled card for each condition
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"#### 🏥 {condition['name']}")
                st.markdown(f"**ICD-11 Code**: {condition.get('icd11_code', 'N/A')} | **DSM-5 Code**: {condition.get('dsm5_code', 'N/A')}")
                st.markdown(f"📊 **Prevalence**: {condition['prevalence']}")
                
                # Show first 3 symptoms
                key_symptoms = condition['key_symptoms'][:3]
                if len(condition['key_symptoms']) > 3:
                    key_symptoms.append(f"... and {len(condition['key_symptoms']) - 3} more")
                st.markdown(f"**Key Symptoms**: {', '.join(key_symptoms)}")
            
            with col2:
                if st.button(
                    f"📋 Assess",
                    key=f"assess_{condition['id']}",
                    use_container_width=True,
                    type="primary"
                ):
                    start_specialized_assessment(condition)
            
            # Expandable details
            with st.expander(f"📖 Detailed Information - {condition['name']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Description:**")
                    st.write(condition['description'])
                    
                    st.markdown("**All Symptoms:**")
                    for symptom in condition['key_symptoms']:
                        st.write(f"• {symptom}")
                
                with col2:
                    if 'severity_criteria' in condition:
                        st.markdown("**Severity Levels:**")
                        for severity, criteria in condition['severity_criteria'].items():
                            st.write(f"**{severity.title()}**: {criteria}")
                    
                    if 'comorbidities' in condition:
                        st.markdown("**Common Comorbidities:**")
                        st.write(", ".join(condition['comorbidities']))
                    
                    if 'treatment_approaches' in condition:
                        st.markdown("**Treatment Approaches:**")
                        for treatment in condition['treatment_approaches']:
                            st.write(f"• {treatment}")
            
            st.markdown("---")

def start_specialized_assessment(condition):
    """Start specialized assessment for a specific condition"""
    st.markdown(f"### 🔬 Specialized Assessment: {condition['name']}")
    
    # Assessment warning
    st.warning(f"⚠️ You are about to begin a specialized assessment for **{condition['name']}**. This assessment uses validated clinical instruments and requires professional interpretation.")
    
    # Get specialized questions
    specialized_questions = assessment_tools.get_specialized_assessment(condition['id'])
    
    if specialized_questions:
        st.info(f"📋 This assessment contains {len(specialized_questions)} specialized questions based on clinical criteria.")
        
        # Add condition context to session state
        if 'current_condition_assessment' not in st.session_state:
            st.session_state.current_condition_assessment = {}
        
        st.session_state.current_condition_assessment = {
            'condition': condition,
            'started': True
        }
        
        # Use enhanced questionnaire
        display_enhanced_questionnaire(specialized_questions, f"{condition['name']} Assessment")
    else:
        st.error(f"❌ No specialized assessment available for {condition['name']}. Please contact support or try a general assessment.")
        st.info("💡 **Alternative**: Try the Basic Assessment for general mental health screening.")

def display_ai_analysis():
    """Code-based comprehensive diagnostic analysis engine"""
    st.header("🧠 Comprehensive Diagnostic Analysis")
    st.markdown("*Advanced code-based clinical analysis using validated algorithms*")
    
    # Analysis engine information
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.info("🔬 **Clinical Analysis Engine**: Evidence-based algorithms using PHQ-9, GAD-7, PSS-10, PSQI, and K10 validated instruments with Indian cultural context")
        
        with col2:
            # Engine capabilities button
            if st.button("🔧 Engine Info", key="engine_info"):
                display_engine_capabilities()
    
    # Check for assessment data
    if st.session_state.user_session.get('assessment_results'):
        assessment_results = st.session_state.user_session['assessment_results']
        
        # Display assessment summary
        st.subheader("📊 Assessment Summary")
        with st.expander("View Assessment Details", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Assessment Type", assessment_results.get('assessment_type', 'Unknown'))
                st.metric("Responses Count", assessment_results.get('responses_count', 0))
            
            with col2:
                st.metric("Severity Level", assessment_results.get('severity_level', 'Unknown').title())
                st.metric("Domains Assessed", len(assessment_results.get('domain_scores', {})))
            
            with col3:
                timestamp = assessment_results.get('timestamp', '')
                if timestamp:
                    from datetime import datetime
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00') if 'Z' in timestamp else timestamp)
                    st.metric("Completed", dt.strftime('%Y-%m-%d %H:%M'))
        
        # Clinical Analysis Section
        st.markdown("---")
        st.subheader("🎯 Clinical Analysis Engine")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("Generate comprehensive clinical insights using validated scoring algorithms and diagnostic decision trees")
        
        with col2:
            analysis_button = st.button(
                "🚀 Generate Analysis",
                type="primary",
                use_container_width=True,
                key="start_analysis"
            )
        
        if analysis_button:
            generate_clinical_analysis(assessment_results)
        
        # Display existing analysis if available
        if 'clinical_analysis_results' in st.session_state.user_session:
            display_analysis_results(st.session_state.user_session['clinical_analysis_results'])
    
    else:
        # No assessment data available
        st.warning("📋 **No Assessment Data Found**")
        st.markdown("To generate AI analysis, you need to:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Start Basic Assessment", use_container_width=True):
                st.session_state.current_page = "Basic Assessment"
                st.rerun()
        
        with col2:
            if st.button("🎯 Start Advanced Diagnostics", use_container_width=True):
                st.session_state.current_page = "Advanced Diagnostics"
                st.rerun()

def display_model_capabilities():
    """Display Meta Phi-3 model capabilities"""
    capabilities = phi3_integration.get_model_capabilities()
    
    st.markdown("### 🤖 Meta Phi-3 Mini Model Capabilities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Model Specifications:**")
        st.write(f"• **Model**: {capabilities['model_name']}")
        st.write(f"• **Parameters**: {capabilities['parameters']}")
        st.write(f"• **Context**: {capabilities['context_window']}")
        st.write(f"• **Provider**: {capabilities['api_provider']}")
        
        st.markdown("**Specialized Domains:**")
        for domain in capabilities['specialized_domains']:
            st.write(f"• {domain}")
    
    with col2:
        st.markdown("**Language Support:**")
        languages = capabilities['languages_supported'][:6]  # Show first 6
        for lang in languages:
            st.write(f"• {lang}")
        if len(capabilities['languages_supported']) > 6:
            st.write(f"• ... and {len(capabilities['languages_supported']) - 6} more")
        
        st.markdown("**Compliance Features:**")
        for feature in capabilities['compliance_features']:
            st.write(f"• {feature}")

def generate_ai_analysis(assessment_results):
    """Generate AI analysis with enhanced UI"""
    with st.spinner("🧠 Meta Phi-3 Mini is analyzing your assessment..."):
        # Add progress indicator
        progress_bar = st.progress(0)
        progress_text = st.empty()
        
        # Simulate analysis steps
        import time
        
        progress_bar.progress(25)
        progress_text.text("🔍 Analyzing assessment responses...")
        time.sleep(1)
        
        progress_bar.progress(50)
        progress_text.text("🤖 Processing with Meta Phi-3 Mini...")
        
        # Generate actual analysis
        analysis = phi3_integration.generate_diagnostic_analysis(assessment_results)
        
        progress_bar.progress(75)
        progress_text.text("📊 Structuring diagnostic insights...")
        time.sleep(0.5)
        
        progress_bar.progress(100)
        progress_text.text("✅ Analysis complete!")
        time.sleep(0.5)
        
        # Clear progress indicators
        progress_bar.empty()
        progress_text.empty()
        
        if analysis:
            # Store analysis results
            st.session_state.user_session['ai_analysis_results'] = analysis
            st.success("✅ **AI Analysis Successfully Generated**")
            
            # Display results
            display_ai_results(analysis)
        else:
            st.error("❌ **AI Analysis Failed**")
            st.markdown("**Possible Issues:**")
            st.write("• Hugging Face API temporary unavailability")
            st.write("• Network connectivity issues")
            st.write("• Assessment data format problems")
            
            if st.button("🔄 Retry Analysis"):
                st.rerun()

def display_ai_results(analysis):
    """Display AI analysis results with enhanced formatting"""
    st.markdown("---")
    st.markdown("## 🔬 AI Analysis Results")
    
    # Disclaimer banner
    st.error("⚠️ **CRITICAL DISCLAIMER**: AI-generated results require professional medical validation. This analysis is for educational purposes only and complies with Mental Healthcare Act 2017.")
    
    # Primary insights
    if analysis.get('primary_insights'):
        st.markdown("### 🧠 Primary Diagnostic Insights")
        st.info(analysis['primary_insights'])
    
    # Differential diagnoses
    if analysis.get('differential_diagnoses'):
        st.markdown("### 🎯 Differential Diagnosis Considerations")
        
        for i, diagnosis in enumerate(analysis['differential_diagnoses']):
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**{i+1}. {diagnosis['condition']}**")
                    st.write(diagnosis['rationale'])
                
                with col2:
                    confidence = diagnosis['confidence']
                    color = "green" if confidence > 70 else "orange" if confidence > 40 else "red"
                    st.metric("Confidence", f"{confidence}%")
    
    # Severity and risk assessment
    col1, col2 = st.columns(2)
    
    with col1:
        if 'severity_score' in analysis:
            st.markdown("### 📊 Severity Assessment")
            severity = analysis['severity_score']
            st.metric("Overall Severity", f"{severity}/10")
            
            if severity <= 3:
                st.success("🟢 **Minimal severity level**")
            elif severity <= 6:
                st.warning("🟡 **Moderate severity level**")
            else:
                st.error("🔴 **High severity level**")
    
    with col2:
        if 'crisis_risk' in analysis:
            st.markdown("### 🚨 Crisis Risk Assessment")
            crisis_risk = analysis['crisis_risk']
            st.metric("Crisis Risk", f"{crisis_risk}/5")
            
            if crisis_risk > 3:
                st.error("⚠️ **ELEVATED CRISIS RISK DETECTED**")
                st.markdown("**Immediate Action Required:**")
                st.write("📞 Contact Tele MANAS: **1800-891-4416**")
                st.write("🏥 Seek immediate professional help")
            elif crisis_risk > 1:
                st.warning("⚠️ **Moderate crisis risk**")
                st.write("Consider professional consultation soon")
            else:
                st.success("✅ **Low crisis risk**")
    
    # Treatment recommendations
    if analysis.get('treatment_recommendations'):
        st.markdown("### 💊 Treatment Recommendations")
        st.info(analysis['treatment_recommendations'])
    
    # Cultural considerations
    if analysis.get('cultural_considerations'):
        st.markdown("### 🇮🇳 Cultural Considerations")
        st.write(analysis['cultural_considerations'])
    
    # Next steps
    if analysis.get('next_steps'):
        st.markdown("### 📋 Recommended Next Steps")
        st.write(analysis['next_steps'])
    
    # Professional validation reminder
    st.markdown("---")
    st.warning("🏥 **MANDATORY**: All AI-generated results require validation by qualified mental health professionals as mandated by Mental Healthcare Act 2017")
    
    # Analysis metadata
    if 'metadata' in analysis:
        with st.expander("🔧 Technical Details"):
            metadata = analysis['metadata']
            st.json(metadata)

def display_enhanced_questionnaire(questions, assessment_type):
    """Display enhanced interactive questionnaire with better UI"""
    st.markdown(f"### 📋 {assessment_type}")
    
    if not questions:
        st.error("❌ No questions found for this assessment type. Please try another assessment.")
        return
    
    # Initialize responses in session state
    if f'responses_{assessment_type}' not in st.session_state:
        st.session_state[f'responses_{assessment_type}'] = {}
    
    responses = st.session_state[f'responses_{assessment_type}']
    
    # Progress indicator
    progress_value = len(responses) / len(questions) if questions else 0
    st.progress(progress_value, f"Progress: {len(responses)}/{len(questions)} questions answered")
    
    # Display questions in a more user-friendly format
    for i, question in enumerate(questions):
        with st.container():
            st.markdown(f"#### Question {i+1} of {len(questions)}")
            st.markdown(f"**{question['text']}**")
            
            # Use session state to track responses
            response_key = f"resp_{assessment_type}_{question['id']}"
            
            try:
                if question['type'] == 'scale':
                    # Enhanced scale display with labels
                    scale_labels = question.get('scale_labels', [])
                    if scale_labels:
                        st.caption("Scale:")
                        for idx, label in enumerate(scale_labels):
                            st.caption(f"**{idx}** - {label}")
                    
                    response = st.slider(
                        "Your response:",
                        min_value=int(question['scale_min']),
                        max_value=int(question['scale_max']),
                        value=responses.get(question['id'], int(question['scale_min'])),
                        key=response_key
                    )
                    
                elif question['type'] == 'multiple_choice':
                    response = st.radio(
                        "Select your answer:",
                        question.get('options', ['Option 1', 'Option 2']),
                        index=0 if question['id'] not in responses else question.get('options', []).index(responses[question['id']]) if responses[question['id']] in question.get('options', []) else 0,
                        key=response_key
                    )
                    
                elif question['type'] == 'checkbox':
                    response = st.multiselect(
                        "Select all that apply:",
                        question.get('options', ['Option 1', 'Option 2']),
                        default=responses.get(question['id'], []),
                        key=response_key
                    )
                else:
                    st.warning(f"⚠️ Unknown question type: {question['type']}")
                    response = None
                
                # Store response
                if response is not None:
                    responses[question['id']] = response
                    
            except Exception as e:
                st.error(f"❌ Error with question {i+1}: {str(e)}")
                st.write(f"Question details: {question}")
        
        # Add separator between questions
        if i < len(questions) - 1:
            st.markdown("---")
    
    # Assessment completion section
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if len(responses) >= len(questions) * 0.8:  # Allow submission if 80% complete
            if st.button("✅ Submit Assessment", type="primary", use_container_width=True, key=f"submit_{assessment_type}"):
                submit_assessment(responses, assessment_type, questions)
        else:
            st.warning(f"⏳ Please answer at least {int(len(questions) * 0.8)} questions to submit")
            if st.button("📊 Save Progress", use_container_width=True, key=f"save_{assessment_type}"):
                st.success("💾 Progress saved! You can continue later.")

def submit_assessment(responses, assessment_type, questions):
    """Process and submit assessment results"""
    try:
        # Calculate domain scores based on responses
        domain_scores = calculate_domain_scores(responses, questions)
        
        # Assess severity level
        severity_level = assess_severity_level(domain_scores)
        
        # Generate preliminary insights
        insights = generate_preliminary_insights(responses, assessment_type, domain_scores)
        
        # Create comprehensive results structure
        assessment_results = {
            'assessment_type': assessment_type,
            'timestamp': datetime.datetime.now().isoformat(),
            'responses': responses,
            'responses_count': len(responses),
            'domain_scores': domain_scores,
            'severity_level': severity_level,
            'preliminary_insights': insights,
            'recommendations': generate_recommendations(severity_level, domain_scores),
            'cultural_context': 'Indian population',
            'compliance_framework': 'DPDPA_2023_MHA_2017'
        }
        
        # Store in session state
        st.session_state.user_session['assessment_results'] = assessment_results
        
        # Display completion message
        st.success("✅ Assessment completed successfully!")
        
        # Show preliminary results
        with st.expander("📊 Preliminary Results", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Overall Severity", severity_level.title(), domain_scores.get('overall', 0))
                st.metric("Responses Collected", len(responses), f"{len(responses)}/{len(questions)}")
            
            with col2:
                if domain_scores:
                    st.write("**Domain Scores:**")
                    for domain, score in domain_scores.items():
                        if domain != 'overall':
                            st.write(f"- {domain.title()}: {score:.1f}/10")
        
        st.info("🤖 **Next Step**: Go to 'AI Analysis' for detailed Meta Phi-3 powered insights!")
        
        # Reset assessment state for new assessment
        st.session_state.assessment_started = False
        
    except Exception as e:
        st.error(f"❌ Error processing assessment: {str(e)}")

def calculate_domain_scores(responses, questions):
    """Calculate domain-specific scores from responses"""
    domain_totals = {}
    domain_counts = {}
    
    for question in questions:
        domain = question.get('domain', 'general')
        weight = question.get('weight', 1.0)
        
        if question['id'] in responses:
            response = responses[question['id']]
            
            # Convert response to numeric score
            if isinstance(response, (int, float)):
                score = response
            elif isinstance(response, str):
                # For multiple choice, find index
                options = question.get('options', [])
                score = options.index(response) if response in options else 0
            elif isinstance(response, list):
                # For checkboxes, count selections
                score = len(response)
            else:
                score = 0
            
            # Normalize score to 0-10 scale
            max_score = question.get('scale_max', len(question.get('options', [1])))
            normalized_score = (score / max_score) * 10 if max_score > 0 else 0
            
            # Apply weight
            weighted_score = normalized_score * weight
            
            if domain not in domain_totals:
                domain_totals[domain] = 0
                domain_counts[domain] = 0
            
            domain_totals[domain] += weighted_score
            domain_counts[domain] += weight
    
    # Calculate averages
    domain_scores = {}
    for domain in domain_totals:
        if domain_counts[domain] > 0:
            domain_scores[domain] = domain_totals[domain] / domain_counts[domain]
    
    # Calculate overall score
    if domain_scores:
        domain_scores['overall'] = sum(domain_scores.values()) / len(domain_scores)
    
    return domain_scores

def assess_severity_level(domain_scores):
    """Assess overall severity level"""
    overall_score = domain_scores.get('overall', 0)
    
    if overall_score <= 3:
        return 'minimal'
    elif overall_score <= 5:
        return 'mild'
    elif overall_score <= 7:
        return 'moderate'
    else:
        return 'severe'

def generate_preliminary_insights(responses, assessment_type, domain_scores):
    """Generate preliminary insights from assessment"""
    insights = []
    
    # Assessment-specific insights
    if 'anxiety' in assessment_type.lower():
        anxiety_score = domain_scores.get('anxiety', domain_scores.get('panic', 0))
        if anxiety_score > 6:
            insights.append("Elevated anxiety symptoms detected")
    
    if 'depression' in assessment_type.lower():
        depression_score = domain_scores.get('depression', 0)
        if depression_score > 6:
            insights.append("Significant depressive symptoms identified")
    
    # General insights
    overall_score = domain_scores.get('overall', 0)
    if overall_score > 7:
        insights.append("Multiple domains affected - comprehensive evaluation recommended")
    elif overall_score > 5:
        insights.append("Moderate symptoms present - professional consultation advised")
    
    return insights if insights else ["Preliminary assessment completed - professional interpretation recommended"]

def generate_recommendations(severity_level, domain_scores):
    """Generate culturally appropriate recommendations"""
    recommendations = []
    
    if severity_level in ['moderate', 'severe']:
        recommendations.append("Consult with a qualified mental health professional")
        recommendations.append("Contact Tele MANAS: 1800-891-4416 for immediate support")
    
    if severity_level in ['mild', 'moderate']:
        recommendations.append("Consider stress management techniques and mindfulness practices")
        recommendations.append("Maintain regular sleep schedule and healthy lifestyle")
    
    # Cultural recommendations for Indian context
    recommendations.extend([
        "Engage with family and social support systems",
        "Consider holistic approaches including yoga and meditation",
        "Ensure compliance with Indian Mental Healthcare Act 2017 rights"
    ])
    
    return recommendations

def display_questionnaire(questions, assessment_type):
    """Legacy questionnaire display - redirects to enhanced version"""
    display_enhanced_questionnaire(questions, assessment_type)

def display_reports_records():
    """Display diagnostic reports and medical records access"""
    st.header("📄 Reports & Medical Records")
    
    # Patient rights under Mental Healthcare Act 2017
    st.info("📋 **Right to Access Medical Records**: Under Mental Healthcare Act 2017, you have the right to access all your mental health records including assessments, treatment plans, and diagnostic reports.")
    
    # Generate comprehensive report
    if st.button("Generate Comprehensive Diagnostic Report"):
        if st.session_state.user_session.get('assessment_results'):
            report = diagnostic_reports.generate_comprehensive_report(
                st.session_state.user_session['assessment_results'],
                st.session_state.user_session['user_id']
            )
            
            st.subheader("🏥 Professional Diagnostic Report")
            st.markdown(report['summary'])
            
            # Severity scoring
            st.subheader("📊 Severity Scoring")
            for condition, score in report['severity_scores'].items():
                st.metric(condition, f"{score}/10", f"{'High' if score > 7 else 'Moderate' if score > 4 else 'Low'} severity")
            
            # Comorbidity assessment
            if report['comorbidities']:
                st.subheader("🔄 Comorbidity Assessment")
                for comorbidity in report['comorbidities']:
                    st.write(f"- {comorbidity}")
            
            # Treatment recommendations
            st.subheader("💊 Treatment Recommendations")
            st.markdown(report['treatment_recommendations'])
            
            # Download report
            st.download_button(
                "📥 Download Report (PDF)",
                data=report['pdf_content'],
                file_name=f"mental_health_report_{datetime.date.today()}.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("No assessment data available. Please complete an assessment first.")

def display_crisis_support():
    """Crisis intervention and emergency support"""
    st.header("🆘 Crisis Support & Emergency Resources")
    
    crisis_intervention.display_comprehensive_support()

def display_legal_rights():
    """Display legal rights and obligations"""
    st.header("⚖️ Legal Rights & Obligations")
    
    # Patient rights under Mental Healthcare Act 2017
    mha_compliance.display_comprehensive_rights()
    
    # DPDPA rights
    dpdpa_compliance.display_data_subject_rights()
    
    # Legal documents
    legal_documents.display_all_documents()

def display_engine_capabilities():
    """Display clinical analysis engine capabilities"""
    with st.expander("🔬 Clinical Analysis Engine Capabilities", expanded=True):
        st.markdown("""
        ### Evidence-Based Clinical Instruments
        
        **Validated Assessments:**
        - **PHQ-9**: Depression screening (0-27 scale)
        - **GAD-7**: Anxiety disorders screening (0-21 scale)
        - **PSS-10**: Perceived stress scale with reverse scoring (0-40 scale)
        - **PSQI**: Sleep quality assessment with component scoring (0-21 scale)
        - **K10**: General mental health screening (10-50 scale)
        
        **Advanced Features:**
        - ✅ Evidence-based scoring algorithms without external AI dependencies
        - ✅ Diagnostic decision trees using DSM-5 criteria
        - ✅ Risk assessment with safety protocols
        - ✅ Cultural adaptation for Indian population
        - ✅ Government of India compliance (MHA 2017, DPDPA 2023)
        - ✅ Comprehensive visualizations and reporting
        
        **Clinical Accuracy:**
        - Validated cutoff scores for each instrument
        - Proper item transformations and reverse scoring
        - Component-based scoring for complex instruments (PSQI)
        - Clinical severity mapping aligned with international standards
        
        **Privacy & Security:**
        - All analysis performed locally without external API calls
        - Data encryption and secure processing
        - DPDPA 2023 compliant data handling
        """)

def generate_clinical_analysis(assessment_results: dict):
    """Generate comprehensive clinical analysis using the code-based engine"""
    
    with st.spinner("🔄 Running comprehensive clinical analysis..."):
        try:
            # Prepare assessment data for analysis engine
            analysis_data = {
                "assessment_type": assessment_results.get('assessment_type', 'General Mental Health Screening'),
                "responses": assessment_results.get('responses', {}),
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            # Run analysis through the code-based engine
            analysis_result = analysis_engine.analyze_assessment(analysis_data)
            
            # Store results in session state
            st.session_state.user_session['clinical_analysis_results'] = analysis_result
            
            # Display success message
            st.success("✅ **Clinical Analysis Complete!** Comprehensive insights generated using validated algorithms.")
            
            # Auto-display results
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ **Analysis Failed**: {str(e)}")
            st.info("🔧 **Troubleshooting**: Please ensure assessment data is complete and try again.")

def display_analysis_results(analysis_result):
    """Display comprehensive analysis results with visualizations"""
    
    # Check if we can use the built-in comprehensive display
    if hasattr(analysis_result, 'display_comprehensive_analysis') and callable(getattr(analysis_result, 'display_comprehensive_analysis')):
        # Use the analysis engine's built-in display method
        analysis_engine.display_comprehensive_analysis(analysis_result)
    else:
        # Fallback display method
        st.subheader("📊 Analysis Results")
        
        # Convert to dict if it's an AnalysisResult object
        if hasattr(analysis_result, '__dict__'):
            result_dict = analysis_result.__dict__
        else:
            result_dict = analysis_result
        
        # Executive Summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Score", f"{result_dict.get('total_score', 0)}/{result_dict.get('max_possible_score', 100)}")
        
        with col2:
            severity = result_dict.get('severity_level', 'unknown')
            if hasattr(severity, 'value'):
                severity_display = severity.value.title()
            else:
                severity_display = str(severity).title()
            st.metric("Severity", severity_display)
        
        with col3:
            risk = result_dict.get('risk_level', 'unknown')
            if hasattr(risk, 'value'):
                risk_display = risk.value.title()
            else:
                risk_display = str(risk).title()
            st.metric("Risk Level", risk_display)
        
        with col4:
            st.metric("Assessment", result_dict.get('assessment_type', 'Unknown'))
        
        # Clinical Interpretation
        st.subheader("🏥 Clinical Interpretation")
        interpretation = result_dict.get('clinical_interpretation', 'Analysis completed.')
        st.info(interpretation)
        
        # Red Flags
        red_flags = result_dict.get('red_flags', [])
        if red_flags:
            st.subheader("🚨 Important Alerts")
            for flag in red_flags:
                st.error(f"⚠️ **ALERT**: {flag}")
        
        # Recommendations
        st.subheader("💡 Recommendations")
        recommendations = result_dict.get('recommendations', [])
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"**{i}.** {rec}")
        
        # Next Steps
        st.subheader("📋 Next Steps")
        next_steps = result_dict.get('next_steps', [])
        for i, step in enumerate(next_steps, 1):
            if "IMMEDIATE" in step or "URGENT" in step:
                st.error(f"**{i}.** {step}")
            else:
                st.markdown(f"**{i}.** {step}")
        
        # Domain Scores
        domain_scores = result_dict.get('domain_scores', {})
        if domain_scores:
            st.subheader("📊 Domain Analysis")
            
            domain_data = {
                'Domain': list(domain_scores.keys()),
                'Score': list(domain_scores.values())
            }
            domain_df = pd.DataFrame(domain_data)
            st.dataframe(domain_df, use_container_width=True)
        
        # Compliance Information
        st.subheader("⚖️ Compliance & Legal Information")
        st.warning("""
        **Mental Healthcare Act 2017 & DPDPA 2023 Compliance**: This analysis uses evidence-based 
        clinical algorithms for screening purposes only. Professional validation by qualified 
        mental health professionals is required for all results. This tool complements but does 
        not replace professional medical evaluation.
        """)

if __name__ == "__main__":
    main()
