import streamlit as st
import datetime
import json
from typing import Dict, Any
from security.encryption import EncryptionManager
from database.secure_storage import SecureStorage

class DPDPACompliance:
    """Digital Personal Data Protection Act (DPDPA) 2023 compliance manager"""
    
    def __init__(self):
        self.encryption_manager = EncryptionManager()
        self.secure_storage = SecureStorage()
        
    def display_compliance_info(self, language: str = 'english'):
        """Display DPDPA 2023 compliance information"""
        
        if language == 'hindi':
            self._display_hindi_compliance()
        else:
            self._display_english_compliance()
    
    def _display_english_compliance(self):
        """Display DPDPA compliance in English"""
        
        st.markdown("""
        ## Digital Personal Data Protection Act (DPDPA) 2023 Compliance
        
        ### Our Obligations Under DPDPA 2023
        
        #### Data Processing Lawfulness
        - **Legal Basis**: Healthcare services exemption under DPDPA 2023
        - **Purpose Limitation**: Data processed only for mental health diagnostic purposes
        - **Data Minimization**: Only necessary health information collected
        
        #### Your Rights as Data Principal
        - **Right to Information**: Clear notice about data processing
        - **Right of Access**: View your personal data we hold
        - **Right to Correction**: Update inaccurate information
        - **Right to Erasure**: Request data deletion (subject to healthcare retention requirements)
        - **Right to Grievance Redressal**: File complaints with our DPO
        
        #### Security Measures Implemented
        - **Encryption**: AES-256 encryption for all personal data
        - **Access Controls**: Role-based access to health information
        - **Audit Logging**: Complete trail of data access and modifications
        - **Breach Response**: 72-hour notification protocol as per Section 8(6)
        
        #### Data Sharing & Third Parties
        - **No Unauthorized Sharing**: Data shared only with explicit consent
        - **Vendor Agreements**: All third-party vendors have signed data protection agreements
        - **Cross-Border Transfer**: Data remains in India as per data residency requirements
        
        #### Children's Data Protection (Under 18)
        - **Verifiable Parental Consent**: Required for all minors as per Section 9
        - **Enhanced Protection**: No targeted advertising to children
        - **Healthcare Exemption**: Processing permitted for child health protection
        """)
    
    def _display_hindi_compliance(self):
        """Display DPDPA compliance in Hindi"""
        
        st.markdown("""
        ## डिजिटल व्यक्तिगत डेटा संरक्षण अधिनियम (DPDPA) 2023 अनुपालन
        
        ### DPDPA 2023 के तहत हमारे दायित्व
        
        #### डेटा प्रसंस्करण की वैधता
        - **कानूनी आधार**: DPDPA 2023 के तहत स्वास्थ्य सेवा छूट
        - **उद्देश्य सीमा**: डेटा केवल मानसिक स्वास्थ्य निदान के लिए प्रसंस्कृत
        - **डेटा न्यूनीकरण**: केवल आवश्यक स्वास्थ्य जानकारी एकत्र की गई
        
        #### डेटा प्रधान के रूप में आपके अधिकार
        - **जानकारी का अधिकार**: डेटा प्रसंस्करण के बारे में स्पष्ट सूचना
        - **पहुंच का अधिकार**: हमारे पास आपका व्यक्तिगत डेटा देखें
        - **सुधार का अधिकार**: गलत जानकारी अपडेट करें
        - **मिटाने का अधिकार**: डेटा हटाने का अनुरोध करें
        - **शिकायत निवारण का अधिकार**: हमारे DPO के साथ शिकायत दर्ज करें
        
        #### लागू सुरक्षा उपाय
        - **एन्क्रिप्शन**: सभी व्यक्तिगत डेटा के लिए AES-256 एन्क्रिप्शन
        - **पहुंच नियंत्रण**: स्वास्थ्य जानकारी तक भूमिका-आधारित पहुंच
        - **ऑडिट लॉगिंग**: डेटा पहुंच और संशोधन का पूरा ट्रेल
        - **उल्लंघन प्रतिक्रिया**: धारा 8(6) के अनुसार 72-घंटे की अधिसूचना प्रोटोकॉल
        """)
    
    def record_consent(self) -> bool:
        """Record user consent for data processing"""
        try:
            consent_record = {
                'timestamp': datetime.datetime.now().isoformat(),
                'consent_type': 'dpdpa_2023_healthcare',
                'consent_given': True,
                'ip_address': self._get_anonymized_ip(),
                'user_agent': 'streamlit_app',
                'legal_basis': 'healthcare_services_exemption',
                'retention_period': '7_years_medical_records'
            }
            
            # Encrypt and store consent
            encrypted_consent = self.encryption_manager.encrypt_data(consent_record)
            consent_id = self.secure_storage.store_consent(encrypted_consent)
            
            st.session_state.user_session['consent_id'] = consent_id
            return True
            
        except Exception as e:
            st.error(f"Error recording consent: {str(e)}")
            return False
    
    def display_data_subject_rights(self):
        """Display comprehensive data subject rights"""
        
        st.subheader("📋 Your Data Rights Under DPDPA 2023")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Access My Data"):
                self._handle_data_access_request()
            
            if st.button("✏️ Correct My Data"):
                self._handle_data_correction_request()
        
        with col2:
            if st.button("🗑️ Delete My Data"):
                self._handle_data_deletion_request()
            
            if st.button("📞 File Grievance"):
                self._display_grievance_form()
    
    def _handle_data_access_request(self):
        """Handle data access request"""
        st.info("📋 **Data Access Request**: Under DPDPA 2023, you have the right to access your personal data. Please contact our DPO at dpo@mentalhealthplatform.gov.in")
        
        st.markdown("""
        ### Data Categories We Hold:
        - Assessment responses (encrypted)
        - Consent records
        - Session metadata
        - Diagnostic reports
        - Crisis intervention records (if applicable)
        
        **Response Time**: Within 30 days as per DPDPA 2023
        """)
    
    def _handle_data_correction_request(self):
        """Handle data correction request"""
        st.info("✏️ **Data Correction Request**: You can request corrections to inaccurate personal data")
        
        correction_type = st.selectbox(
            "What would you like to correct?",
            ["Personal Information", "Assessment Responses", "Contact Details", "Other"]
        )
        
        correction_details = st.text_area("Please describe the correction needed:")
        
        if st.button("Submit Correction Request"):
            if correction_details:
                # Record correction request
                self._record_correction_request(correction_type, correction_details)
                st.success("✅ Correction request submitted. Our DPO will respond within 30 days.")
            else:
                st.error("Please provide correction details")
    
    def _handle_data_deletion_request(self):
        """Handle data deletion request"""
        st.warning("🗑️ **Data Deletion Request**: Please note that medical records may be subject to retention requirements under healthcare regulations")
        
        deletion_reason = st.selectbox(
            "Reason for deletion:",
            [
                "No longer need the service",
                "Withdraw consent",
                "Data no longer accurate",
                "Other"
            ]
        )
        
        st.info("⚠️ **Important**: Deletion of medical records may be subject to 7-year retention requirements under healthcare laws")
        
        if st.button("Request Data Deletion"):
            self._record_deletion_request(deletion_reason)
            st.success("✅ Deletion request submitted. Our DPO will review and respond within 30 days.")
    
    def _display_grievance_form(self):
        """Display grievance redressal form"""
        st.subheader("📞 Grievance Redressal Form")
        
        grievance_type = st.selectbox(
            "Type of Grievance:",
            [
                "Data Processing Complaint",
                "Privacy Violation",
                "Consent Issues",
                "Data Breach Concern",
                "Other"
            ]
        )
        
        grievance_details = st.text_area("Please describe your grievance in detail:")
        
        contact_preference = st.radio(
            "Preferred contact method:",
            ["Email", "Phone", "Post"]
        )
        
        if st.button("Submit Grievance"):
            if grievance_details:
                self._record_grievance(grievance_type, grievance_details, contact_preference)
                st.success("✅ Grievance submitted. Our DPO will respond within 72 hours as per DPDPA 2023.")
            else:
                st.error("Please provide grievance details")
    
    def _get_anonymized_ip(self) -> str:
        """Get anonymized IP address for logging"""
        # In production, this would get the actual IP and anonymize it
        return "xxx.xxx.xxx.xxx"
    
    def _record_correction_request(self, correction_type: str, details: str):
        """Record data correction request"""
        request_record = {
            'type': 'data_correction',
            'correction_type': correction_type,
            'details': details,
            'timestamp': datetime.datetime.now().isoformat(),
            'status': 'pending'
        }
        
        encrypted_request = self.encryption_manager.encrypt_data(request_record)
        self.secure_storage.store_request(encrypted_request)
    
    def _record_deletion_request(self, reason: str):
        """Record data deletion request"""
        request_record = {
            'type': 'data_deletion',
            'reason': reason,
            'timestamp': datetime.datetime.now().isoformat(),
            'status': 'pending_review',
            'note': 'Subject to healthcare record retention requirements'
        }
        
        encrypted_request = self.encryption_manager.encrypt_data(request_record)
        self.secure_storage.store_request(encrypted_request)
    
    def _record_grievance(self, grievance_type: str, details: str, contact_preference: str):
        """Record grievance for DPO review"""
        grievance_record = {
            'type': 'grievance',
            'grievance_type': grievance_type,
            'details': details,
            'contact_preference': contact_preference,
            'timestamp': datetime.datetime.now().isoformat(),
            'status': 'submitted',
            'dpo_response_due': (datetime.datetime.now() + datetime.timedelta(hours=72)).isoformat()
        }
        
        encrypted_grievance = self.encryption_manager.encrypt_data(grievance_record)
        self.secure_storage.store_grievance(encrypted_grievance)
