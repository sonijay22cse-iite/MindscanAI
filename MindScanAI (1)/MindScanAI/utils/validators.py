import re
from typing import Optional


class Validators:
    """Data validation utilities for user inputs"""
    
    def __init__(self):
        # Indian phone number patterns
        self.phone_pattern = re.compile(r'^(\+91|91)?[6-9]\d{9}$')
        # Email validation pattern
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def validate_phone(self, phone: str) -> bool:
        """Validate Indian phone numbers"""
        if not phone:
            return False
        
        # Remove spaces, hyphens, and other common separators
        cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
        
        # Check if it matches Indian phone number pattern
        return bool(self.phone_pattern.match(cleaned_phone))
    
    def validate_email(self, email: str) -> bool:
        """Validate email addresses"""
        if not email:
            return False
        
        # Check basic email format
        return bool(self.email_pattern.match(email.strip().lower()))
    
    def validate_age(self, age: int) -> bool:
        """Validate age input"""
        return 5 <= age <= 120
    
    def validate_name(self, name: str) -> bool:
        """Validate name input"""
        if not name or len(name.strip()) < 2:
            return False
        
        # Allow letters, spaces, and common name characters
        name_pattern = re.compile(r'^[a-zA-Z\s\.\-\']+$')
        return bool(name_pattern.match(name.strip()))
    
    def validate_user_id(self, user_id: str) -> bool:
        """Validate user ID format"""
        if not user_id:
            return False
        
        # Basic user ID validation - alphanumeric and underscores
        user_id_pattern = re.compile(r'^[a-zA-Z0-9_]{3,50}$')
        return bool(user_id_pattern.match(user_id))
    
    def sanitize_input(self, input_text: str) -> str:
        """Sanitize text input to prevent injection attacks"""
        if not input_text:
            return ""
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>\"\'&]', '', input_text)
        return sanitized.strip()
    
    def validate_assessment_response(self, response: any, question_type: str) -> bool:
        """Validate assessment response based on question type"""
        if response is None:
            return False
        
        if question_type == 'scale':
            return isinstance(response, (int, float)) and 0 <= response <= 10
        elif question_type == 'multiple_choice':
            return isinstance(response, str) and len(response.strip()) > 0
        elif question_type == 'checkbox':
            return isinstance(response, list)
        
        return True