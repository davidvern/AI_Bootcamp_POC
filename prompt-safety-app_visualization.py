import streamlit as st
from helper_functions.prompt_safety_app_security import PromptSafetyChecker

def main():
    st.title("Enhanced Secure Prompt Input System with Visualizations")
    
    # Initialize the safety checker
    if 'safety_checker' not in st.session_state:
        st.session_state.safety_checker = PromptSafetyChecker()
    
    # Add a description
    st.markdown("""
    This application demonstrates advanced prompt safety measures with visual analysis tools.
    It includes:
    - Pattern detection visualization
    - Character distribution analysis
    - Security metrics visualization
    - Real-time analysis feedback
    """)
    
    # User input
    user_input = st.text_area("Enter your prompt:", max_chars=1000,height=300)
    
    if user_input:
        # Sanitize input
        sanitized_input = st.session_state.safety_checker.sanitize_input(user_input)
        
        # Validate input and get visualizations
        is_valid, error_message, validation_results = st.session_state.safety_checker.validate_input(sanitized_input)
        
        # Create tabs for different visualizations
        tabs = st.tabs(["Results", "Pattern Analysis", "Metrics", "Details"])
        
        with tabs[0]:
            if is_valid:
                st.success("Input validated successfully!")
                st.write("Sanitized input:", sanitized_input)
            else:
                st.error(error_message)
                st.warning("Please modify your input and try again.")
        
        with tabs[1]:
            st.subheader("Pattern Detection")
            pattern_viz = st.session_state.safety_checker.generate_pattern_visualization(
                sanitized_input,
                validation_results[-1].get('findings', []) if validation_results else []
            )
            if pattern_viz:
                st.plotly_chart(pattern_viz, use_container_width=True)
            else:
                st.info("No suspicious patterns detected.")
        
        with tabs[2]:
            st.subheader("Text Analysis Metrics")
            metrics_viz = st.session_state.safety_checker.generate_metrics_visualization(sanitized_input)
            
            # Display metrics in columns
            col1, col2, col3 = st.columns(3)
            with col1:
                st.plotly_chart(metrics_viz['entropy_gauge'], use_container_width=True)
            with col2:
                st.plotly_chart(metrics_viz['repetition_gauge'], use_container_width=True)
            with col3:
                st.plotly_chart(metrics_viz['special_chars_gauge'], use_container_width=True)
            
            # Character distribution
            st.plotly_chart(metrics_viz['char_dist'], use_container_width=True)
        
        with tabs[3]:
            st.subheader("Detailed Analysis Results")
            if validation_results:
                st.json(validation_results)
            else:
                st.info("No validation issues found.")
    
    # Display enhanced security information
    with st.expander("Security Information"):
        st.markdown("""
        ### Visualization Features:
        1. **Pattern Detection Visualization**:
           - Visual representation of detected patterns in text
           - Color-coded by pattern category
           - Position indicators for pattern matches
        
        2. **Metrics Visualization**:
           - Entropy ratio gauge
           - Repetition detection gauge
           - Special character ratio gauge
           - Character distribution analysis
        
        3. **Analysis Tabs**:
           - Results summary
           - Pattern analysis
           - Metrics visualization
           - Detailed validation results
        
        4. **Real-time Analysis**:
           - Immediate visual feedback
           - Interactive charts
           - Detailed pattern information
        """)

if __name__ == "__main__":
    main()
