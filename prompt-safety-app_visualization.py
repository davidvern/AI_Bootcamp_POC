import streamlit as st
import re
import html
import json
from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

# [Previous PromptSafetyChecker class remains the same until the validate_input method]

    def generate_pattern_visualization(self, text: str, findings: List[Dict]) -> go.Figure:
        """Generate a visualization of where patterns were detected in the text."""
        if not findings:
            return None
        
        # Create a list of pattern occurrences
        pattern_locations = []
        colors = px.colors.qualitative.Set3
        color_map = {}
        current_color = 0
        
        for finding in findings:
            category = finding['category']
            if category not in color_map:
                color_map[category] = colors[current_color % len(colors)]
                current_color += 1
            
            start, end = finding['position']
            pattern_locations.append({
                'category': category,
                'start': start,
                'end': end,
                'text': finding['matched_text'],
                'color': color_map[category]
            })
        
        # Create the visualization
        fig = go.Figure()
        
        # Add the base text line
        fig.add_shape(
            type="line",
            x0=0,
            x1=len(text),
            y0=0,
            y1=0,
            line=dict(color="gray", width=2)
        )
        
        # Add markers for each pattern
        for loc in pattern_locations:
            # Add a rectangle for the pattern
            fig.add_shape(
                type="rect",
                x0=loc['start'],
                x1=loc['end'],
                y0=-0.2,
                y1=0.2,
                fillcolor=loc['color'],
                opacity=0.5,
                line_width=0,
            )
            
            # Add annotation
            fig.add_annotation(
                x=(loc['start'] + loc['end']) / 2,
                y=0.3,
                text=f"{loc['category']}<br>{loc['text']}",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor=loc['color'],
                font=dict(size=10)
            )
        
        fig.update_layout(
            title="Pattern Detection Visualization",
            showlegend=False,
            height=300,
            yaxis_range=[-0.5, 1],
            yaxis_visible=False,
            xaxis_title="Character Position"
        )
        
        return fig

    def generate_metrics_visualization(self, text: str) -> Dict[str, go.Figure]:
        """Generate visualizations for various text metrics."""
        visualizations = {}
        
        # Character distribution
        char_counts = Counter(text)
        char_df = pd.DataFrame([
            {'character': char, 'count': count}
            for char, count in char_counts.items()
        ]).sort_values('count', ascending=False)
        
        fig_chars = px.bar(
            char_df.head(20),
            x='character',
            y='count',
            title='Character Distribution (Top 20)',
            labels={'character': 'Character', 'count': 'Frequency'}
        )
        visualizations['char_dist'] = fig_chars
        
        # Metrics gauge charts
        entropy_ratio = self.calculate_entropy(text)
        repetition_ratio = self.check_repetition(text)
        special_chars = sum(1 for c in text if not c.isalnum() and not c.isspace())
        special_chars_ratio = special_chars / len(text) if text else 0
        
        metrics_data = [
            ('Entropy', entropy_ratio, self.min_entropy_ratio, 'Higher is better'),
            ('Repetition', repetition_ratio, self.max_repetition_ratio, 'Lower is better'),
            ('Special Chars', special_chars_ratio, self.max_special_chars_ratio, 'Lower is better')
        ]
        
        for name, value, threshold, direction in metrics_data:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=value,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': f"{name} Ratio"},
                gauge={
                    'axis': {'range': [0, 1]},
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': threshold
                    },
                    'steps': [
                        {'range': [0, threshold], 'color': "lightgray"},
                        {'range': [threshold, 1], 'color': "gray"}
                    ]
                }
            ))
            fig.update_layout(height=200)
            visualizations[f'{name.lower()}_gauge'] = fig
        
        return visualizations

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
    user_input = st.text_area("Enter your prompt:", max_chars=1000)
    
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
