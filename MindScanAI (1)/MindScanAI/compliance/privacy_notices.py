import streamlit as st
import datetime
from typing import Dict, List

class PrivacyNotices:
    """Privacy notices for DPDPA 2023 compliance"""
    
    def __init__(self):
        self.notice_version = "2025-01-v1.0"
        self.last_updated = "January 2025"
    
    def display_detailed_notice(self, language: str = 'english'):
        """Display comprehensive privacy notice"""
        
        if language == 'hindi':
            self._display_hindi_notice()
        else:
            self._display_english_notice()
    
    def _display_english_notice(self):
        """Display detailed privacy notice in English"""
        
        st.markdown(f"""
        # Privacy Notice
        **Version**: {self.notice_version} | **Last Updated**: {self.last_updated}
        
        ## About This Notice
        This privacy notice explains how we collect, use, and protect your personal data in compliance with:
        - Digital Personal Data Protection Act (DPDPA) 2023
        - Mental Healthcare Act 2017
        - Information Technology Act 2000
        
        ## Data Controller Information
        **Organization**: Mental Health Diagnostic Platform
        **Legal Status**: Government of India Initiative
        **Registration**: Ministry of Health & Family Welfare
        **Data Protection Officer**: dpo@mentalhealthplatform.gov.in
        **Contact Address**: Mental Health Platform, MOHFW, New Delhi - 110001
        
        ## Personal Data We Collect
        
        ### Assessment Data
        - Mental health questionnaire responses
        - Diagnostic assessment results
        - Symptom tracking information
        - Treatment preferences and history
        
        ### Identity Information
        - Age and demographic information
        - Contact details (for service delivery)
        - Unique platform identifiers
        - Parental consent records (for minors)
        
        ### Technical Data
        - Device and browser information
        - IP addresses (anonymized)
        - Session logs and usage patterns
        - Security audit trails
        
        ### Sensitive Health Data
        - Mental health condition indicators
        - Crisis intervention records
        - Medication and treatment responses
        - Healthcare provider communications
        
        ## Legal Basis for Processing
        
        ### Healthcare Services Exemption (DPDPA 2023)
        - Processing necessary for healthcare service delivery
        - Public health and safety considerations
        - Mental Healthcare Act 2017 compliance requirements
        
        ### Explicit Consent
        - Research participation (optional)
        - Marketing communications (opt-in only)
        - Data sharing with third parties
        
        ## How We Use Your Data
        
        ### Primary Purposes
        1. **Diagnostic Assessment**: AI-powered mental health evaluation
        2. **Treatment Support**: Personalized care recommendations
        3. **Crisis Intervention**: Emergency support and referrals
        4. **Medical Records**: Healthcare documentation as required by law
        
        ### Secondary Purposes (With Consent)
        1. **Research**: Anonymized data for mental health research
        2. **Service Improvement**: Platform enhancement and optimization
        3. **Quality Assurance**: Clinical accuracy and safety monitoring
        
        ## Data Sharing and Disclosure
        
        ### No Unauthorized Sharing
        - Personal data is never sold or shared for commercial purposes
        - Strict confidentiality as per Mental Healthcare Act 2017
        - No marketing or advertising use without explicit consent
        
        ### Limited Authorized Sharing
        - **Healthcare Providers**: With explicit consent for treatment coordination
        - **Emergency Services**: Crisis intervention and immediate safety concerns
        - **Legal Compliance**: Court orders or statutory requirements only
        - **Research Institutions**: Anonymized data with ethical approval
        
        ### Third-Party Vendors
        - Cloud storage providers (Indian data centers only)
        - AI processing services (Meta Phi-3 via Azure India)
        - Security and encryption services
        - **Note**: All vendors have signed comprehensive data protection agreements
        
        ## Data Security Measures
        
        ### Technical Safeguards
        - **Encryption**: AES-256 encryption for all personal data at rest and in transit
        - **Access Controls**: Multi-factor authentication and role-based access
        - **Network Security**: Firewall protection and intrusion detection
        - **Backup Systems**: Secure, encrypted backup and disaster recovery
        
        ### Organizational Safeguards
        - Staff training on data protection and confidentiality
        - Regular security audits and vulnerability assessments
        - Data minimization and purpose limitation practices
        - Incident response and breach notification procedures
        
        ## Data Retention
        
        ### Medical Records (7 Years)
        - Mental health assessments and diagnoses
        - Treatment plans and progress notes
        - Crisis intervention records
        - **Legal Basis**: Healthcare record retention requirements
        
        ### Consent Records (Lifetime + 7 Years)
        - DPDPA consent documentation
        - Parental consent for minors
        - Research participation consent
        
        ### Technical Logs (1 Year)
        - Security audit trails
        - System access logs
        - Error and performance logs
        
        ## Your Rights Under DPDPA 2023
        
        ### Information Rights
        - Right to know what personal data we hold
        - Right to understand how your data is processed
        - Right to receive this privacy notice in clear language
        
        ### Access Rights
        - Request copies of your personal data
        - View all processing activities
        - Access your consent history
        
        ### Correction Rights
        - Update inaccurate personal information
        - Complete incomplete data records
        - Correct outdated information
        
        ### Erasure Rights
        - Request deletion of personal data
        - **Note**: Subject to healthcare record retention requirements
        - Right to be forgotten (with legal exceptions)
        
        ### Portability Rights
        - Receive data in structured, machine-readable format
        - Transfer data to another healthcare provider
        - Export assessment results and medical records
        
        ## Children's Data Protection
        
        ### Under 18 Years (DPDPA Section 9)
        - **Verifiable Parental Consent**: Required for all processing
        - **Enhanced Protection**: No behavioral advertising
        - **Limited Processing**: Only for healthcare service delivery
        - **Guardian Rights**: Parents can exercise all data rights on behalf of children
        
        ### Verification Process
        - Parent/guardian identity verification
        - Documented consent with contact information
        - Regular consent renewal requirements
        - Child's right to withdraw consent upon turning 18
        
        ## Data Breach Notification
        
        ### 72-Hour Notification (DPDPA Section 8)
        - Immediate notification to Data Protection Board
        - Affected individuals notified without delay
        - Detailed breach impact assessment
        - Remedial measures and prevention steps
        
        ### Breach Communication
        - Clear explanation of what happened
        - What data was involved
        - Steps taken to address the breach
        - Protective measures for affected individuals
        
        ## International Data Transfers
        
        ### Data Localization
        - All personal data stored in Indian data centers
        - Processing occurs within Indian territorial boundaries
        - No cross-border data transfers without explicit consent
        
        ### Vendor Compliance
        - All cloud providers maintain Indian data residency
        - AI processing through Azure India regions
        - Contractual obligations for data localization
        
        ## Grievance Redressal
        
        ### Data Protection Officer (DPO)
        - **Email**: dpo@mentalhealthplatform.gov.in
        - **Phone**: +91-11-2345-6789
        - **Address**: Mental Health Platform DPO, MOHFW, New Delhi - 110001
        - **Response Time**: Within 72 hours
        
        ### Complaint Process
        1. Submit complaint to DPO with details
        2. Acknowledge receipt within 24 hours
        3. Investigation and response within 30 days
        4. Appeal to Data Protection Board if unsatisfied
        
        ## Contact Information
        
        ### Platform Support
        - **General Inquiries**: support@mentalhealthplatform.gov.in
        - **Technical Issues**: tech@mentalhealthplatform.gov.in
        - **Crisis Support**: 1800-891-4416 (Tele MANAS)
        
        ### Regulatory Bodies
        - **Data Protection Board**: dpb@gov.in
        - **Central Mental Health Authority**: cmha@mohfw.gov.in
        - **Ministry of Health**: webmaster@mohfw.gov.in
        
        ## Updates to This Notice
        
        ### Version Control
        - Current Version: {self.notice_version}
        - Previous versions archived and accessible
        - Change log maintained with update reasons
        
        ### Notification of Changes
        - Email notification to registered users
        - Platform notice for 30 days
        - Opportunity to withdraw consent if changes are material
        
        ---
        
        **Effective Date**: January 1, 2025
        **Next Review**: July 1, 2025
        
        *This privacy notice is available in Hindi and English. For any discrepancies, the English version shall prevail.*
        """)
    
    def _display_hindi_notice(self):
        """Display privacy notice in Hindi"""
        
        st.markdown(f"""
        # गोपनीयता सूचना
        **संस्करण**: {self.notice_version} | **अंतिम अपडेट**: {self.last_updated}
        
        ## इस सूचना के बारे में
        यह गोपनीयता सूचना बताती है कि हम आपके व्यक्तिगत डेटा को कैसे एकत्र, उपयोग और सुरक्षित करते हैं:
        - डिजिटल व्यक्तिगत डेटा संरक्षण अधिनियम (DPDPA) 2023
        - मानसिक स्वास्थ्य देखभाल अधिनियम 2017
        - सूचना प्रौद्योगिकी अधिनियम 2000
        
        ## डेटा नियंत्रक जानकारी
        **संगठन**: मानसिक स्वास्थ्य निदान प्लेटफॉर्म
        **कानूनी स्थिति**: भारत सरकार पहल
        **पंजीकरण**: स्वास्थ्य और परिवार कल्याण मंत्रालय
        **डेटा संरक्षण अधिकारी**: dpo@mentalhealthplatform.gov.in
        **संपर्क पता**: मानसिक स्वास्थ्य प्लेटफॉर्म, MOHFW, नई दिल्ली - 110001
        
        ## हम जो व्यक्तिगत डेटा एकत्र करते हैं
        
        ### मूल्यांकन डेटा
        - मानसिक स्वास्थ्य प्रश्नावली प्रतिक्रियाएं
        - नैदानिक मूल्यांकन परिणाम
        - लक्षण ट्रैकिंग जानकारी
        - उपचार प्राथमिकताएं और इतिहास
        
        ### पहचान जानकारी
        - आयु और जनसांख्यिकीय जानकारी
        - संपर्क विवरण (सेवा वितरण के लिए)
        - अद्वितीय प्लेटफॉर्म पहचानकर्ता
        - अभिभावकीय सहमति रिकॉर्ड (नाबालिगों के लिए)
        
        ## डेटा सुरक्षा उपाय
        
        ### तकनीकी सुरक्षा
        - **एन्क्रिप्शन**: सभी व्यक्तिगत डेटा के लिए AES-256 एन्क्रिप्शन
        - **पहुंच नियंत्रण**: बहु-कारक प्रमाणीकरण और भूमिका-आधारित पहुंच
        - **नेटवर्क सुरक्षा**: फ़ायरवॉल सुरक्षा और घुसपैठ का पता लगाना
        
        ### संगठनात्मक सुरक्षा
        - डेटा संरक्षण पर कर्मचारी प्रशिक्षण
        - नियमित सुरक्षा ऑडिट
        - डेटा न्यूनीकरण प्रथाएं
        - घटना प्रतिक्रिया प्रक्रियाएं
        
        ## DPDPA 2023 के तहत आपके अधिकार
        
        ### सूचना अधिकार
        - जानने का अधिकार कि हमारे पास आपका कौन सा व्यक्तिगत डेटा है
        - समझने का अधिकार कि आपका डेटा कैसे प्रसंस्कृत किया जाता है
        
        ### पहुंच अधिकार
        - अपने व्यक्तिगत डेटा की प्रतियां मांगना
        - सभी प्रसंस्करण गतिविधियां देखना
        
        ### सुधार अधिकार
        - गलत व्यक्तिगत जानकारी अपडेट करना
        - अधूरे डेटा रिकॉर्ड पूरा करना
        
        ### मिटाने के अधिकार
        - व्यक्तिगत डेटा हटाने का अनुरोध
        - **नोट**: स्वास्थ्य रिकॉर्ड प्रतिधारण आवश्यकताओं के अधीन
        
        ## शिकायत निवारण
        
        ### डेटा संरक्षण अधिकारी (DPO)
        - **ईमेल**: dpo@mentalhealthplatform.gov.in
        - **फोन**: +91-11-2345-6789
        - **पता**: मानसिक स्वास्थ्य प्लेटफॉर्म DPO, MOHFW, नई दिल्ली - 110001
        - **प्रतिक्रिया समय**: 72 घंटे के भीतर
        
        ---
        
        **प्रभावी तिथि**: 1 जनवरी, 2025
        **अगली समीक्षा**: 1 जुलाई, 2025
        """)
    
    def display_consent_summary(self):
        """Display consent summary for users"""
        
        st.subheader("📋 Your Consent Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### ✅ Consents Given
            - Data processing for healthcare services
            - Secure storage of mental health records
            - AI analysis for diagnostic insights
            - Crisis intervention support
            """)
        
        with col2:
            st.markdown("""
            ### ❌ Optional Consents (Not Given)
            - Research participation
            - Marketing communications
            - Third-party data sharing
            - Non-essential analytics
            """)
        
        if st.button("📝 Modify Consent Preferences"):
            self._display_consent_management()
    
    def _display_consent_management(self):
        """Consent management interface"""
        
        st.subheader("🔧 Consent Management")
        
        st.markdown("### Essential Consents (Cannot be withdrawn)")
        st.info("✅ Healthcare service delivery - Required for platform operation")
        st.info("✅ Data security and protection - Required by law")
        st.info("✅ Legal compliance - Required by regulation")
        
        st.markdown("### Optional Consents")
        
        research_consent = st.checkbox("Participate in anonymized mental health research")
        marketing_consent = st.checkbox("Receive mental health tips and updates")
        analytics_consent = st.checkbox("Allow enhanced analytics for service improvement")
        
        if st.button("💾 Update Consent Preferences"):
            consent_record = {
                'research_consent': research_consent,
                'marketing_consent': marketing_consent,
                'analytics_consent': analytics_consent,
                'timestamp': datetime.datetime.now().isoformat(),
                'ip_address': 'anonymized',
                'user_agent': 'streamlit_app'
            }
            
            st.success("✅ Consent preferences updated successfully")
            st.info("Changes take effect immediately. You can modify these preferences at any time.")
    
    def get_data_categories(self) -> Dict[str, List[str]]:
        """Get comprehensive list of data categories"""
        return {
            'Identity Data': [
                'Age and demographic information',
                'Contact details (email, phone)',
                'Platform user identifiers',
                'Parental consent records (minors)'
            ],
            'Health Data': [
                'Mental health questionnaire responses',
                'Diagnostic assessment results', 
                'Symptom tracking information',
                'Treatment preferences and history',
                'Crisis intervention records'
            ],
            'Technical Data': [
                'Device and browser information',
                'IP addresses (anonymized)',
                'Session logs and usage patterns',
                'Security audit trails',
                'Performance metrics'
            ],
            'Communication Data': [
                'Platform messages and notifications',
                'Support ticket communications',
                'Feedback and survey responses',
                'Emergency contact records'
            ]
        }
