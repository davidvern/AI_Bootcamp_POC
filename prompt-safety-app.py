import streamlit as st
import re
import html
from typing import List, Dict, Optional


from helper_functions.prompt_safety_app_security import PromptSafetyChecker

# class PromptSafetyChecker:
#     def __init__(self):
#         # Common prompt injection patterns
#         self.suspicious_patterns = [
#             r"ignore previous instructions",
#             r"disregard (?:all )?(?:previous )?(?:instructions|prompts)",
#             r"forget (?:all )?(?:previous )?(?:instructions|prompts)",
#             r"new instruction:",
#             r"system prompt:",
#             r"you are now",
#             r"act as",
#             r"<\/?[a-z][\s\S]*>",  # HTML/XML tags
#             r"\[.*?\]\(.*?\)",      # Markdown links
#             r"```.*?```",           # Code blocks
#         ]
        
#         # Maximum allowed input length
#         self.max_input_length = 1000
        
#         # Keep track of user inputs for rate limiting
#         self.user_inputs: Dict[str, List[float]] = {}
        
#     def sanitize_input(self, text: str) -> str:
#         """Sanitize user input by escaping special characters."""
#         # HTML escape to prevent XSS
#         text = html.escape(text)
#         # Remove any control characters
#         text = ''.join(char for char in text if ord(char) >= 32)
#         return text.strip()
    
#     def check_suspicious_patterns(self, text: str) -> List[str]:
#         """Check for suspicious patterns that might indicate prompt injection attempts."""
#         findings = []
#         for pattern in self.suspicious_patterns:
#             if re.search(pattern, text, re.IGNORECASE):
#                 findings.append(f"Suspicious pattern detected: {pattern}")
#         return findings
    
#     def validate_input(self, text: str) -> tuple[bool, Optional[str]]:
#         """Validate user input for potential security issues."""
#         # Check input length
#         if len(text) > self.max_input_length:
#             return False, f"Input exceeds maximum length of {self.max_input_length} characters"
        
#         # Check for suspicious patterns
#         findings = self.check_suspicious_patterns(text)
#         if findings:
#             return False, "Potential prompt injection detected:\n" + "\n".join(findings)
        
#         return True, None

def main():
    st.title("Secure Prompt Input System")
    
    # Initialize the safety checker
    if 'safety_checker' not in st.session_state:
        st.session_state.safety_checker = PromptSafetyChecker()
    
    # Add a description
    st.markdown("""
    This application demonstrates prompt safety measures to prevent prompt injection attacks.
    It includes:
    - Input sanitization
    - Pattern matching for common prompt injection attempts
    - Length validation
    - Input history tracking
    """)
    
    # User input
    user_input = st.text_area("Enter your prompt:", max_chars=1000)
    
    if st.button("Submit"):
        if user_input:
            # Sanitize input
            sanitized_input = st.session_state.safety_checker.sanitize_input(user_input)
            
            # Validate input
            is_valid, error_message = st.session_state.safety_checker.validate_input(sanitized_input)
            
            if is_valid:
                st.success("Input validated successfully!")
                st.write("Sanitized input:", sanitized_input)
            else:
                st.error(error_message)
                st.warning("Please modify your input and try again.")
        else:
            st.warning("Please enter some text.")
    
    # Display safety information
    with st.expander("Security Information"):
        st.markdown("""
        ### Security Measures:
        1. **Input Sanitization**: Removes potentially dangerous characters and HTML escapes the input
        2. **Pattern Matching**: Checks for common prompt injection patterns
        3. **Length Validation**: Ensures input doesn't exceed maximum allowed length
        4. **Input History**: Tracks user inputs for rate limiting (not implemented in this demo)
        
        ### Blocked Patterns Include:
        - Attempts to ignore or override instructions
        - System prompt modifications
        - Role-playing commands
        - HTML/XML injection
        - Markdown injection
        - Code block injection
        """)

if __name__ == "__main__":
    main()
