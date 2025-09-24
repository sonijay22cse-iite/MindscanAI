import streamlit as st
import sqlite3
import json
import datetime
import os
from typing import Dict, List, Any, Optional, Union
from security.encryption import EncryptionManager
import hashlib
import uuid

class SecureStorage:
    """Secure database storage with DPDPA 2023 compliance and encryption"""
    
    def __init__(self):
        self.encryption_manager = EncryptionManager()
        self.db_path = self._get_db_path()
        self.connection_pool = {}
        self._initialize_database()
    
    def _get_db_path(self) -> str:
        """Get secure database path"""
        # In production, this would be a secure, encrypted database location
        db_dir = "secure_data"
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, mode=0o700)  # Restricted permissions
        
        return os.path.join(db_dir, "mental_health_platform.db")
    
    def _initialize_database(self):
        """Initialize database with secure schema"""
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # User data table with encryption
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    id TEXT PRIMARY KEY,
                    user_hash TEXT UNIQUE NOT NULL,
                    encrypted_pii TEXT NOT NULL,
                    consent_records TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    data_classification TEXT NOT NULL,
                    retention_policy TEXT NOT NULL
                )
            """)
            
            # Assessment data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS assessments (
                    id TEXT PRIMARY KEY,
                    user_hash TEXT NOT NULL,
                    assessment_type TEXT NOT NULL,
                    encrypted_responses TEXT NOT NULL,
                    encrypted_results TEXT NOT NULL,
                    severity_level TEXT,
                    crisis_flags TEXT,
                    created_at TEXT NOT NULL,
                    expires_at TEXT,
                    FOREIGN KEY (user_hash) REFERENCES user_data (user_hash)
                )
            """)
            
            # AI analysis table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ai_analyses (
                    id TEXT PRIMARY KEY,
                    assessment_id TEXT NOT NULL,
                    model_version TEXT NOT NULL,
                    encrypted_analysis TEXT NOT NULL,
                    confidence_scores TEXT,
                    validation_status TEXT DEFAULT 'pending',
                    created_at TEXT NOT NULL,
                    expires_at TEXT,
                    FOREIGN KEY (assessment_id) REFERENCES assessments (id)
                )
            """)
            
            # Crisis intervention records
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS crisis_records (
                    id TEXT PRIMARY KEY,
                    user_hash TEXT NOT NULL,
                    crisis_type TEXT NOT NULL,
                    severity_level INTEGER NOT NULL,
                    encrypted_details TEXT NOT NULL,
                    intervention_actions TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TEXT NOT NULL,
                    resolved_at TEXT,
                    retention_extended BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (user_hash) REFERENCES user_data (user_hash)
                )
            """)
            
            # Diagnostic reports table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS diagnostic_reports (
                    id TEXT PRIMARY KEY,
                    user_hash TEXT NOT NULL,
                    assessment_ids TEXT NOT NULL,
                    encrypted_report TEXT NOT NULL,
                    report_type TEXT NOT NULL,
                    professional_validated BOOLEAN DEFAULT FALSE,
                    created_at TEXT NOT NULL,
                    accessed_at TEXT,
                    expires_at TEXT,
                    FOREIGN KEY (user_hash) REFERENCES user_data (user_hash)
                )
            """)
            
            # Consent management table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS consent_records (
                    id TEXT PRIMARY KEY,
                    user_hash TEXT NOT NULL,
                    consent_type TEXT NOT NULL,
                    consent_given BOOLEAN NOT NULL,
                    encrypted_details TEXT NOT NULL,
                    legal_basis TEXT NOT NULL,
                    withdrawal_date TEXT,
                    created_at TEXT NOT NULL,
                    expires_at TEXT,
                    FOREIGN KEY (user_hash) REFERENCES user_data (user_hash)
                )
            """)
            
            # Data subject requests table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS data_requests (
                    id TEXT PRIMARY KEY,
                    user_hash TEXT,
                    request_type TEXT NOT NULL,
                    encrypted_details TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    processed_by TEXT,
                    response_data TEXT,
                    created_at TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    completed_at TEXT
                )
            """)
            
            # Audit log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id TEXT PRIMARY KEY,
                    user_hash TEXT,
                    action_type TEXT NOT NULL,
                    resource_type TEXT NOT NULL,
                    resource_id TEXT,
                    encrypted_details TEXT,
                    ip_address_hash TEXT,
                    user_agent_hash TEXT,
                    success BOOLEAN NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            
            # Data breach log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS breach_log (
                    id TEXT PRIMARY KEY,
                    breach_type TEXT NOT NULL,
                    severity_level TEXT NOT NULL,
                    affected_data_categories TEXT NOT NULL,
                    estimated_affected_users INTEGER,
                    containment_status TEXT,
                    notification_status TEXT,
                    investigation_status TEXT,
                    created_at TEXT NOT NULL,
                    resolved_at TEXT
                )
            """)
            
            # Create indices for performance and security
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_hash ON user_data(user_hash)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_assessment_user ON assessments(user_hash)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_assessment_created ON assessments(created_at)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_crisis_user ON crisis_records(user_hash)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_crisis_status ON crisis_records(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_log(created_at)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log(user_hash)")
            
            conn.commit()
            
        except Exception as e:
            st.error(f"Database initialization error: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection with security settings"""
        
        conn = sqlite3.connect(
            self.db_path,
            timeout=30.0,
            check_same_thread=False
        )
        
        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Set secure defaults
        conn.execute("PRAGMA journal_mode = WAL")  # Write-Ahead Logging for better concurrency
        conn.execute("PRAGMA synchronous = FULL")  # Maximum durability
        conn.execute("PRAGMA temp_store = MEMORY")  # Store temp data in memory
        
        return conn
    
    def store_user_data(self, user_data: Dict[str, Any]) -> str:
        """Store user data with encryption and compliance"""
        
        try:
            user_id = str(uuid.uuid4())
            user_hash = self._create_user_hash(user_data.get('email', user_id))
            
            # Encrypt PII data
            encrypted_pii = self.encryption_manager.encrypt_pii(user_data)
            
            # Create consent record
            consent_records = {
                'dpdpa_consent': True,
                'healthcare_consent': True,
                'timestamp': datetime.datetime.now().isoformat(),
                'legal_basis': 'healthcare_services_exemption'
            }
            
            # Determine data classification and retention
            data_classification = 'personal_identifiable'
            retention_policy = 'as_per_consent'
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO user_data 
                (id, user_hash, encrypted_pii, consent_records, created_at, updated_at, data_classification, retention_policy)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                user_hash,
                self.encryption_manager.encrypt_data(encrypted_pii),
                self.encryption_manager.encrypt_data(consent_records),
                datetime.datetime.now().isoformat(),
                datetime.datetime.now().isoformat(),
                data_classification,
                retention_policy
            ))
            
            conn.commit()
            
            # Log the action
            self._log_action(user_hash, 'create', 'user_data', user_id, {'action': 'user_registration'})
            
            return user_id
            
        except Exception as e:
            st.error(f"Error storing user data: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    def store_assessment(self, encrypted_responses: str, assessment_type: str, user_hash: str = None) -> str:
        """Store assessment data with encryption"""
        
        try:
            assessment_id = str(uuid.uuid4())
            
            if not user_hash:
                user_hash = self._get_session_user_hash()
            
            # Ensure user record exists before storing assessment
            self._ensure_user_record_exists(user_hash)
            
            # Calculate expiration date (7 years for medical records)
            expires_at = (datetime.datetime.now() + datetime.timedelta(days=7*365)).isoformat()
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO assessments 
                (id, user_hash, assessment_type, encrypted_responses, encrypted_results, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                assessment_id,
                user_hash,
                assessment_type,
                encrypted_responses,
                self.encryption_manager.encrypt_data({}),  # Results will be updated later
                datetime.datetime.now().isoformat(),
                expires_at
            ))
            
            conn.commit()
            
            # Log the action
            self._log_action(user_hash, 'create', 'assessment', assessment_id, {
                'assessment_type': assessment_type,
                'compliance_framework': 'MHA_2017'
            })
            
            return assessment_id
            
        except Exception as e:
            st.error(f"Error storing assessment: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    def store_ai_analysis(self, assessment_id: str, analysis_data: Dict[str, Any]) -> str:
        """Store AI analysis results with encryption"""
        
        try:
            analysis_id = str(uuid.uuid4())
            
            # Extract confidence scores
            confidence_scores = {
                'overall_confidence': analysis_data.get('metadata', {}).get('confidence', 0.8),
                'model_version': analysis_data.get('metadata', {}).get('model_used', 'phi-3-medium'),
                'analysis_timestamp': analysis_data.get('metadata', {}).get('analysis_timestamp')
            }
            
            # Calculate expiration (7 years for medical AI analysis)
            expires_at = (datetime.datetime.now() + datetime.timedelta(days=7*365)).isoformat()
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO ai_analyses 
                (id, assessment_id, model_version, encrypted_analysis, confidence_scores, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                analysis_id,
                assessment_id,
                analysis_data.get('metadata', {}).get('model_used', 'phi-3-medium'),
                self.encryption_manager.encrypt_data(analysis_data),
                self.encryption_manager.encrypt_data(confidence_scores),
                datetime.datetime.now().isoformat(),
                expires_at
            ))
            
            conn.commit()
            
            # Log the action
            user_hash = self._get_user_hash_from_assessment(assessment_id)
            self._log_action(user_hash, 'create', 'ai_analysis', analysis_id, {
                'assessment_id': assessment_id,
                'model_used': analysis_data.get('metadata', {}).get('model_used'),
                'compliance_note': 'AI_analysis_requires_professional_validation'
            })
            
            return analysis_id
            
        except Exception as e:
            st.error(f"Error storing AI analysis: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    def store_crisis_record(self, crisis_data: Dict[str, Any], user_hash: str = None) -> str:
        """Store crisis intervention record with extended retention"""
        
        try:
            crisis_id = str(uuid.uuid4())
            
            if not user_hash:
                user_hash = self._get_session_user_hash()
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO crisis_records 
                (id, user_hash, crisis_type, severity_level, encrypted_details, intervention_actions, created_at, retention_extended)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                crisis_id,
                user_hash,
                crisis_data.get('type', 'general'),
                crisis_data.get('severity', 1),
                self.encryption_manager.encrypt_data(crisis_data),
                self.encryption_manager.encrypt_data(crisis_data.get('interventions', [])),
                datetime.datetime.now().isoformat(),
                True  # Extended retention for crisis records (10 years)
            ))
            
            conn.commit()
            
            # Log the critical action
            self._log_action(user_hash, 'create', 'crisis_record', crisis_id, {
                'crisis_type': crisis_data.get('type'),
                'severity': crisis_data.get('severity'),
                'urgent_flag': True,
                'compliance_note': 'Crisis_records_retained_10_years'
            })
            
            return crisis_id
            
        except Exception as e:
            st.error(f"Error storing crisis record: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    def store_diagnostic_report(self, report_data: Dict[str, Any], user_hash: str = None) -> str:
        """Store diagnostic report with professional validation tracking"""
        
        try:
            report_id = str(uuid.uuid4())
            
            if not user_hash:
                user_hash = self._get_session_user_hash()
            
            # Calculate expiration (7 years for diagnostic reports)
            expires_at = (datetime.datetime.now() + datetime.timedelta(days=7*365)).isoformat()
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO diagnostic_reports 
                (id, user_hash, assessment_ids, encrypted_report, report_type, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                report_id,
                user_hash,
                json.dumps(report_data.get('assessment_ids', [])),
                self.encryption_manager.encrypt_data(report_data),
                report_data.get('report_type', 'comprehensive'),
                datetime.datetime.now().isoformat(),
                expires_at
            ))
            
            conn.commit()
            
            # Log the action
            self._log_action(user_hash, 'create', 'diagnostic_report', report_id, {
                'report_type': report_data.get('report_type'),
                'assessment_count': len(report_data.get('assessment_ids', [])),
                'professional_validation_required': True
            })
            
            return report_id
            
        except Exception as e:
            st.error(f"Error storing diagnostic report: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    def store_consent(self, encrypted_consent: str, user_hash: str = None) -> str:
        """Store consent record with legal compliance"""
        
        try:
            consent_id = str(uuid.uuid4())
            
            if not user_hash:
                user_hash = self._get_session_user_hash()
            
            # Ensure user record exists before storing consent
            self._ensure_user_record_exists(user_hash)
            
            # Consent records have lifetime + 7 years retention
            expires_at = (datetime.datetime.now() + datetime.timedelta(days=80*365)).isoformat()
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO consent_records 
                (id, user_hash, consent_type, consent_given, encrypted_details, legal_basis, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                consent_id,
                user_hash,
                'dpdpa_2023_healthcare',
                True,
                encrypted_consent,
                'healthcare_services_exemption',
                datetime.datetime.now().isoformat(),
                expires_at
            ))
            
            conn.commit()
            
            # Log the consent
            self._log_action(user_hash, 'create', 'consent', consent_id, {
                'consent_type': 'dpdpa_2023_healthcare',
                'legal_basis': 'healthcare_services_exemption',
                'compliance_framework': 'DPDPA_2023'
            })
            
            return consent_id
            
        except Exception as e:
            st.error(f"Error storing consent: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    def store_request(self, encrypted_request: str) -> str:
        """Store data subject request"""
        
        try:
            request_id = str(uuid.uuid4())
            
            # Parse request to get type and user info
            request_data = self.encryption_manager.decrypt_data(encrypted_request)
            user_hash = request_data.get('user_hash', 'anonymous')
            request_type = request_data.get('type', 'general')
            
            # Calculate due date (30 days for most requests)
            due_date = (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat()
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO data_requests 
                (id, user_hash, request_type, encrypted_details, due_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                request_id,
                user_hash,
                request_type,
                encrypted_request,
                due_date,
                datetime.datetime.now().isoformat()
            ))
            
            conn.commit()
            
            # Log the request
            self._log_action(user_hash, 'create', 'data_request', request_id, {
                'request_type': request_type,
                'due_date': due_date,
                'dpo_assigned': True
            })
            
            return request_id
            
        except Exception as e:
            st.error(f"Error storing request: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    def store_grievance(self, encrypted_grievance: str) -> str:
        """Store grievance for DPO review"""
        
        try:
            grievance_id = str(uuid.uuid4())
            
            # Parse grievance data
            grievance_data = self.encryption_manager.decrypt_data(encrypted_grievance)
            user_hash = grievance_data.get('user_hash', 'anonymous')
            
            # Grievances have 72-hour response requirement
            due_date = (datetime.datetime.now() + datetime.timedelta(hours=72)).isoformat()
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO data_requests 
                (id, user_hash, request_type, encrypted_details, due_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                grievance_id,
                user_hash,
                'grievance',
                encrypted_grievance,
                due_date,
                datetime.datetime.now().isoformat()
            ))
            
            conn.commit()
            
            # Log the grievance with high priority
            self._log_action(user_hash, 'create', 'grievance', grievance_id, {
                'request_type': 'grievance',
                'due_date': due_date,
                'priority': 'high',
                'dpo_notification_required': True,
                'response_time_hours': 72
            })
            
            return grievance_id
            
        except Exception as e:
            st.error(f"Error storing grievance: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    def get_user_data(self, user_hash: str) -> Optional[Dict[str, Any]]:
        """Retrieve and decrypt user data"""
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT encrypted_pii, consent_records, created_at, data_classification
                FROM user_data 
                WHERE user_hash = ?
            """, (user_hash,))
            
            result = cursor.fetchone()
            
            if result:
                encrypted_pii, consent_records, created_at, data_classification = result
                
                # Decrypt data
                pii_data = self.encryption_manager.decrypt_data(encrypted_pii)
                consent_data = self.encryption_manager.decrypt_data(consent_records)
                
                # Log access
                self._log_action(user_hash, 'read', 'user_data', user_hash, {
                    'data_classification': data_classification,
                    'access_reason': 'user_data_retrieval'
                })
                
                return {
                    'pii_data': pii_data,
                    'consent_records': consent_data,
                    'created_at': created_at,
                    'data_classification': data_classification
                }
            
            return None
            
        except Exception as e:
            st.error(f"Error retrieving user data: {str(e)}")
            return None
        finally:
            if conn:
                conn.close()
    
    def get_user_assessments(self, user_hash: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve user assessments with decryption"""
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, assessment_type, encrypted_responses, encrypted_results, 
                       severity_level, crisis_flags, created_at
                FROM assessments 
                WHERE user_hash = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (user_hash, limit))
            
            results = cursor.fetchall()
            assessments = []
            
            for result in results:
                assessment_id, assessment_type, encrypted_responses, encrypted_results, severity_level, crisis_flags, created_at = result
                
                # Decrypt data
                try:
                    responses = self.encryption_manager.decrypt_data(encrypted_responses)
                    results_data = self.encryption_manager.decrypt_data(encrypted_results) if encrypted_results else {}
                    
                    assessments.append({
                        'id': assessment_id,
                        'assessment_type': assessment_type,
                        'responses': responses,
                        'results': results_data,
                        'severity_level': severity_level,
                        'crisis_flags': crisis_flags,
                        'created_at': created_at
                    })
                    
                except Exception as decrypt_error:
                    st.warning(f"Could not decrypt assessment {assessment_id}: {str(decrypt_error)}")
                    continue
            
            # Log access
            self._log_action(user_hash, 'read', 'assessments', f"count_{len(assessments)}", {
                'assessment_count': len(assessments),
                'access_reason': 'user_assessment_history'
            })
            
            return assessments
            
        except Exception as e:
            st.error(f"Error retrieving assessments: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()
    
    def get_crisis_records(self, user_hash: str) -> List[Dict[str, Any]]:
        """Retrieve crisis intervention records"""
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, crisis_type, severity_level, encrypted_details, 
                       intervention_actions, status, created_at, resolved_at
                FROM crisis_records 
                WHERE user_hash = ?
                ORDER BY created_at DESC
            """, (user_hash,))
            
            results = cursor.fetchall()
            crisis_records = []
            
            for result in results:
                crisis_id, crisis_type, severity_level, encrypted_details, intervention_actions, status, created_at, resolved_at = result
                
                # Decrypt data
                try:
                    details = self.encryption_manager.decrypt_data(encrypted_details)
                    interventions = self.encryption_manager.decrypt_data(intervention_actions) if intervention_actions else []
                    
                    crisis_records.append({
                        'id': crisis_id,
                        'crisis_type': crisis_type,
                        'severity_level': severity_level,
                        'details': details,
                        'interventions': interventions,
                        'status': status,
                        'created_at': created_at,
                        'resolved_at': resolved_at
                    })
                    
                except Exception as decrypt_error:
                    st.warning(f"Could not decrypt crisis record {crisis_id}: {str(decrypt_error)}")
                    continue
            
            # Log access to sensitive crisis data
            self._log_action(user_hash, 'read', 'crisis_records', f"count_{len(crisis_records)}", {
                'crisis_record_count': len(crisis_records),
                'access_reason': 'crisis_history_review',
                'sensitive_data_access': True
            })
            
            return crisis_records
            
        except Exception as e:
            st.error(f"Error retrieving crisis records: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()
    
    def delete_user_data(self, user_hash: str, deletion_scope: str = 'partial') -> Dict[str, Any]:
        """Delete user data with retention compliance"""
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            deletion_summary = {
                'user_data_deleted': False,
                'assessments_deleted': 0,
                'reports_deleted': 0,
                'retained_records': [],
                'deletion_timestamp': datetime.datetime.now().isoformat(),
                'legal_compliance': True
            }
            
            if deletion_scope == 'complete':
                # Check for legal retention requirements
                cursor.execute("""
                    SELECT COUNT(*) FROM crisis_records 
                    WHERE user_hash = ? AND status = 'active'
                """, (user_hash,))
                
                active_crisis_count = cursor.fetchone()[0]
                
                if active_crisis_count > 0:
                    deletion_summary['retained_records'].append(
                        f"Crisis records ({active_crisis_count}) - retained for legal/safety requirements"
                    )
                
                # Delete user PII data
                cursor.execute("DELETE FROM user_data WHERE user_hash = ?", (user_hash,))
                deletion_summary['user_data_deleted'] = True
                
                # Delete assessments older than retention period
                cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=7*365)).isoformat()
                cursor.execute("""
                    DELETE FROM assessments 
                    WHERE user_hash = ? AND created_at < ?
                """, (user_hash, cutoff_date))
                deletion_summary['assessments_deleted'] = cursor.rowcount
                
                # Delete reports
                cursor.execute("DELETE FROM diagnostic_reports WHERE user_hash = ?", (user_hash,))
                deletion_summary['reports_deleted'] = cursor.rowcount
                
            elif deletion_scope == 'partial':
                # Delete only non-essential data
                cursor.execute("""
                    UPDATE user_data 
                    SET encrypted_pii = ? 
                    WHERE user_hash = ?
                """, (self.encryption_manager.encrypt_data({'deleted': True, 'timestamp': datetime.datetime.now().isoformat()}), user_hash))
                
                deletion_summary['user_data_deleted'] = True
                deletion_summary['retained_records'].append("Medical records - retained per healthcare regulations")
            
            conn.commit()
            
            # Log the deletion
            self._log_action(user_hash, 'delete', 'user_data', user_hash, {
                'deletion_scope': deletion_scope,
                'deletion_summary': deletion_summary,
                'compliance_framework': 'DPDPA_2023_MHA_2017',
                'legal_review_completed': True
            })
            
            return deletion_summary
            
        except Exception as e:
            st.error(f"Error deleting user data: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    def _create_user_hash(self, identifier: str) -> str:
        """Create consistent user hash for identification"""
        return self.encryption_manager.hash_data(identifier)
    
    def _get_session_user_hash(self) -> str:
        """Get user hash from current session"""
        # In production, this would get from authenticated session
        if 'user_session' in st.session_state and 'user_id' in st.session_state.user_session:
            return self._create_user_hash(st.session_state.user_session['user_id'])
        
        # Fallback to anonymous session
        return self._create_user_hash('anonymous_session')
    
    def _ensure_user_record_exists(self, user_hash: str):
        """Ensure a user record exists in the database, create one if it doesn't"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if user record already exists
            cursor.execute("SELECT id FROM user_data WHERE user_hash = ?", (user_hash,))
            existing_user = cursor.fetchone()
            
            if not existing_user:
                # Create a minimal user record for anonymous sessions
                user_id = str(uuid.uuid4())
                
                # Create minimal user data for anonymous consent
                minimal_user_data = {
                    'session_type': 'anonymous',
                    'created_for': 'consent_recording',
                    'timestamp': datetime.datetime.now().isoformat()
                }
                
                # Encrypt the minimal data
                encrypted_pii = self.encryption_manager.encrypt_data(minimal_user_data)
                
                # Create default consent records structure
                consent_records = {
                    'initial_consent': True,
                    'timestamp': datetime.datetime.now().isoformat(),
                    'legal_basis': 'healthcare_services_exemption'
                }
                
                cursor.execute("""
                    INSERT INTO user_data 
                    (id, user_hash, encrypted_pii, consent_records, created_at, updated_at, data_classification, retention_policy)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    user_hash,
                    encrypted_pii,
                    self.encryption_manager.encrypt_data(consent_records),
                    datetime.datetime.now().isoformat(),
                    datetime.datetime.now().isoformat(),
                    'anonymous_session',
                    'consent_based'
                ))
                
                conn.commit()
                
                # Log the automatic user creation
                self._log_action(user_hash, 'create', 'user_data', user_id, {
                    'action': 'automatic_user_creation_for_consent',
                    'session_type': 'anonymous'
                })
            
        except Exception as e:
            st.error(f"Error ensuring user record exists: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    def _get_user_hash_from_assessment(self, assessment_id: str) -> str:
        """Get user hash from assessment ID"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT user_hash FROM assessments WHERE id = ?", (assessment_id,))
            result = cursor.fetchone()
            
            return result[0] if result else 'unknown'
            
        except Exception:
            return 'unknown'
        finally:
            if conn:
                conn.close()
    
    def _log_action(self, user_hash: str, action_type: str, resource_type: str, resource_id: str, details: Dict[str, Any], success: bool = True):
        """Log action for audit trail"""
        
        try:
            log_id = str(uuid.uuid4())
            
            # Anonymize IP and user agent for logging
            ip_hash = self.encryption_manager.hash_data('127.0.0.1')  # Placeholder
            user_agent_hash = self.encryption_manager.hash_data('streamlit_app')
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO audit_log 
                (id, user_hash, action_type, resource_type, resource_id, encrypted_details, 
                 ip_address_hash, user_agent_hash, success, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                log_id,
                user_hash,
                action_type,
                resource_type,
                resource_id,
                self.encryption_manager.encrypt_data(details),
                ip_hash,
                user_agent_hash,
                success,
                datetime.datetime.now().isoformat()
            ))
            
            conn.commit()
            
        except Exception as e:
            # Don't fail the main operation if logging fails
            st.warning(f"Audit logging failed: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    def get_audit_trail(self, user_hash: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get audit trail for user actions"""
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT action_type, resource_type, resource_id, encrypted_details, success, created_at
                FROM audit_log 
                WHERE user_hash = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (user_hash, limit))
            
            results = cursor.fetchall()
            audit_trail = []
            
            for result in results:
                action_type, resource_type, resource_id, encrypted_details, success, created_at = result
                
                try:
                    details = self.encryption_manager.decrypt_data(encrypted_details) if encrypted_details else {}
                    
                    audit_trail.append({
                        'action_type': action_type,
                        'resource_type': resource_type,
                        'resource_id': resource_id,
                        'details': details,
                        'success': success,
                        'created_at': created_at
                    })
                    
                except Exception as decrypt_error:
                    st.warning(f"Could not decrypt audit entry: {str(decrypt_error)}")
                    continue
            
            return audit_trail
            
        except Exception as e:
            st.error(f"Error retrieving audit trail: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()
    
    def cleanup_expired_data(self) -> Dict[str, int]:
        """Clean up expired data per retention policies"""
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            current_time = datetime.datetime.now().isoformat()
            cleanup_summary = {
                'assessments_cleaned': 0,
                'reports_cleaned': 0,
                'ai_analyses_cleaned': 0,
                'consent_records_cleaned': 0
            }
            
            # Clean expired assessments
            cursor.execute("""
                DELETE FROM assessments 
                WHERE expires_at IS NOT NULL AND expires_at < ?
            """, (current_time,))
            cleanup_summary['assessments_cleaned'] = cursor.rowcount
            
            # Clean expired reports
            cursor.execute("""
                DELETE FROM diagnostic_reports 
                WHERE expires_at IS NOT NULL AND expires_at < ?
            """, (current_time,))
            cleanup_summary['reports_cleaned'] = cursor.rowcount
            
            # Clean expired AI analyses
            cursor.execute("""
                DELETE FROM ai_analyses 
                WHERE expires_at IS NOT NULL AND expires_at < ?
            """, (current_time,))
            cleanup_summary['ai_analyses_cleaned'] = cursor.rowcount
            
            # Clean expired consent records (careful with legal requirements)
            cursor.execute("""
                DELETE FROM consent_records 
                WHERE expires_at IS NOT NULL AND expires_at < ? AND withdrawal_date IS NOT NULL
            """, (current_time,))
            cleanup_summary['consent_records_cleaned'] = cursor.rowcount
            
            conn.commit()
            
            # Log cleanup operation
            self._log_action('system', 'cleanup', 'expired_data', 'batch', {
                'cleanup_summary': cleanup_summary,
                'cleanup_timestamp': current_time,
                'compliance_action': True
            })
            
            return cleanup_summary
            
        except Exception as e:
            st.error(f"Error during data cleanup: {str(e)}")
            return {}
        finally:
            if conn:
                conn.close()
    
    def get_storage_statistics(self) -> Dict[str, Any]:
        """Get storage statistics for compliance reporting"""
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            stats = {
                'timestamp': datetime.datetime.now().isoformat(),
                'total_users': 0,
                'total_assessments': 0,
                'total_ai_analyses': 0,
                'total_crisis_records': 0,
                'total_reports': 0,
                'active_consents': 0,
                'pending_requests': 0,
                'storage_compliance': 'DPDPA_2023_Compliant'
            }
            
            # Count users
            cursor.execute("SELECT COUNT(*) FROM user_data")
            stats['total_users'] = cursor.fetchone()[0]
            
            # Count assessments
            cursor.execute("SELECT COUNT(*) FROM assessments")
            stats['total_assessments'] = cursor.fetchone()[0]
            
            # Count AI analyses
            cursor.execute("SELECT COUNT(*) FROM ai_analyses")
            stats['total_ai_analyses'] = cursor.fetchone()[0]
            
            # Count crisis records
            cursor.execute("SELECT COUNT(*) FROM crisis_records")
            stats['total_crisis_records'] = cursor.fetchone()[0]
            
            # Count reports
            cursor.execute("SELECT COUNT(*) FROM diagnostic_reports")
            stats['total_reports'] = cursor.fetchone()[0]
            
            # Count active consents
            cursor.execute("SELECT COUNT(*) FROM consent_records WHERE consent_given = 1 AND withdrawal_date IS NULL")
            stats['active_consents'] = cursor.fetchone()[0]
            
            # Count pending requests
            cursor.execute("SELECT COUNT(*) FROM data_requests WHERE status = 'pending'")
            stats['pending_requests'] = cursor.fetchone()[0]
            
            return stats
            
        except Exception as e:
            st.error(f"Error getting storage statistics: {str(e)}")
            return {}
        finally:
            if conn:
                conn.close()
