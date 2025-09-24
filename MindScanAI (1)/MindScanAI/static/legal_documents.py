import streamlit as st


class LegalDocuments:
    """Display legal documents and compliance information"""
    
    def __init__(self):
        pass
    
    def display_all_documents(self):
        """Display all legal documents and compliance information"""
        
        st.header("📋 Legal Documents & Compliance")
        
        # Create tabs for different document types
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🏛️ Government Acts",
            "📄 Terms of Service", 
            "🔒 Privacy Policy",
            "⚖️ Disclaimers",
            "📞 Contact Information"
        ])
        
        with tab1:
            self._display_government_acts()
        
        with tab2:
            self._display_terms_of_service()
        
        with tab3:
            self._display_privacy_policy()
        
        with tab4:
            self._display_disclaimers()
        
        with tab5:
            self._display_contact_information()
    
    def _display_government_acts(self):
        """Display relevant Government of India acts and regulations"""
        
        st.subheader("Government of India Legal Framework")
        
        st.markdown("""
        ### Digital Personal Data Protection Act (DPDPA) 2023
        
        **Key Provisions Applicable to This Platform:**
        - Section 6: Lawful processing of personal data
        - Section 7: Notice requirements for data processing
        - Section 8: Consent requirements and withdrawal mechanisms
        - Section 9: Special provisions for children's data (under 18)
        - Section 10: Data breach notification requirements
        
        **Your Rights Under DPDPA 2023:**
        - Right to access your personal data
        - Right to correction and erasure
        - Right to data portability
        - Right to grievance redressal
        """)
        
        st.markdown("""
        ### Mental Healthcare Act 2017
        
        **Patient Rights (Section 18-25):**
        - Right to access mental healthcare
        - Right to community living
        - Right to protection from cruel treatment
        - Right to equality and non-discrimination
        - Right to information about treatment
        - Right to confidentiality
        - Right to access medical records
        - Right to complain about deficiencies
        
        **Advanced Directives (Section 5):**
        You have the right to make advance directives regarding your mental healthcare treatment.
        """)
    
    def _display_terms_of_service(self):
        """Display terms of service"""
        
        st.subheader("Terms of Service")
        
        st.markdown("""
        ### Acceptance of Terms
        
        By using this Mental Health Diagnostic Platform, you agree to comply with and be bound by these Terms of Service and all applicable laws and regulations.
        
        ### Service Description
        
        This platform provides AI-assisted mental health screening and diagnostic support tools. All results are preliminary and require professional medical validation.
        
        ### User Responsibilities
        
        - Provide accurate information during assessments
        - Use the platform responsibly and not for emergency situations
        - Understand that AI results are not substitute for professional medical advice
        - Respect the confidentiality of the platform
        
        ### Limitation of Liability
        
        This platform is for informational purposes only. We do not provide medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals for medical decisions.
        
        ### Compliance Requirements
        
        This platform operates under strict Government of India regulations including DPDPA 2023 and Mental Healthcare Act 2017.
        """)
    
    def _display_privacy_policy(self):
        """Display privacy policy"""
        
        st.subheader("Privacy Policy")
        
        st.markdown("""
        ### Data Collection and Processing
        
        **Personal Data We Collect:**
        - Assessment responses and mental health screening data
        - Contact information (when provided voluntarily)
        - Usage analytics and platform interaction data
        - Consent records and preferences
        
        **Legal Basis for Processing:**
        - Consent for healthcare services (DPDPA 2023 Section 6)
        - Legitimate interest for platform improvement
        - Legal compliance requirements
        
        ### Data Protection Measures
        
        - AES-256 encryption for all sensitive data
        - Secure data transmission protocols
        - Regular security audits and compliance checks
        - Access controls and audit logging
        
        ### Data Retention
        
        - Assessment data: Retained as per healthcare regulations
        - Consent records: Maintained for legal compliance
        - Analytics data: Anonymized after 12 months
        
        ### Your Privacy Rights
        
        Under DPDPA 2023, you have the right to:
        - Access your personal data
        - Correct inaccurate information
        - Request deletion of your data
        - Data portability
        - Withdraw consent at any time
        """)
    
    def _display_disclaimers(self):
        """Display medical and legal disclaimers"""
        
        st.subheader("Important Disclaimers")
        
        st.error("""
        🚨 **MEDICAL DISCLAIMER**
        
        This platform provides AI-generated mental health screening results that are NOT medical diagnoses. 
        All results require validation by qualified mental health professionals.
        """)
        
        st.warning("""
        ⚠️ **NOT FOR EMERGENCY USE**
        
        This platform is not designed for crisis intervention or emergency mental health situations.
        
        **For Immediate Help:**
        - Emergency Services: 112
        - Tele MANAS: 1800-891-4416
        - National Helpline: 9152987821
        """)
        
        st.info("""
        📋 **AI TECHNOLOGY LIMITATIONS**
        
        - AI results are preliminary assessments only
        - Cultural and individual variations may not be fully captured
        - Professional clinical judgment is always required
        - Technology cannot replace human mental health professionals
        """)
    
    def _display_contact_information(self):
        """Display contact information for support and compliance"""
        
        st.subheader("Contact Information")
        
        st.markdown("""
        ### Data Protection Officer (DPO)
        **As required by DPDPA 2023**
        
        - **Email**: dpo@mentalhealthplatform.gov.in
        - **Phone**: +91-11-2345-6789
        - **Address**: Mental Health Platform DPO  
          Ministry of Health & Family Welfare  
          New Delhi - 110001
        - **Response Time**: Within 72 hours
        
        ### Technical Support
        
        - **Email**: support@mentalhealthplatform.gov.in
        - **Phone**: 1800-123-4567
        - **Hours**: 24/7 Support Available
        
        ### Grievance Redressal
        
        - **Email**: grievance@mentalhealthplatform.gov.in
        - **Phone**: +91-11-9876-5432
        - **Process**: As per DPDPA 2023 Section 32
        
        ### Crisis Support Resources
        
        - **Tele MANAS**: 1800-891-4416
        - **National Helpline**: 9152987821
        - **Emergency Services**: 112
        - **Poison Control**: 1066
        """)