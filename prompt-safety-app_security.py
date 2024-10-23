import streamlit as st
import re
import html
import json
from typing import List, Dict, Optional
from datetime import datetime

class PromptSafetyChecker:
    def __init__(self):
        # Expanded suspicious patterns organized by category
        self.suspicious_patterns = {
            "instruction_override": [
                r"ignore (?:all )?(?:previous |above )?instructions",
                r"disregard (?:all )?(?:previous )?(?:instructions|prompts)",
                r"forget (?:all )?(?:previous )?(?:instructions|prompts)",
                r"new instruction:",
                r"system prompt:",
                r"you (?:are|will be|shall be|must be) now",
                r"act as",
                r"do not follow",
                r"override (?:previous |all )?(?:instructions|settings)",
                r"disable (?:all )?(?:filters|restrictions|limitations)",
                r"bypass (?:all )?(?:filters|restrictions|limitations)",
                r"ignore (?:all )?(?:filters|restrictions|limitations)",
            ],
            
            "system_commands": [
                r"sudo",
                r"/[a-z]+",  # Command-like patterns
                r"\\[a-z]+",
                r"\$[a-z]+",
                r"execute(?:\s+(?:command|script|file))?:",
                r"run(?:\s+(?:command|script|file))?:",
                r"system\s*\(",
                r"eval\s*\(",
                r"exec\s*\(",
            ],
            
            "code_injection": [
                r"```.*?```",
                r"<script.*?>.*?</script>",
                r"javascript:",
                r"data:text/[a-z]+;base64,",
                r"(?:file|https?|ftp|data)://\S+",
                r"(?:require|import|from)\s+['\"]?\w+",
            ],
            
            "markup_injection": [
                r"<\/?[a-z][\s\S]*>",
                r"\[.*?\]\(.*?\)",
                r"\{\{.*?\}\}",  # Template injection
                r"\{\%.*?\%\}",
                r"\$\{.*?\}",    # Template string injection
            ],
            
            "role_playing": [
                r"you are(?: now)?(?: a| an| the)? \w+",
                r"switch(?: your)? (?:role|personality)(?: to)?",
                r"behave like(?: a| an)?",
                r"pretend(?: to be| you are)",
                r"role-?play as",
            ],
            
            "escaping_attempts": [
                r"base64:",
                r"\\x[0-9a-fA-F]{2}",
                r"\\u[0-9a-fA-F]{4}",
                r"\\[rnt]",
                r"&#x?[0-9a-fA-F]+;",
                r"%[0-9a-fA-F]{2}",
            ],
            
            "prompt_manipulation": [
                r"context manipulation",
                r"change(?: your)? (?:behavior|personality|response)",
                r"modify(?: your)? (?:output|behavior|response)",
                r"reset(?: your)? (?:context|memory|state)",
                r"(?:previous|above) conversation is false",
                r"(?:previous|above) context is wrong",
                r"your(?: new)? purpose is",
            ],
            
            "data_exfiltration": [
                r"show(?: me)?(?:(?: the)? system| internal| hidden| secret) (?:prompt|instructions|data|information)",
                r"reveal(?: the)?(?: system| internal| hidden| secret) (?:prompt|instructions|data|information)",
                r"display(?: the)?(?: system| internal| hidden| secret) (?:prompt|instructions|data|information)",
                r"what(?: are)?(?: your)?(?: system| internal| hidden| secret) (?:prompt|instructions|settings)",
            ]
        }
        
        # Maximum allowed input length
        self.max_input_length = 1000
        
        # Additional security settings
        self.max_special_chars_ratio = 0.3
        self.max_repetition_ratio = 0.4
        self.min_entropy_ratio = 0.6
        
        # Keep track of user inputs for rate limiting
        self.user_inputs: Dict[str, List[Dict]] = {}
        
    def calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of the text to detect potential obfuscation."""
        if not text:
            return 0
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1
        entropy = 0
        for count in freq.values():
            probability = count / len(text)
            entropy -= probability * (probability.real.log2())
        return entropy / 8.0  # Normalize to [0,1]
    
    def check_repetition(self, text: str) -> float:
        """Check for suspicious repetition patterns."""
        if not text:
            return 0
        chunks = [text[i:i+3] for i in range(len(text)-2)]
        unique_chunks = len(set(chunks))
        return 1 - (unique_chunks / max(len(chunks), 1))
    
    def sanitize_input(self, text: str) -> str:
        """Enhanced input sanitization."""
        # HTML escape to prevent XSS
        text = html.escape(text)
        # Remove any control characters
        text = ''.join(char for char in text if ord(char) >= 32)
        # Normalize whitespace
        text = ' '.join(text.split())
        # Remove UTF-8 invisible characters
        text = re.sub(r'[\u200B-\u200F\uFEFF]', '', text)
        return text.strip()
    
    def check_suspicious_patterns(self, text: str) -> List[Dict[str, str]]:
        """Enhanced pattern checking with categorization."""
        findings = []
        for category, patterns in self.suspicious_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    findings.append({
                        "category": category,
                        "pattern": pattern,
                        "matched_text": match.group(0),
                        "position": match.span()
                    })
        return findings
    
    def validate_input(self, text: str) -> tuple[bool, Optional[str], List[Dict]]:
        """Enhanced input validation with detailed reporting."""
        validation_results = []
        
        # Check input length
        if len(text) > self.max_input_length:
            return False, f"Input exceeds maximum length of {self.max_input_length} characters", validation_results
        
        # Check special characters ratio
        special_chars = sum(1 for c in text if not c.isalnum() and not c.isspace())
        special_chars_ratio = special_chars / len(text) if text else 0
        if special_chars_ratio > self.max_special_chars_ratio:
            validation_results.append({
                "check": "special_chars",
                "status": "failed",
                "ratio": special_chars_ratio
            })
        
        # Check repetition
        repetition_ratio = self.check_repetition(text)
        if repetition_ratio > self.max_repetition_ratio:
            validation_results.append({
                "check": "repetition",
                "status": "failed",
                "ratio": repetition_ratio
            })
        
        # Check entropy
        entropy_ratio = self.calculate_entropy(text)
        if entropy_ratio < self.min_entropy_ratio:
            validation_results.append({
                "check": "entropy",
                "status": "failed",
                "ratio": entropy_ratio
            })
        
        # Check for suspicious patterns
        findings = self.check_suspicious_patterns(text)
        if findings:
            validation_results.append({
                "check": "patterns",
                "status": "failed",
                "findings": findings
            })
            pattern_details = "\n".join([
                f"- {f['category']}: {f['matched_text']}" 
                for f in findings
            ])
            return False, f"Potential prompt injection detected:\n{pattern_details}", validation_results
        
        if validation_results:
            return False, "Input validation failed", validation_results
        
        return True, None, validation_results

def main():
    st.title("Enhanced Secure Prompt Input System")
    
    # Initialize the safety checker
    if 'safety_checker' not in st.session_state:
        st.session_state.safety_checker = PromptSafetyChecker()
    
    # Add a description
    st.markdown("""
    This application demonstrates advanced prompt safety measures to prevent prompt injection attacks.
    It includes:
    - Enhanced pattern detection across multiple categories
    - Advanced input sanitization
    - Statistical analysis of input characteristics
    - Detailed validation reporting
    """)
    
    # User input
    user_input = st.text_area("Enter your prompt:", max_chars=1000)
    
    if st.button("Submit"):
        if user_input:
            # Sanitize input
            sanitized_input = st.session_state.safety_checker.sanitize_input(user_input)
            
            # Validate input
            is_valid, error_message, validation_results = st.session_state.safety_checker.validate_input(sanitized_input)
            
            if is_valid:
                st.success("Input validated successfully!")
                st.write("Sanitized input:", sanitized_input)
            else:
                st.error(error_message)
                
                # Display detailed validation results
                if validation_results:
                    st.expander("Validation Details").json(validation_results)
                
                st.warning("Please modify your input and try again.")
        else:
            st.warning("Please enter some text.")
    
    # Display enhanced security information
    with st.expander("Security Information"):
        st.markdown("""
        ### Enhanced Security Measures:
        1. **Advanced Input Sanitization**:
           - HTML escape
           - Control character removal
           - Whitespace normalization
           - UTF-8 invisible character removal
        
        2. **Pattern Detection Categories**:
           - Instruction override attempts
           - System command injection
           - Code injection
           - Markup injection
           - Role-playing attempts
           - Escaping attempts
           - Prompt manipulation
           - Data exfiltration attempts
        
        3. **Statistical Analysis**:
           - Special character ratio checking
           - Repetition pattern detection
           - Shannon entropy analysis
        
        4. **Additional Features**:
           - Detailed validation reporting
           - Pattern categorization
           - Position tracking of suspicious patterns
        """)

if __name__ == "__main__":
    main()
