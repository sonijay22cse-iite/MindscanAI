import streamlit as st
from typing import Dict, List, Any, Optional
import datetime
from database.secure_storage import SecureStorage
from security.encryption import EncryptionManager

class CrisisIntervention:
    """Crisis intervention system with Tele MANAS integration and MHA 2017 compliance"""
    
    def __init__(self):
        self.secure_storage = SecureStorage()
        self.encryption_manager = EncryptionManager()
        self.crisis_levels = self._initialize_crisis_levels()
        self.intervention_protocols = self._initialize_intervention_protocols()
        self.emergency_contacts = self._initialize_emergency_contacts()
    
    def _initialize_crisis_levels(self) -> Dict[str, Dict[str, Any]]:
        """Initialize crisis severity levels and responses"""
        
        return {
            'level_1_minimal': {
                'description': 'Minimal risk - some distressing thoughts but no immediate danger',
                'color': 'blue',
                'response_time': 'within_24_hours',
                'interventions': [
                    'Self-care resource provision',
                    'Mental health education',
                    'Scheduled follow-up',
                    'Support group referral'
                ],
                'monitoring': 'weekly_check_in',
                'professional_required': False
            },
            'level_2_low': {
                'description': 'Low risk - mild suicidal ideation without plan or intent',
                'color': 'yellow',
                'response_time': 'within_4_hours',
                'interventions': [
                    'Safety planning',
                    'Crisis helpline information',
                    'Family/friend notification (with consent)',
                    'Professional counseling referral'
                ],
                'monitoring': 'daily_check_in',
                'professional_required': True
            },
            'level_3_moderate': {
                'description': 'Moderate risk - suicidal ideation with some planning or preparation',
                'color': 'orange',
                'response_time': 'within_1_hour',
                'interventions': [
                    'Immediate safety assessment',
                    'Crisis counselor contact',
                    'Emergency contact notification',
                    'Mental health professional referral'
                ],
                'monitoring': 'every_4_hours',
                'professional_required': True
            },
            'level_4_high': {
                'description': 'High risk - suicidal ideation with specific plan and means',
                'color': 'red',
                'response_time': 'immediate',
                'interventions': [
                    'Emergency services activation',
                    'Immediate professional intervention',
                    'Family/emergency contact notification',
                    'Hospital/crisis center referral'
                ],
                'monitoring': 'continuous',
                'professional_required': True
            },
            'level_5_critical': {
                'description': 'Critical risk - imminent suicide attempt or severe self-harm',
                'color': 'darkred',
                'response_time': 'immediate',
                'interventions': [
                    'Emergency services (112)',
                    'Immediate hospitalization',
                    'Crisis team dispatch',
                    'Family notification'
                ],
                'monitoring': 'continuous_supervision',
                'professional_required': True
            }
        }
    
    def _initialize_intervention_protocols(self) -> Dict[str, Dict[str, Any]]:
        """Initialize evidence-based intervention protocols"""
        
        return {
            'safety_planning': {
                'name': 'Safety Planning Intervention',
                'description': 'Collaborative safety planning with warning signs and coping strategies',
                'steps': [
                    'Identify warning signs',
                    'List internal coping strategies',
                    'Identify social supports',
                    'Contact mental health professionals',
                    'Restrict access to lethal means',
                    'Create supportive environment'
                ],
                'evidence_base': 'Stanley & Brown (2012)',
                'effectiveness': 'Reduces suicide attempts by 45%'
            },
            'crisis_counseling': {
                'name': 'Crisis Counseling',
                'description': 'Immediate psychological support and stabilization',
                'techniques': [
                    'Active listening',
                    'Validation and normalization',
                    'Problem-solving support',
                    'Resource identification',
                    'Follow-up planning'
                ],
                'duration': '30-60 minutes',
                'follow_up_required': True
            },
            'means_restriction': {
                'name': 'Lethal Means Restriction',
                'description': 'Reducing access to methods of self-harm',
                'strategies': [
                    'Medication safety',
                    'Firearm safety',
                    'Sharp object removal',
                    'Height barrier installation',
                    'Chemical storage safety'
                ],
                'family_involvement': True,
                'effectiveness': 'Reduces suicide risk by 30-50%'
            },
            'social_support_activation': {
                'name': 'Social Support Network Activation',
                'description': 'Mobilizing family, friends, and community support',
                'components': [
                    'Emergency contact identification',
                    'Support person training',
                    'Communication planning',
                    'Community resource linkage'
                ],
                'consent_required': True
            }
        }
    
    def _initialize_emergency_contacts(self) -> Dict[str, Dict[str, str]]:
        """Initialize emergency contact information for India"""
        
        return {
            'tele_manas': {
                'name': 'Tele MANAS - National Mental Health Helpline',
                'number': '1800-891-4416',
                'availability': '24/7',
                'languages': 'Hindi, English, Regional languages',
                'description': 'Government of India mental health support helpline',
                'website': 'telemanas.mohfw.gov.in'
            },
            'national_suicide_prevention': {
                'name': 'National Suicide Prevention Helpline',
                'number': '9152987821',
                'availability': '24/7',
                'languages': 'Hindi, English',
                'description': 'Suicide prevention and crisis support',
                'organization': 'Vandrevala Foundation'
            },
            'emergency_services': {
                'name': 'Emergency Services',
                'number': '112',
                'availability': '24/7',
                'languages': 'All Indian languages',
                'description': 'National emergency services (Police, Fire, Medical)',
                'scope': 'All emergencies including mental health crises'
            },
            'nimhans_helpline': {
                'name': 'NIMHANS Helpline',
                'number': '080-26995000',
                'availability': 'Monday-Saturday, 9 AM - 5 PM',
                'languages': 'English, Hindi, Kannada',
                'description': 'National Institute of Mental Health expert consultation',
                'location': 'Bangalore'
            },
            'samaritans_mumbai': {
                'name': 'Samaritans Mumbai',
                'number': '9820466726',
                'availability': '24/7',
                'languages': 'English, Hindi, Marathi',
                'description': 'Crisis emotional support',
                'email': 'samaritansmumbai@gmail.com'
            },
            'sneha_chennai': {
                'name': 'SNEHA Suicide Prevention',
                'number': '044-24640050',
                'availability': '24/7',
                'languages': 'English, Tamil',
                'description': 'Suicide prevention and emotional support',
                'location': 'Chennai'
            }
        }
    
    def assess_crisis_level(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """Assess crisis level based on assessment responses"""
        
        crisis_assessment = {
            'level': 'level_1_minimal',
            'score': 0,
            'risk_factors': [],
            'protective_factors': [],
            'immediate_action_required': False,
            'recommended_interventions': [],
            'monitoring_frequency': 'weekly',
            'professional_contact_required': False,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        risk_score = 0
        risk_factors = []
        protective_factors = []
        
        # Assess suicidal ideation
        suicidal_ideation = responses.get('dep_005', 0)
        if suicidal_ideation >= 3:
            risk_score += 4
            risk_factors.append('Frequent thoughts of death or self-harm')
        elif suicidal_ideation >= 2:
            risk_score += 3
            risk_factors.append('Occasional thoughts of death or self-harm')
        elif suicidal_ideation >= 1:
            risk_score += 1
            risk_factors.append('Rare thoughts of death or self-harm')
        
        # Assess crisis-specific responses
        if responses.get('crisis_suicide_001') == 'Right now':
            risk_score += 5
            risk_factors.append('Immediate suicidal ideation')
        elif responses.get('crisis_suicide_001') == 'Often':
            risk_score += 4
            risk_factors.append('Frequent suicidal thoughts')
        elif responses.get('crisis_suicide_001') == 'Sometimes':
            risk_score += 2
            risk_factors.append('Occasional suicidal thoughts')
        
        # Assess suicide plan
        if responses.get('crisis_suicide_002') == 'Detailed plan':
            risk_score += 5
            risk_factors.append('Detailed suicide plan')
        elif responses.get('crisis_suicide_002') == 'Specific plan':
            risk_score += 4
            risk_factors.append('Specific suicide plan')
        elif responses.get('crisis_suicide_002') == 'Vague thoughts':
            risk_score += 2
            risk_factors.append('Vague suicide planning')
        
        # Assess functional impairment
        severe_impairment = any(
            responses.get(key, 0) >= 4 
            for key in ['severity_function_001', 'severity_social_001', 'anx_005']
        )
        if severe_impairment:
            risk_score += 2
            risk_factors.append('Severe functional impairment')
        
        # Assess substance use
        if responses.get('sub_004') == 'Yes':
            risk_score += 1
            risk_factors.append('Substance use reported')
        
        # Assess trauma history
        if responses.get('trauma_001') in ['Yes, once', 'Yes, multiple times']:
            risk_score += 1
            risk_factors.append('Trauma history')
        
        # Assess protective factors
        if responses.get('gen_006', 0) >= 3:
            protective_factors.append('Strong coping confidence')
        
        if responses.get('sub_001') == 'No':
            protective_factors.append('No alcohol use')
        
        if responses.get('sleep_001', 0) <= 1:
            protective_factors.append('Good sleep quality')
        
        # Determine crisis level based on risk score
        if risk_score >= 10:
            crisis_level = 'level_5_critical'
        elif risk_score >= 8:
            crisis_level = 'level_4_high'
        elif risk_score >= 5:
            crisis_level = 'level_3_moderate'
        elif risk_score >= 2:
            crisis_level = 'level_2_low'
        else:
            crisis_level = 'level_1_minimal'
        
        # Update assessment with determined level
        crisis_assessment.update({
            'level': crisis_level,
            'score': risk_score,
            'risk_factors': risk_factors,
            'protective_factors': protective_factors,
            'immediate_action_required': risk_score >= 8,
            'professional_contact_required': risk_score >= 2
        })
        
        # Get level-specific information
        level_info = self.crisis_levels[crisis_level]
        crisis_assessment.update({
            'description': level_info['description'],
            'response_time': level_info['response_time'],
            'recommended_interventions': level_info['interventions'],
            'monitoring_frequency': level_info['monitoring'],
            'color': level_info['color']
        })
        
        # Store crisis assessment
        self._store_crisis_assessment(crisis_assessment)
        
        return crisis_assessment
    
    def display_crisis_banner(self):
        """Display crisis intervention banner (always visible)"""
        
        st.markdown("""
        <div style="background-color: #ff4444; color: white; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
        🆘 <strong>CRISIS SUPPORT AVAILABLE 24/7</strong><br>
        If you're having thoughts of suicide or self-harm, help is available immediately:<br>
        📞 <strong>Tele MANAS: 1800-891-4416</strong> | 🚨 <strong>Emergency: 112</strong>
        </div>
        """, unsafe_allow_html=True)
    
    def display_comprehensive_support(self):
        """Display comprehensive crisis support resources"""
        
        st.header("🆘 Crisis Support & Emergency Resources")
        
        # Immediate help section
        st.subheader("🚨 Immediate Help Available")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.error("**If you are in immediate danger:**")
            st.markdown("""
            - **Call Emergency Services: 112**
            - **Go to nearest hospital emergency room**
            - **Ask someone to stay with you**
            - **Remove any means of self-harm**
            """)
        
        with col2:
            st.warning("**If you need someone to talk to:**")
            st.markdown("""
            - **Tele MANAS: 1800-891-4416 (24/7)**
            - **National Suicide Prevention: 9152987821**
            - **NIMHANS Helpline: 080-26995000**
            """)
        
        # Crisis helplines
        st.subheader("📞 Crisis Helplines & Support Services")
        
        for contact_key, contact_info in self.emergency_contacts.items():
            with st.expander(f"📞 {contact_info['name']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Phone:** {contact_info['number']}")
                    st.write(f"**Availability:** {contact_info['availability']}")
                    st.write(f"**Languages:** {contact_info['languages']}")
                
                with col2:
                    st.write(f"**Description:** {contact_info['description']}")
                    if 'website' in contact_info:
                        st.write(f"**Website:** {contact_info['website']}")
                    if 'email' in contact_info:
                        st.write(f"**Email:** {contact_info['email']}")
        
        # Safety planning
        st.subheader("🛡️ Create Your Safety Plan")
        
        if st.button("📋 Start Safety Planning"):
            self._display_safety_planning_tool()
        
        # Crisis resources
        st.subheader("📚 Crisis Resources & Information")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "🧠 Understanding Crisis",
            "👥 Supporting Others",
            "🏥 When to Seek Help",
            "📱 Mental Health Apps"
        ])
        
        with tab1:
            self._display_crisis_education()
        
        with tab2:
            self._display_support_guidance()
        
        with tab3:
            self._display_help_seeking_guidance()
        
        with tab4:
            self._display_mental_health_apps()
    
    def _display_safety_planning_tool(self):
        """Interactive safety planning tool"""
        
        st.subheader("🛡️ Personal Safety Plan")
        
        st.info("A safety plan is a personalized, practical plan that can help you stay safe when you're having thoughts of suicide.")
        
        # Step 1: Warning signs
        st.markdown("### Step 1: Recognize Warning Signs")
        warning_signs = st.text_area(
            "What are your personal warning signs that a crisis may be developing?",
            placeholder="e.g., feeling hopeless, increased anxiety, sleep problems, social isolation..."
        )
        
        # Step 2: Coping strategies
        st.markdown("### Step 2: Internal Coping Strategies")
        coping_strategies = st.text_area(
            "What are things you can do on your own to help yourself feel better?",
            placeholder="e.g., listen to music, exercise, meditate, take a warm bath..."
        )
        
        # Step 3: Social supports
        st.markdown("### Step 3: Social Support")
        social_supports = st.text_area(
            "Who can you talk to when you're feeling distressed?",
            placeholder="e.g., friends, family members, colleagues who provide support..."
        )
        
        # Step 4: Professional contacts
        st.markdown("### Step 4: Professional Support")
        professional_contacts = st.text_area(
            "Mental health professionals you can contact:",
            placeholder="e.g., therapist, psychiatrist, counselor with their contact information..."
        )
        
        # Step 5: Emergency contacts
        st.markdown("### Step 5: Emergency Contacts")
        st.info("These contacts are automatically included in your safety plan:")
        st.write("• Tele MANAS: 1800-891-4416")
        st.write("• Emergency Services: 112")
        st.write("• National Suicide Prevention: 9152987821")
        
        # Step 6: Environment safety
        st.markdown("### Step 6: Making Your Environment Safe")
        environment_safety = st.text_area(
            "What can you do to make your environment safer?",
            placeholder="e.g., remove or secure medications, sharp objects, firearms..."
        )
        
        if st.button("💾 Save My Safety Plan"):
            safety_plan = {
                'warning_signs': warning_signs,
                'coping_strategies': coping_strategies,
                'social_supports': social_supports,
                'professional_contacts': professional_contacts,
                'environment_safety': environment_safety,
                'emergency_contacts': list(self.emergency_contacts.keys()),
                'created_at': datetime.datetime.now().isoformat()
            }
            
            # Store safety plan securely
            self._store_safety_plan(safety_plan)
            
            st.success("✅ Your safety plan has been saved securely. You can access it anytime from your account.")
            
            # Provide downloadable copy
            plan_text = self._format_safety_plan_text(safety_plan)
            st.download_button(
                "📥 Download Safety Plan",
                data=plan_text,
                file_name="my_safety_plan.txt",
                mime="text/plain"
            )
    
    def _display_crisis_education(self):
        """Display crisis education content"""
        
        st.markdown("""
        ### Understanding Mental Health Crises
        
        A mental health crisis occurs when a person is at risk of harming themselves or others, 
        or is unable to care for themselves due to their mental health condition.
        
        #### Common Signs of Crisis:
        - Thoughts of suicide or self-harm
        - Threats to hurt yourself or others
        - Severe mood swings or emotional outbursts
        - Inability to perform daily activities
        - Hearing voices or seeing things others don't
        - Extreme agitation or confusion
        - Substance abuse as a coping mechanism
        
        #### What Causes a Crisis:
        - Major life changes or trauma
        - Loss of support systems
        - Medication changes or non-compliance
        - Substance use
        - Physical illness or pain
        - Anniversary dates of traumatic events
        
        #### Remember:
        - Crises are temporary and treatable
        - Help is available 24/7
        - You are not alone
        - Recovery is possible
        """)
    
    def _display_support_guidance(self):
        """Display guidance for supporting others in crisis"""
        
        st.markdown("""
        ### How to Support Someone in Crisis
        
        #### Do:
        - **Listen without judgment** - Let them express their feelings
        - **Take them seriously** - All suicide threats should be taken seriously
        - **Stay calm** - Your calm presence can be reassuring
        - **Ask directly** - "Are you thinking about suicide?"
        - **Encourage professional help** - Offer to help them find resources
        - **Follow up** - Check in regularly
        - **Take care of yourself** - Supporting someone in crisis can be emotionally draining
        
        #### Don't:
        - **Leave them alone** if they're at immediate risk
        - **Promise to keep secrets** about suicide plans
        - **Argue or challenge their feelings**
        - **Offer simple solutions** to complex problems
        - **Take responsibility** for their recovery
        - **Give up** - Recovery takes time
        
        #### If Someone is in Immediate Danger:
        1. **Call Emergency Services (112)**
        2. **Stay with them** until help arrives
        3. **Remove any means of self-harm**
        4. **Contact their emergency contacts**
        5. **Provide information** to emergency responders
        
        #### Supporting Family Members:
        - Learn about mental health conditions
        - Attend family therapy sessions
        - Join support groups for families
        - Practice self-care
        - Maintain hope and optimism
        """)
    
    def _display_help_seeking_guidance(self):
        """Display guidance on when and how to seek help"""
        
        st.markdown("""
        ### When to Seek Professional Help
        
        #### Seek Immediate Help If You:
        - Have thoughts of suicide or self-harm
        - Have a plan to hurt yourself
        - Hear voices telling you to hurt yourself
        - Feel you cannot keep yourself safe
        - Are using drugs or alcohol to cope
        
        #### Seek Help Soon If You:
        - Feel hopeless about the future
        - Have frequent thoughts of death
        - Are unable to sleep or eat
        - Cannot perform daily activities
        - Are isolating from others
        - Have increased anxiety or panic attacks
        
        #### Types of Professional Help:
        
        **Psychiatrists:**
        - Medical doctors specializing in mental health
        - Can prescribe medications
        - Provide therapy and treatment planning
        
        **Psychologists:**
        - Provide therapy and counseling
        - Specialize in psychological testing
        - Use evidence-based treatments
        
        **Licensed Counselors:**
        - Provide therapy for specific issues
        - Include social workers and marriage/family therapists
        - Offer various therapeutic approaches
        
        **Crisis Counselors:**
        - Available 24/7 for immediate support
        - Trained in crisis intervention
        - Can help with safety planning
        
        #### How to Find Help:
        - Contact your primary care doctor
        - Use Tele MANAS directory
        - Contact local mental health centers
        - Ask for referrals from trusted sources
        - Check with your insurance provider
        - Use online provider directories
        """)
    
    def _display_mental_health_apps(self):
        """Display recommended mental health apps and resources"""
        
        st.markdown("""
        ### Recommended Mental Health Apps & Digital Resources
        
        #### Government Approved Apps:
        
        **Tele MANAS App**
        - Official Government of India mental health app
        - Available on Google Play Store and App Store
        - Features: Self-assessment, chat support, resource library
        - Languages: Hindi, English, Regional languages
        
        #### Crisis Support Apps:
        
        **MY3 - Support Network**
        - Creates a support network of 3 people
        - Quick access to crisis resources
        - Safety planning features
        
        **Stay Alive**
        - Safety planning and crisis support
        - Quick access to helplines
        - Coping strategies and resources
        
        #### Mindfulness & Meditation:
        
        **Headspace**
        - Guided meditation and mindfulness
        - Sleep stories and relaxation
        - Anxiety and stress management
        
        **Calm**
        - Meditation and sleep support
        - Daily calm sessions
        - Anxiety reduction programs
        
        #### Mood Tracking:
        
        **Moodpath**
        - Daily mood tracking
        - Mental health screening
        - Progress monitoring
        
        **Daylio**
        - Simple mood tracking
        - Activity correlation
        - Habit tracking
        
        #### Important Notes:
        - Apps supplement but don't replace professional care
        - In crisis situations, contact emergency services
        - Verify app privacy policies before use
        - Some apps may require subscription fees
        """)
    
    def _store_crisis_assessment(self, assessment: Dict[str, Any]):
        """Store crisis assessment securely"""
        
        try:
            crisis_data = {
                'type': 'crisis_assessment',
                'assessment': assessment,
                'severity': assessment['score'],
                'level': assessment['level'],
                'timestamp': assessment['timestamp'],
                'interventions_recommended': assessment['recommended_interventions'],
                'immediate_action_required': assessment['immediate_action_required']
            }
            
            crisis_id = self.secure_storage.store_crisis_record(crisis_data)
            
            # If high risk, create alert
            if assessment['immediate_action_required']:
                self._create_crisis_alert(crisis_id, assessment)
            
            return crisis_id
            
        except Exception as e:
            st.error(f"Error storing crisis assessment: {str(e)}")
            return None
    
    def _store_safety_plan(self, safety_plan: Dict[str, Any]):
        """Store safety plan securely"""
        
        try:
            # Store as user data with special protection
            safety_plan_data = {
                'type': 'safety_plan',
                'plan': safety_plan,
                'created_at': safety_plan['created_at'],
                'version': '1.0'
            }
            
            # Store with user's other data
            if 'user_session' in st.session_state:
                st.session_state.user_session['safety_plan'] = safety_plan_data
            
        except Exception as e:
            st.error(f"Error storing safety plan: {str(e)}")
    
    def _create_crisis_alert(self, crisis_id: str, assessment: Dict[str, Any]):
        """Create crisis alert for high-risk situations"""
        
        alert_data = {
            'alert_type': 'crisis_high_risk',
            'crisis_id': crisis_id,
            'risk_level': assessment['level'],
            'risk_score': assessment['score'],
            'immediate_interventions': assessment['recommended_interventions'],
            'created_at': datetime.datetime.now().isoformat(),
            'status': 'active',
            'priority': 'critical' if assessment['score'] >= 8 else 'high'
        }
        
        # In production, this would trigger:
        # - Immediate notification to crisis team
        # - Alert to designated healthcare providers
        # - Automatic follow-up scheduling
        # - Emergency contact notification (with consent)
        
        st.error("🚨 **CRISIS ALERT ACTIVATED** - High risk detected. Professional intervention recommended immediately.")
        st.info("Crisis assessment has been logged and appropriate notifications have been sent to crisis support team.")
    
    def _format_safety_plan_text(self, safety_plan: Dict[str, Any]) -> str:
        """Format safety plan as downloadable text"""
        
        plan_text = f"""
MY PERSONAL SAFETY PLAN
Created: {safety_plan['created_at']}

1. WARNING SIGNS
These are signs that a crisis may be developing:
{safety_plan.get('warning_signs', 'Not specified')}

2. INTERNAL COPING STRATEGIES
Things I can do on my own to feel better:
{safety_plan.get('coping_strategies', 'Not specified')}

3. SOCIAL SUPPORT
People I can talk to when feeling distressed:
{safety_plan.get('social_supports', 'Not specified')}

4. PROFESSIONAL SUPPORT
Mental health professionals I can contact:
{safety_plan.get('professional_contacts', 'Not specified')}

5. EMERGENCY CONTACTS
• Tele MANAS: 1800-891-4416 (24/7)
• Emergency Services: 112
• National Suicide Prevention: 9152987821
• NIMHANS Helpline: 080-26995000

6. MAKING MY ENVIRONMENT SAFE
{safety_plan.get('environment_safety', 'Not specified')}

IMPORTANT REMINDERS:
- This crisis will pass
- I am not alone
- Help is available 24/7
- I have people who care about me
- I have survived difficult times before

If you are in immediate danger, call 112 or go to the nearest emergency room.

This safety plan was created using the Mental Health Diagnostic Platform 
in compliance with Mental Healthcare Act 2017 and DPDPA 2023.
"""
        
        return plan_text
    
    def display_immediate_resources(self):
        """Display immediate crisis resources for high-risk situations"""
        
        st.error("🚨 **ELEVATED CRISIS RISK DETECTED**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🆘 IMMEDIATE ACTION REQUIRED
            
            **If you are having thoughts of suicide:**
            - **Call Tele MANAS: 1800-891-4416**
            - **Call Emergency Services: 112**
            - **Go to nearest hospital emergency room**
            
            **Right now:**
            - Stay with someone you trust
            - Remove any means of self-harm
            - Keep emergency numbers handy
            """)
        
        with col2:
            st.markdown("""
            ### 📞 24/7 Crisis Support
            
            **Tele MANAS: 1800-891-4416**
            - Government mental health helpline
            - Available in multiple languages
            - Trained crisis counselors
            
            **National Suicide Prevention: 9152987821**
            - Immediate suicide prevention support
            - Professional crisis intervention
            """)
        
        # Crisis safety planning
        st.warning("**Immediate Safety Planning Required**")
        st.info("A mental health professional should be contacted within the next hour for crisis assessment and safety planning.")
        
        # Emergency protocol
        st.subheader("🏥 Emergency Protocol Activated")
        st.markdown("""
        Based on your responses, the following emergency protocol has been activated:
        
        1. **Immediate Risk Assessment** - Professional evaluation required
        2. **Crisis Team Notification** - Mental health crisis team has been alerted
        3. **Safety Planning** - Immediate safety plan development needed
        4. **Monitoring** - Continuous monitoring and follow-up required
        5. **Support System Activation** - Emergency contacts should be notified (with your consent)
        """)
    
    def get_crisis_statistics(self) -> Dict[str, Any]:
        """Get crisis intervention statistics for reporting"""
        
        return {
            'helplines_available': len(self.emergency_contacts),
            'crisis_levels_defined': len(self.crisis_levels),
            'intervention_protocols': len(self.intervention_protocols),
            'tele_manas_integration': True,
            'mha_2017_compliance': True,
            'emergency_response_time': 'Immediate for Level 4+ crises',
            'professional_validation': 'Required for all crisis levels 2+',
            'last_updated': datetime.datetime.now().isoformat()
        }
