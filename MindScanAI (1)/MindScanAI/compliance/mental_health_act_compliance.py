import streamlit as st
import datetime
from typing import Dict, List, Any

class MentalHealthActCompliance:
    """Mental Healthcare Act 2017 compliance manager"""
    
    def __init__(self):
        self.act_sections = self._load_act_sections()
    
    def display_patient_rights(self, language: str = 'english'):
        """Display patient rights under Mental Healthcare Act 2017"""
        
        if language == 'hindi':
            self._display_hindi_rights()
        else:
            self._display_english_rights()
    
    def _display_english_rights(self):
        """Display patient rights in English"""
        
        st.markdown("""
        ## Mental Healthcare Act 2017 - Patient Rights
        
        ### Right to Access Mental Health Care (Section 18)
        - Every person has the right to access mental health care and treatment
        - Right to affordable mental health care services
        - Protection from discrimination in healthcare settings
        
        ### Right to Confidentiality (Section 23)
        - Complete confidentiality of all mental health information
        - Protection extends to all information stored in electronic or digital format
        - Prohibition on disclosure without explicit consent
        
        ### Right to Access Medical Records (Section 24)
        - Access to all mental health records including:
          - Medical notes and assessments
          - Treatment plans and progress reports
          - Diagnostic reports and test results
          - Any other information recorded by healthcare providers
        
        ### Advance Directives (Section 5)
        - Right to make advance directives regarding mental healthcare
        - Specification of treatment preferences
        - Nomination of representatives for healthcare decisions
        
        ### Right to Complaints (Section 37)
        - File complaints regarding mental health services
        - Protection against retaliation for filing complaints
        - Right to grievance redressal through Mental Health Review Boards
        
        ### Informed Consent Requirements (Section 19)
        - Right to give or refuse consent for treatment
        - Full disclosure of treatment options and risks
        - Protection of decision-making capacity
        """)
    
    def _display_hindi_rights(self):
        """Display patient rights in Hindi"""
        
        st.markdown("""
        ## मानसिक स्वास्थ्य देखभाल अधिनियम 2017 - रोगी अधिकार
        
        ### मानसिक स्वास्थ्य देखभाल तक पहुंच का अधिकार (धारा 18)
        - हर व्यक्ति को मानसिक स्वास्थ्य देखभाल और उपचार तक पहुंच का अधिकार है
        - किफायती मानसिक स्वास्थ्य देखभाल सेवाओं का अधिकार
        - स्वास्थ्य देखभाल सेटिंग्स में भेदभाव से सुरक्षा
        
        ### गोपनीयता का अधिकार (धारा 23)
        - सभी मानसिक स्वास्थ्य जानकारी की पूर्ण गोपनीयता
        - इलेक्ट्रॉनिक या डिजिटल प्रारूप में संग्रहीत सभी जानकारी तक सुरक्षा विस्तार
        - स्पष्ट सहमति के बिना प्रकटीकरण पर प्रतिबंध
        
        ### चिकित्सा रिकॉर्ड तक पहुंच का अधिकार (धारा 24)
        - सभी मानसिक स्वास्थ्य रिकॉर्ड तक पहुंच जिसमें शामिल है:
          - चिकित्सा नोट्स और आकलन
          - उपचार योजनाएं और प्रगति रिपोर्ट
          - निदान रिपोर्ट और परीक्षण परिणाम
          - स्वास्थ्य सेवा प्रदाताओं द्वारा दर्ज की गई कोई अन्य जानकारी
        
        ### अग्रिम निर्देश (धारा 5)
        - मानसिक स्वास्थ्य देखभाल के संबंध में अग्रिम निर्देश बनाने का अधिकार
        - उपचार प्राथमिकताओं का विनिर्देश
        - स्वास्थ्य देखभाल निर्णयों के लिए प्रतिनिधियों का नामांकन
        """)
    
    def display_comprehensive_rights(self):
        """Display comprehensive patient rights with interactive elements"""
        
        st.header("⚖️ Complete Patient Rights Under Mental Healthcare Act 2017")
        
        # Create tabs for different categories of rights
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🏥 Healthcare Rights",
            "🔒 Privacy & Confidentiality", 
            "📋 Information Access",
            "⚖️ Legal Protections",
            "🆘 Emergency Rights"
        ])
        
        with tab1:
            self._display_healthcare_rights()
        
        with tab2:
            self._display_privacy_rights()
        
        with tab3:
            self._display_information_rights()
        
        with tab4:
            self._display_legal_protections()
        
        with tab5:
            self._display_emergency_rights()
    
    def _display_healthcare_rights(self):
        """Display healthcare-specific rights"""
        
        st.subheader("🏥 Fundamental Healthcare Rights")
        
        st.markdown("""
        ### Right to Mental Healthcare (Section 18)
        - **Universal Access**: Every person shall have a right to access mental health care and treatment from mental health services
        - **Non-Discrimination**: Equal access regardless of gender, sex, sexual orientation, religion, culture, caste, social or political beliefs
        - **Affordable Care**: Right to mental health care and treatment that is affordable
        - **Community Integration**: Right to live in the community and be included in community activities
        
        ### Treatment Rights (Section 19)
        - **Informed Consent**: Right to receive complete information about proposed treatment
        - **Treatment Refusal**: Right to refuse treatment or procedure (with exceptions for emergency situations)
        - **Second Opinion**: Right to seek a second opinion
        - **Treatment Review**: Right to have treatment reviewed by independent healthcare professionals
        
        ### Quality Standards
        - **Evidence-Based Care**: Right to treatment based on scientific evidence
        - **Least Restrictive Environment**: Treatment in the least restrictive environment possible
        - **Cultural Sensitivity**: Culturally appropriate care and treatment
        """)
        
        # Interactive elements
        if st.button("📋 Know Your Treatment Rights"):
            st.info("""
            **Your Treatment Rights Include:**
            1. Detailed explanation of your condition
            2. Information about all available treatment options
            3. Explanation of risks and benefits
            4. Right to involve family/caregivers in treatment planning
            5. Right to regular review of treatment progress
            """)
    
    def _display_privacy_rights(self):
        """Display privacy and confidentiality rights"""
        
        st.subheader("🔒 Privacy & Confidentiality Rights")
        
        st.markdown("""
        ### Comprehensive Confidentiality (Section 23)
        - **Absolute Confidentiality**: All information about persons with mental illness shall be kept confidential
        - **Digital Protection**: Confidentiality applies to all information stored in electronic or digital format
        - **Professional Obligations**: All mental health professionals bound by confidentiality
        - **Legal Restrictions**: Information cannot be disclosed in legal proceedings without specific procedures
        
        ### Information Sharing Restrictions
        - **Explicit Consent Required**: Information can only be shared with explicit written consent
        - **Limited Exceptions**: Only specific legal exceptions allow information sharing without consent
        - **Media Protection**: Prohibition on media disclosure of identity
        - **Family Restrictions**: Even family members need consent to access information
        
        ### Digital Privacy Protections
        - **Electronic Records**: Same confidentiality applies to electronic health records
        - **Data Security**: Secure storage and transmission of digital health information
        - **Access Logging**: Audit trails for all access to digital records
        """)
        
        # Privacy management tools
        if st.button("🔐 Manage Privacy Settings"):
            self._display_privacy_management()
    
    def _display_information_rights(self):
        """Display information access rights"""
        
        st.subheader("📋 Information Access Rights")
        
        st.markdown("""
        ### Right to Access Medical Records (Section 24)
        - **Complete Access**: Right to access all medical records and information
        - **Timely Access**: Records must be provided within reasonable time
        - **Copy Rights**: Right to obtain copies of all records
        - **Explanation Rights**: Right to have records explained in understandable language
        
        ### Covered Information
        - Medical history and assessments
        - Diagnostic reports and test results
        - Treatment plans and medication records
        - Progress notes and discharge summaries
        - Advance directives and consent forms
        
        ### Digital Records Access
        - Electronic health records access
        - Digital assessment results
        - Online consultation records
        - Mobile health app data
        """)
        
        # Record access tool
        if st.button("📄 Request Medical Records"):
            self._display_record_request_form()
    
    def _display_legal_protections(self):
        """Display legal protections and safeguards"""
        
        st.subheader("⚖️ Legal Protections & Safeguards")
        
        st.markdown("""
        ### Mental Health Review Board (MHRB) Protections
        - **Independent Review**: Right to independent review of treatment decisions
        - **Appeals Process**: Right to appeal treatment decisions to MHRB
        - **Legal Representation**: Right to legal representation in MHRB proceedings
        - **Regular Review**: Periodic review of ongoing treatment
        
        ### Advance Directives (Section 5)
        - **Future Planning**: Right to make decisions about future treatment
        - **Binding Nature**: Advance directives are legally binding
        - **Nominated Representative**: Right to nominate someone to make decisions
        - **Review and Modification**: Right to review and modify directives
        
        ### Complaint Rights (Section 37)
        - **Formal Complaints**: Right to file complaints about mental health services
        - **Protection from Retaliation**: Legal protection against retaliation
        - **Investigation Rights**: Right to investigation of complaints
        - **Remedy Rights**: Right to appropriate remedies for violations
        """)
    
    def _display_emergency_rights(self):
        """Display emergency situation rights"""
        
        st.subheader("🆘 Emergency Rights & Crisis Protections")
        
        st.markdown("""
        ### Emergency Treatment Rights
        - **Immediate Care**: Right to immediate care in emergency situations
        - **Minimal Intervention**: Least restrictive intervention necessary
        - **Time Limitations**: Strict time limits on emergency interventions
        - **Review Requirements**: Immediate review of emergency decisions
        
        ### Crisis Situation Protections
        - **Legal Safeguards**: Enhanced legal protections during crisis
        - **Family Notification**: Rights regarding family notification
        - **Independent Advocacy**: Access to independent advocacy services
        - **Discharge Planning**: Right to appropriate discharge planning
        
        ### 24/7 Support Services
        - **Tele MANAS**: National helpline 1800-891-4416
        - **Crisis Intervention**: Immediate crisis intervention services
        - **Emergency Contacts**: Access to emergency mental health services
        """)
        
        # Emergency resources
        st.error("🆘 **Crisis Support Available 24/7**")
        st.markdown("""
        **Immediate Help:**
        - **Tele MANAS**: 1800-891-4416
        - **National Suicide Prevention**: 9152987821
        - **Emergency Services**: 112
        """)
    
    def _display_privacy_management(self):
        """Privacy settings management interface"""
        
        st.subheader("🔐 Privacy Settings Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Information Sharing Preferences")
            family_sharing = st.checkbox("Allow family access to basic health information")
            emergency_sharing = st.checkbox("Allow emergency contact notification")
            research_participation = st.checkbox("Participate in anonymized research")
        
        with col2:
            st.markdown("### Communication Preferences")
            phone_contact = st.checkbox("Allow phone communication")
            email_contact = st.checkbox("Allow email communication")
            text_updates = st.checkbox("Receive text message updates")
        
        if st.button("💾 Save Privacy Preferences"):
            preferences = {
                'family_sharing': family_sharing,
                'emergency_sharing': emergency_sharing,
                'research_participation': research_participation,
                'phone_contact': phone_contact,
                'email_contact': email_contact,
                'text_updates': text_updates,
                'timestamp': datetime.datetime.now().isoformat()
            }
            
            # In production, save encrypted preferences
            st.success("✅ Privacy preferences saved securely")
    
    def _display_record_request_form(self):
        """Medical records request form"""
        
        st.subheader("📄 Medical Records Request Form")
        
        record_type = st.multiselect(
            "Select records to request:",
            [
                "Complete Medical History",
                "Assessment Reports",
                "Treatment Plans",
                "Medication Records",
                "Progress Notes",
                "Diagnostic Reports",
                "Advance Directives"
            ]
        )
        
        date_range = st.date_input(
            "Select date range:",
            value=[datetime.date.today() - datetime.timedelta(days=365), datetime.date.today()]
        )
        
        delivery_method = st.radio(
            "Preferred delivery method:",
            ["Secure Email", "Encrypted Download", "Physical Copy", "In-Person Pickup"]
        )
        
        purpose = st.text_area("Purpose for requesting records (optional):")
        
        if st.button("📤 Submit Records Request"):
            if record_type:
                request_data = {
                    'record_types': record_type,
                    'date_range': [str(date_range[0]), str(date_range[1])],
                    'delivery_method': delivery_method,
                    'purpose': purpose,
                    'timestamp': datetime.datetime.now().isoformat(),
                    'status': 'submitted'
                }
                
                # In production, process the request
                st.success("✅ Records request submitted. You will receive your records within 7 working days as per Mental Healthcare Act 2017")
            else:
                st.error("Please select at least one record type")
    
    def _load_act_sections(self) -> Dict[str, Any]:
        """Load Mental Healthcare Act 2017 sections"""
        return {
            'section_5': 'Advance Directives',
            'section_18': 'Right to Access Mental Health Care',
            'section_19': 'Right to Give or Refuse Consent for Treatment',
            'section_23': 'Right to Confidentiality',
            'section_24': 'Right to Access Medical Records',
            'section_37': 'Complaints'
        }
