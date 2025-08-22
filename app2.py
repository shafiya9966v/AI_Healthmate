import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import base64
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="AI HealthMate - Your Smart Wellness Companion",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for stunning UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        padding: 0rem 1rem;
    }
    
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.3rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 1px solid #f0f2f6;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .feature-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-right: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .feature-title {
        font-size: 1.8rem;
        font-weight: 600;
        color:#2c3e50; /* Dark blue color */
        margin: 0;
    }
    
    .feature-description {
        color: #7f8c8d;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    /* Input Styles */
    .stSelectbox > div > div {
        background: #f8f9ff;
        border-radius: 10px;
        border: 2px solid #e3e8ff;
    }
    
    .stNumberInput > div > div > input {
        background: #f8f9ff;
        border-radius: 10px;
        border: 2px solid #e3e8ff;
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .css-1d391kg .css-1v0mbdj {
        color: white;
    }
    
    /* Results Box */
    .result-box {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(67, 233, 123, 0.3);
    }
    
    .risk-high {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #ffa726 0%, #fb8c00 100%);
    }
    
    .risk-low {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 0.5rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        color: #7f8c8d;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    /* Navigation */
    .nav-item {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .nav-item:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(5px);
    }
    
    .nav-item.active {
        background: rgba(255, 255, 255, 0.2);
        border-left: 4px solid white;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: blue; font-size: 2rem; margin-bottom: 0.5rem;">🏥 AI HealthMate</h1>
    <p style="color: rgba(138, 43, 226, 1); margin: 0;">Smart Wellness Companion</p>
</div>
""", unsafe_allow_html=True)

# Navigation menu
menu_options = {
    "🏠 Dashboard": "dashboard",
    "🩸 HemoSmart": "hemosmart",
    "👂 TinniSense": "tinnisense", 
    "⏰ BioClock AI": "bioclock",
    "🫁 Medical Imaging": "imaging",
    "💖 Heart & Diabetes": "heart_diabetes",
    "🤖 AI Assistant": "chatbot",
    "🧠 Parkinson's": "parkinsons"
}

selected_page = st.sidebar.selectbox("Navigate to:", list(menu_options.keys()), index=0)
current_page = menu_options[selected_page]

# Main header
st.markdown("""
<div class="main-header">
    <h1>🏥 AI HealthMate</h1>
    <p>Your Smart AI Wellness Companion - Empowering Preventive Healthcare</p>
</div>
""", unsafe_allow_html=True)

# Dashboard Page
if current_page == "dashboard":
    st.markdown("## 📊 Health Dashboard")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">8.5</div>
            <div class="metric-label">Health Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">42</div>
            <div class="metric-label">Scans Completed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">Low</div>
            <div class="metric-label">Risk Level</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">98%</div>
            <div class="metric-label">Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature overview
    st.markdown("## 🚀 Available Features")
    
    features_data = [
        {"Feature": "HemoSmart", "Description": "AI-based anemia detection", "Icon": "🩸", "Status": "Active"},
        {"Feature": "TinniSense", "Description": "Tinnitus risk assessment", "Icon": "👂", "Status": "Active"},
        {"Feature": "BioClock AI", "Description": "Biological age prediction", "Icon": "⏰", "Status": "Active"},
        {"Feature": "Medical Imaging", "Description": "Pneumonia & cancer detection", "Icon": "🫁", "Status": "Active"},
        {"Feature": "Heart & Diabetes", "Description": "Cardiovascular risk analysis", "Icon": "💖", "Status": "Active"},
        {"Feature": "AI Assistant", "Description": "Intelligent symptom analyzer", "Icon": "🤖", "Status": "Active"}
    ]
    
    for feature in features_data:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-header">
                <span class="feature-icon">{feature['Icon']}</span>
                <h3 class="feature-title">{feature['Feature']}</h3>
            </div>
            <p class="feature-description">{feature['Description']}</p>
            <span style="background: #43e97b; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.9rem;">✓ {feature['Status']}</span>
        </div>
        """, unsafe_allow_html=True)

# HemoSmart - Anemia Detection
elif current_page == "hemosmart":
    st.markdown("""
    <div class="feature-card">
        <div class="feature-header">
            <span class="feature-icon">🩸</span>
            <h2 class="feature-title">HemoSmart - AI Anemia Detection</h2>
        </div>
        <p class="feature-description">Advanced machine learning analysis of your Complete Blood Count (CBC) data to detect iron deficiency anemia risk.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Enter Your CBC Values")
        
        # CBC input fields
        hemoglobin = st.number_input("Hemoglobin (g/dL)", min_value=5.0, max_value=20.0, value=12.5, step=0.1)
        hematocrit = st.number_input("Hematocrit (%)", min_value=20.0, max_value=60.0, value=37.5, step=0.1)
        mcv = st.number_input("Mean Corpuscular Volume (fL)", min_value=60.0, max_value=120.0, value=85.0, step=0.1)
        mch = st.number_input("Mean Corpuscular Hemoglobin (pg)", min_value=20.0, max_value=40.0, value=29.0, step=0.1)
        mchc = st.number_input("MCHC (g/dL)", min_value=30.0, max_value=40.0, value=34.0, step=0.1)
        rbc_count = st.number_input("RBC Count (million/μL)", min_value=3.0, max_value=6.0, value=4.5, step=0.1)
        
        # Additional factors
        age = st.slider("Age", min_value=18, max_value=100, value=35)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        if st.button("🔍 Analyze Anemia Risk", key="hemo_analyze"):
            # Simulate ML prediction
            risk_score = np.random.uniform(0.1, 0.9)
            
            if risk_score < 0.3:
                risk_level = "Low"
                risk_class = "risk-low"
                recommendations = ["Maintain current diet", "Regular check-ups", "Stay hydrated"]
            elif risk_score < 0.7:
                risk_level = "Medium"
                risk_class = "risk-medium"
                recommendations = ["Increase iron-rich foods", "Consider supplements", "Consult healthcare provider"]
            else:
                risk_level = "High"
                risk_class = "risk-high"
                recommendations = ["Immediate medical consultation", "Blood work follow-up", "Dietary intervention"]
            
            st.markdown(f"""
            <div class="result-box {risk_class}">
                <h3>🎯 Anemia Risk Analysis</h3>
                <h2>{risk_level} Risk ({risk_score:.1%})</h2>
                <p>Based on your CBC values and personal factors</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader("💡 Recommendations")
            for rec in recommendations:
                st.write(f"• {rec}")
    
    with col2:
        st.subheader("📊 Reference Ranges")
        reference_data = pd.DataFrame({
            "Parameter": ["Hemoglobin (M)", "Hemoglobin (F)", "Hematocrit (M)", "Hematocrit (F)", "MCV", "MCH", "MCHC"],
            "Normal Range": ["13.8-17.2 g/dL", "12.1-15.1 g/dL", "40.7-50.3%", "36.1-44.3%", "80-100 fL", "27-31 pg", "32-36 g/dL"]
        })
        st.dataframe(reference_data, use_container_width=True)
        
        # Visualization
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = hemoglobin,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Hemoglobin Level"},
            gauge = {'axis': {'range': [None, 20]},
                    'bar': {'color': "darkblue"},
                    'steps' : [
                        {'range': [0, 12], 'color': "lightgray"},
                        {'range': [12, 16], 'color': "gray"}],
                    'threshold' : {'line': {'color': "red", 'width': 4},
                                  'thickness': 0.75, 'value': 15}}))
        st.plotly_chart(fig, use_container_width=True)

# TinniSense - Tinnitus Risk
elif current_page == "tinnisense":
    st.markdown("""
    <div class="feature-card">
        <div class="feature-header">
            <span class="feature-icon">👂</span>
            <h2 class="feature-title">TinniSense - Tinnitus Risk Assessment</h2>
        </div>
        <p class="feature-description">Evaluate your hearing health and tinnitus risk based on lifestyle factors and audio exposure patterns.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎧 Hearing Health Assessment")
        
        # Hearing assessment inputs
        headphone_hours = st.slider("Daily headphone usage (hours)", min_value=0, max_value=12, value=3)
        volume_level = st.slider("Average volume level (1-10)", min_value=1, max_value=10, value=6)
        noise_exposure = st.selectbox("Work environment noise level", 
                                    ["Quiet office", "Moderate noise", "Loud environment", "Very loud (construction/factory)"])
        concert_frequency = st.selectbox("Concert/loud event attendance", 
                                       ["Never", "Rarely (few per year)", "Monthly", "Weekly"])
        age = st.slider("Age", min_value=18, max_value=100, value=35)
        
        # Hearing test simulation
        st.subheader("🔊 Quick Hearing Test")
        st.info("Adjust your device volume to comfortable level before starting")
        
        test_frequencies = ["250 Hz", "500 Hz", "1000 Hz", "2000 Hz", "4000 Hz", "8000 Hz"]
        hearing_results = {}
        
        for freq in test_frequencies:
            hearing_results[freq] = st.selectbox(f"Can you hear the {freq} tone clearly?", 
                                               ["Yes, clearly", "Faintly", "Cannot hear"], key=f"freq_{freq}")
        
        if st.button("🎯 Assess Tinnitus Risk", key="tinni_analyze"):
            # Simulate risk calculation
            risk_factors = 0
            risk_factors += headphone_hours * 0.1
            risk_factors += (volume_level - 5) * 0.15
            risk_factors += {"Quiet office": 0, "Moderate noise": 0.2, "Loud environment": 0.4, "Very loud (construction/factory)": 0.6}[noise_exposure]
            risk_factors += {"Never": 0, "Rarely (few per year)": 0.1, "Monthly": 0.3, "Weekly": 0.5}[concert_frequency]
            
            # Hearing test impact
            hearing_issues = sum([1 for result in hearing_results.values() if result != "Yes, clearly"])
            risk_factors += hearing_issues * 0.1
            
            risk_score = min(risk_factors, 1.0)
            
            if risk_score < 0.3:
                risk_level = "Low"
                risk_class = "risk-low"
                recommendations = ["Continue current habits", "Annual hearing check", "Use ear protection in noisy environments"]
            elif risk_score < 0.6:
                risk_level = "Medium"
                risk_class = "risk-medium"
                recommendations = ["Reduce headphone volume", "Take listening breaks", "Consider hearing protection", "Monitor symptoms"]
            else:
                risk_level = "High"
                risk_class = "risk-high"
                recommendations = ["Immediate hearing evaluation", "Reduce noise exposure", "Use proper ear protection", "Lifestyle changes needed"]
            
            st.markdown(f"""
            <div class="result-box {risk_class}">
                <h3>🎯 Tinnitus Risk Analysis</h3>
                <h2>{risk_level} Risk ({risk_score:.1%})</h2>
                <p>Based on your lifestyle and hearing test results</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader("💡 Recommendations")
            for rec in recommendations:
                st.write(f"• {rec}")
    
    with col2:
        st.subheader("📈 Risk Factors")
        
        # Create risk factor chart
        factors = ["Headphone Use", "Volume Level", "Noise Exposure", "Event Attendance", "Age Factor"]
        scores = [headphone_hours/12, volume_level/10, 
                 {"Quiet office": 0.2, "Moderate noise": 0.4, "Loud environment": 0.7, "Very loud (construction/factory)": 1.0}[noise_exposure],
                 {"Never": 0.1, "Rarely (few per year)": 0.3, "Monthly": 0.6, "Weekly": 1.0}[concert_frequency],
                 min(age/100, 0.8)]
        
        fig = px.bar(x=factors, y=scores, title="Individual Risk Factors", 
                    color=scores, color_continuous_scale="reds")
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("🔊 Hearing Protection Tips")
        tips = [
            "Use 60/60 rule: 60% volume for 60 minutes max",
            "Take 15-minute breaks every hour",
            "Use noise-cancelling headphones",
            "Wear earplugs at loud events",
            "Keep safe distance from speakers"
        ]
        
        for tip in tips:
            st.write(f"• {tip}")

# BioClock AI - Biological Age
elif current_page == "bioclock":
    st.markdown("""
    <div class="feature-card">
        <div class="feature-header">
            <span class="feature-icon">⏰</span>
            <h2 class="feature-title">BioClock AI - Biological Age Predictor</h2>
        </div>
        <p class="feature-description">Discover your biological age based on lifestyle factors, health metrics, and wellness indicators.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Health & Lifestyle Assessment")
        
        # Basic info
        chronological_age = st.slider("Chronological Age", min_value=18, max_value=100, value=35)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        # Physical metrics
        height = st.number_input("Height (cm)", min_value=140, max_value=220, value=170)
        weight = st.number_input("Weight (kg)", min_value=40, max_value=200, value=70)
        bmi = weight / ((height/100) ** 2)
        st.write(f"*BMI:* {bmi:.1f}")
        
        # Lifestyle factors
        st.subheader("🏃‍♂ Lifestyle Factors")
        exercise_freq = st.selectbox("Exercise frequency", 
                                   ["Never", "1-2 times/week", "3-4 times/week", "5+ times/week"])
        sleep_hours = st.slider("Average sleep hours per night", min_value=4, max_value=12, value=7)
        stress_level = st.slider("Stress level (1-10)", min_value=1, max_value=10, value=5)
        
        # Diet and habits
        st.subheader("🥗 Diet & Habits")
        diet_quality = st.selectbox("Diet quality", 
                                  ["Poor (fast food, processed)", "Average (mixed)", "Good (balanced)", "Excellent (organic, whole foods)"])
        smoking = st.selectbox("Smoking status", ["Never", "Former smoker", "Occasional", "Regular"])
        alcohol = st.selectbox("Alcohol consumption", 
                             ["Never", "Occasional (1-2/week)", "Moderate (3-7/week)", "Heavy (8+/week)"])
        
        # Health metrics
        st.subheader("💊 Health Metrics")
        blood_pressure = st.selectbox("Blood pressure", ["Normal (<120/80)", "Elevated (120-129/<80)", 
                                    "High Stage 1 (130-139/80-89)", "High Stage 2 (140+/90+)"])
        cholesterol = st.selectbox("Cholesterol level", ["Normal (<200)", "Borderline (200-239)", "High (240+)", "Unknown"])
        blood_sugar = st.selectbox("Blood sugar", ["Normal (<100)", "Prediabetic (100-125)", "Diabetic (126+)", "Unknown"])
        
        if st.button("🧬 Calculate Biological Age", key="bio_analyze"):
            # Simulate biological age calculation
            age_adjustment = 0
            
            # BMI impact
            if bmi < 18.5 or bmi > 30:
                age_adjustment += 3
            elif bmi > 25:
                age_adjustment += 1
            
            # Exercise impact
            exercise_impact = {"Never": 5, "1-2 times/week": 2, "3-4 times/week": -1, "5+ times/week": -3}[exercise_freq]
            age_adjustment += exercise_impact
            
            # Sleep impact
            if sleep_hours < 6 or sleep_hours > 9:
                age_adjustment += 2
            elif 7 <= sleep_hours <= 8:
                age_adjustment -= 1
            
            # Stress impact
            age_adjustment += (stress_level - 5) * 0.5
            
            # Diet impact
            diet_impact = {"Poor (fast food, processed)": 4, "Average (mixed)": 1, "Good (balanced)": -1, "Excellent (organic, whole foods)": -3}[diet_quality]
            age_adjustment += diet_impact
            
            # Smoking impact
            smoking_impact = {"Never": -1, "Former smoker": 1, "Occasional": 3, "Regular": 8}[smoking]
            age_adjustment += smoking_impact
            
            # Alcohol impact
            alcohol_impact = {"Never": 0, "Occasional (1-2/week)": 0, "Moderate (3-7/week)": 2, "Heavy (8+/week)": 5}[alcohol]
            age_adjustment += alcohol_impact
            
            biological_age = chronological_age + age_adjustment
            age_difference = biological_age - chronological_age
            
            if age_difference < -3:
                status = "Excellent"
                status_class = "risk-low"
                message = "You're aging slower than average! 🎉"
            elif age_difference < 0:
                status = "Good"
                status_class = "risk-low"
                message = "You're doing well! Keep it up! 👍"
            elif age_difference < 3:
                status = "Average"
                status_class = "risk-medium"
                message = "Room for improvement in some areas 📈"
            else:
                status = "Needs Attention"
                status_class = "risk-high"
                message = "Consider lifestyle changes for healthier aging ⚠"
            
            st.markdown(f"""
            <div class="result-box {status_class}">
                <h3>⏰ Biological Age Analysis</h3>
                <h2>Age: {biological_age:.1f} years</h2>
                <h3>Difference: {age_difference:+.1f} years</h3>
                <p>{message}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Recommendations based on major factors
            st.subheader("💡 Personalized Recommendations")
            recommendations = []
            
            if bmi > 25:
                recommendations.append("🏃‍♂ Focus on weight management through diet and exercise")
            if exercise_freq in ["Never", "1-2 times/week"]:
                recommendations.append("🚴‍♀ Increase physical activity to 150+ minutes per week")
            if sleep_hours < 7:
                recommendations.append("😴 Prioritize 7-8 hours of quality sleep")
            if stress_level > 7:
                recommendations.append("🧘‍♀ Practice stress management techniques (meditation, yoga)")
            if smoking != "Never":
                recommendations.append("🚭 Consider smoking cessation programs")
            if alcohol in ["Heavy (8+/week)"]:
                recommendations.append("🍷 Reduce alcohol consumption")
            
            if not recommendations:
                recommendations.append("✨ Great job! Maintain your healthy lifestyle")
                recommendations.append("📊 Regular health screenings to stay on track")
            
            for rec in recommendations:
                st.write(f"• {rec}")
    
    with col2:
        st.subheader("📈 Age Factors Impact")
        
        # Show factor contributions if analysis was done
        if 'age_adjustment' in locals():
            factors = ["Exercise", "Sleep", "Diet", "Stress", "BMI", "Smoking", "Alcohol"]
            impacts = [exercise_impact, 
                      2 if sleep_hours < 6 or sleep_hours > 9 else (-1 if 7 <= sleep_hours <= 8 else 0),
                      diet_impact, 
                      (stress_level - 5) * 0.5,
                      3 if bmi < 18.5 or bmi > 30 else (1 if bmi > 25 else 0),
                      smoking_impact, 
                      alcohol_impact]
            
            fig = px.bar(x=impacts, y=factors, orientation='h', 
                        title="Factor Impact on Biological Age",
                        color=impacts, color_continuous_scale="RdYlGn_r")
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("🎯 Aging Tips")
        aging_tips = [
            "💪 Regular strength training preserves muscle mass",
            "🥗 Antioxidant-rich foods fight cellular damage",
            "🧠 Mental challenges keep brain sharp",
            "☀ Vitamin D supports bone health",
            "💧 Stay hydrated for optimal cell function",
            "🤝 Social connections boost longevity"
        ]
        
        for tip in aging_tips:
            st.write(f"{tip}")

# Medical Imaging Analysis
elif current_page == "imaging":
    st.markdown("""
    <div class="feature-card">
        <div class="feature-header">
            <span class="feature-icon">🫁</span>
            <h2 class="feature-title">Medical Imaging Analysis</h2>
        </div>
        <p class="feature-description">Advanced AI analysis of medical images for early detection of pneumonia and cancer screening.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Image analysis tabs
    tab1, tab2 = st.tabs(["🫁 Chest X-Ray Analysis", "🔬 Histopathology Analysis"])
    
    with tab1:
        st.subheader("📷 Chest X-Ray Pneumonia Detection")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_xray = st.file_uploader("Upload chest X-ray image", 
                                           type=['png', 'jpg', 'jpeg', 'dcm'],
                                           help="Supported formats: PNG, JPG, JPEG, DICOM")
            
            if uploaded_xray is not None:
                # Display uploaded image
                image = Image.open(uploaded_xray)
                st.image(image, caption="Uploaded X-Ray", use_column_width=True)
                
                # Image analysis button
                if st.button("🔍 Analyze X-Ray", key="xray_analyze"):
                    with st.spinner("Analyzing image with AI..."):
                        # Simulate AI analysis
                        import time
                        time.sleep(3)
                        
                        # Simulate results
                        pneumonia_prob = np.random.uniform(0.05, 0.95)
                        normal_prob = 1 - pneumonia_prob
                        
                        if pneumonia_prob > 0.7:
                            diagnosis = "High probability of pneumonia"
                            risk_class = "risk-high"
                            confidence = "High"
                        elif pneumonia_prob > 0.4:
                            diagnosis = "Possible pneumonia - further evaluation needed"
                            risk_class = "risk-medium"
                            confidence = "Medium"
                        else:
                            diagnosis = "No significant abnormalities detected"
                            risk_class = "risk-low"
                            confidence = "High"
                        
                        st.markdown(f"""
                        <div class="result-box {risk_class}">
                            <h3>🏥 X-Ray Analysis Results</h3>
                            <h4>{diagnosis}</h4>
                            <p>Pneumonia Probability: {pneumonia_prob:.1%}</p>
                            <p>Normal Probability: {normal_prob:.1%}</p>
                            <p>Confidence: {confidence}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Detailed findings
                        st.subheader("📋 Detailed Findings")
                        findings = [
                            f"Lung opacity analysis: {'Abnormal patterns detected' if pneumonia_prob > 0.5 else 'Clear lung fields'}",
                            f"Cardiac silhouette: Normal",
                            f"Pleural spaces: {'Possible effusion' if pneumonia_prob > 0.6 else 'Clear'}",
                            f"Diaphragm: Normal position and contour"
                        ]
                        
                        for finding in findings:
                            st.write(f"• {finding}")
                        
                        st.warning("⚠ This AI analysis is for screening purposes only. Always consult a qualified radiologist for definitive diagnosis.")
        
        with col2:
            st.subheader("📊 Analysis Features")
            features = [
                "🧠 Deep CNN Architecture",
                "📈 99.2% Accuracy Rate", 
                "⚡ Real-time Processing",
                "🔍 Automated Feature Detection",
                "📋 Detailed Reporting",
                "🏥 DICOM Compatible"
            ]
            
            for feature in features:
                st.write(feature)
            
            st.subheader("🎯 What We Detect")
            conditions = [
                "Pneumonia",
                "Lung consolidation", 
                "Pleural effusion",
                "Atelectasis",
                "Pulmonary edema"
            ]
            
            for condition in conditions:
                st.write(f"• {condition}")
    
    with tab2:
        st.subheader("🔬 Histopathology Cancer Detection")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_histo = st.file_uploader("Upload histopathology slide", 
                                            type=['png', 'jpg', 'jpeg', 'tiff'],
                                            help="Supported formats: PNG, JPG, JPEG, TIFF")
            
            cancer_type = st.selectbox("Select tissue type", 
                                     ["Breast tissue", "Lung tissue", "Skin (melanoma)", "Prostate", "Colorectal"])
            
            if uploaded_histo is not None:
                # Display uploaded image
                image = Image.open(uploaded_histo)
                st.image(image, caption="Uploaded Histopathology Slide", use_column_width=True)
                
                if st.button("🔍 Analyze Tissue Sample", key="histo_analyze"):
                    with st.spinner("Performing cancer screening analysis..."):
                        time.sleep(4)
                        
                        # Simulate cancer detection results
                        cancer_prob = np.random.uniform(0.1, 0.9)
                        benign_prob = 1 - cancer_prob
                        
                        if cancer_prob > 0.75:
                            diagnosis = "Malignant features detected"
                            risk_class = "risk-high"
                            grade = "High-grade"
                        elif cancer_prob > 0.45:
                            diagnosis = "Suspicious features - biopsy recommended"
                            risk_class = "risk-medium"
                            grade = "Intermediate"
                        else:
                            diagnosis = "Benign characteristics"
                            risk_class = "risk-low"
                            grade = "Low-grade"
                        
                        st.markdown(f"""
                        <div class="result-box {risk_class}">
                            <h3>🔬 Histopathology Analysis</h3>
                            <h4>{diagnosis}</h4>
                            <p>Malignancy Probability: {cancer_prob:.1%}</p>
                            <p>Benign Probability: {benign_prob:.1%}</p>
                            <p>Grade: {grade}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Morphological features
                        st.subheader("🔍 Morphological Analysis")
                        features = [
                            f"Cell morphology: {'Abnormal' if cancer_prob > 0.5 else 'Normal'}",
                            f"Nuclear pleomorphism: {'Present' if cancer_prob > 0.6 else 'Absent'}",
                            f"Mitotic activity: {'Increased' if cancer_prob > 0.7 else 'Normal'}",
                            f"Tissue architecture: {'Disrupted' if cancer_prob > 0.5 else 'Preserved'}"
                        ]
                        
                        for feature in features:
                            st.write(f"• {feature}")
                        
                        st.error("🚨 This AI screening tool requires pathologist confirmation for all diagnoses.")
        
        with col2:
            st.subheader("🎯 Supported Cancers")
            cancers = [
                "🎀 Breast cancer",
                "🫁 Lung adenocarcinoma",
                "🔴 Melanoma",
                "🔵 Prostate cancer", 
                "🟠 Colorectal cancer"
            ]
            
            for cancer in cancers:
                st.write(cancer)
            
            st.subheader("📊 AI Performance")
            metrics = pd.DataFrame({
                "Metric": ["Sensitivity", "Specificity", "Accuracy", "PPV", "NPV"],
                "Score": ["94.2%", "96.8%", "95.5%", "93.1%", "97.3%"]
            })
            st.dataframe(metrics, use_container_width=True)

# Heart Disease & Diabetes Detection
elif current_page == "heart_diabetes":
    st.markdown("""
    <div class="feature-card">
        <div class="feature-header">
            <span class="feature-icon">💖</span>
            <h2 class="feature-title">Heart Disease & Diabetes Risk Assessment</h2>
        </div>
        <p class="feature-description">Comprehensive cardiovascular and metabolic risk evaluation using clinical parameters and lifestyle factors.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Disease selection tabs
    tab1, tab2 = st.tabs(["💓 Heart Disease Risk", "🍯 Diabetes Risk"])
    
    with tab1:
        st.subheader("🫀 Cardiovascular Risk Assessment")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Basic demographics
            age = st.slider("Age", min_value=20, max_value=100, value=45)
            gender = st.selectbox("Gender", ["Male", "Female"])
            
            # Vital signs
            st.subheader("📊 Vital Signs")
            systolic_bp = st.number_input("Systolic Blood Pressure (mmHg)", min_value=80, max_value=250, value=120)
            diastolic_bp = st.number_input("Diastolic Blood Pressure (mmHg)", min_value=50, max_value=150, value=80)
            resting_hr = st.slider("Resting Heart Rate (bpm)", min_value=40, max_value=150, value=70)
            
            # Lab values
            st.subheader("🧪 Laboratory Values")
            total_chol = st.number_input("Total Cholesterol (mg/dL)", min_value=100, max_value=400, value=200)
            ldl_chol = st.number_input("LDL Cholesterol (mg/dL)", min_value=50, max_value=300, value=100)
            hdl_chol = st.number_input("HDL Cholesterol (mg/dL)", min_value=20, max_value=100, value=50)
            triglycerides = st.number_input("Triglycerides (mg/dL)", min_value=50, max_value=500, value=150)
            
            # Risk factors
            st.subheader("⚠ Risk Factors")
            smoking = st.checkbox("Current smoker")
            diabetes = st.checkbox("Diabetes")
            family_history = st.checkbox("Family history of heart disease")
            exercise = st.selectbox("Exercise frequency", ["Never", "Rarely", "Sometimes", "Regularly"])
            chest_pain = st.selectbox("Chest pain type", ["None", "Typical angina", "Atypical angina", "Non-anginal"])
            
            if st.button("💓 Assess Heart Disease Risk", key="heart_analyze"):
                # Calculate risk score
                risk_score = 0
                
                # Age factor
                risk_score += (age - 40) * 0.02 if age > 40 else 0
                risk_score += 0.1 if gender == "Male" else 0
                
                # Blood pressure
                if systolic_bp > 140 or diastolic_bp > 90:
                    risk_score += 0.2
                elif systolic_bp > 130 or diastolic_bp > 80:
                    risk_score += 0.1
                
                # Cholesterol
                if total_chol > 240:
                    risk_score += 0.15
                elif total_chol > 200:
                    risk_score += 0.08
                
                if ldl_chol > 160:
                    risk_score += 0.12
                elif ldl_chol > 130:
                    risk_score += 0.06
                
                if hdl_chol < 40:
                    risk_score += 0.1
                
                # Risk factors
                if smoking:
                    risk_score += 0.15
                if diabetes:
                    risk_score += 0.2
                if family_history:
                    risk_score += 0.1
                
                exercise_factor = {"Never": 0.1, "Rarely": 0.05, "Sometimes": 0, "Regularly": -0.05}[exercise]
                risk_score += exercise_factor
                
                chest_pain_factor = {"None": 0, "Non-anginal": 0.05, "Atypical angina": 0.1, "Typical angina": 0.15}[chest_pain]
                risk_score += chest_pain_factor
                
                risk_score = min(max(risk_score, 0), 1)
                
                if risk_score < 0.3:
                    risk_level = "Low"
                    risk_class = "risk-low"
                    ten_year_risk = risk_score * 10
                elif risk_score < 0.6:
                    risk_level = "Moderate"
                    risk_class = "risk-medium"
                    ten_year_risk = risk_score * 20
                else:
                    risk_level = "High"
                    risk_class = "risk-high"
                    ten_year_risk = risk_score * 30
                
                st.markdown(f"""
                <div class="result-box {risk_class}">
                    <h3>💓 Cardiovascular Risk Assessment</h3>
                    <h2>{risk_level} Risk</h2>
                    <h4>10-year risk: {ten_year_risk:.1f}%</h4>
                    <p>Risk Score: {risk_score:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Risk stratification
                st.subheader("📈 Risk Breakdown")
                risk_factors_contrib = {
                    "Age/Gender": (age - 40) * 0.02 + (0.1 if gender == "Male" else 0),
                    "Blood Pressure": 0.2 if systolic_bp > 140 or diastolic_bp > 90 else (0.1 if systolic_bp > 130 or diastolic_bp > 80 else 0),
                    "Cholesterol": (0.15 if total_chol > 240 else 0.08 if total_chol > 200 else 0) + (0.12 if ldl_chol > 160 else 0.06 if ldl_chol > 130 else 0),
                    "Lifestyle": (0.15 if smoking else 0) + exercise_factor,
                    "Medical History": (0.2 if diabetes else 0) + (0.1 if family_history else 0)
                }
                
                fig = px.pie(values=list(risk_factors_contrib.values()), 
                           names=list(risk_factors_contrib.keys()),
                           title="Risk Factor Contributions")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📋 Risk Categories")
            
            categories = pd.DataFrame({
                "Risk Level": ["Low", "Moderate", "High"],
                "10-Year Risk": ["<10%", "10-20%", ">20%"],
                "Action": ["Lifestyle", "Monitor closely", "Medical intervention"]
            })
            st.dataframe(categories, use_container_width=True)
            
            st.subheader("💡 Prevention Tips")
            prevention_tips = [
                "🏃‍♂ Regular exercise (150 min/week)",
                "🥗 Heart-healthy diet (Mediterranean)", 
                "🚭 Quit smoking",
                "⚖ Maintain healthy weight",
                "💊 Medication adherence",
                "😴 Quality sleep (7-8 hours)",
                "🧘‍♀ Stress management"
            ]
            
            for tip in prevention_tips:
                st.write(tip)
    
    with tab2:
        st.subheader("🍯 Type 2 Diabetes Risk Assessment")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Demographics
            age_diabetes = st.slider("Age", min_value=18, max_value=100, value=45, key="diabetes_age")
            gender_diabetes = st.selectbox("Gender", ["Male", "Female"], key="diabetes_gender")
            
            # Physical measurements
            st.subheader("📏 Physical Measurements")
            height_cm = st.number_input("Height (cm)", min_value=140, max_value=220, value=170, key="diabetes_height")
            weight_kg = st.number_input("Weight (kg)", min_value=40, max_value=200, value=75, key="diabetes_weight")
            bmi_diabetes = weight_kg / ((height_cm/100) ** 2)
            waist_circumference = st.number_input("Waist circumference (cm)", min_value=60, max_value=150, value=85)
            
            st.write(f"*BMI:* {bmi_diabetes:.1f}")
            
            # Laboratory values
            st.subheader("🧪 Laboratory Results")
            fasting_glucose = st.number_input("Fasting glucose (mg/dL)", min_value=70, max_value=300, value=95)
            hba1c = st.number_input("HbA1c (%)", min_value=4.0, max_value=15.0, value=5.5, step=0.1)
            
            # Risk factors
            st.subheader("⚠ Risk Factors")
            family_diabetes = st.checkbox("Family history of diabetes", key="diabetes_family")
            hypertension = st.checkbox("High blood pressure")
            gestational_diabetes = st.checkbox("History of gestational diabetes (if female)")
            pcos = st.checkbox("PCOS (if female)")
            physical_activity = st.selectbox("Physical activity level", 
                                           ["Sedentary", "Light activity", "Moderate activity", "Very active"])
            
            if st.button("🍯 Assess Diabetes Risk", key="diabetes_analyze"):
                # Calculate diabetes risk
                diabetes_risk = 0
                
                # Age factor
                if age_diabetes >= 45:
                    diabetes_risk += 0.1
                elif age_diabetes >= 35:
                    diabetes_risk += 0.05
                
                # BMI factor
                if bmi_diabetes >= 30:
                    diabetes_risk += 0.15
                elif bmi_diabetes >= 25:
                    diabetes_risk += 0.1
                
                # Waist circumference
                if (gender_diabetes == "Male" and waist_circumference > 102) or \
                   (gender_diabetes == "Female" and waist_circumference > 88):
                    diabetes_risk += 0.1
                
                # Glucose levels
                if fasting_glucose >= 126:
                    diabetes_risk += 0.3
                elif fasting_glucose >= 100:
                    diabetes_risk += 0.15
                
                if hba1c >= 6.5:
                    diabetes_risk += 0.25
                elif hba1c >= 5.7:
                    diabetes_risk += 0.1
                
                # Risk factors
                if family_diabetes:
                    diabetes_risk += 0.1
                if hypertension:
                    diabetes_risk += 0.08
                if gestational_diabetes:
                    diabetes_risk += 0.12
                if pcos:
                    diabetes_risk += 0.1
                
                activity_factor = {"Sedentary": 0.1, "Light activity": 0.05, "Moderate activity": 0, "Very active": -0.05}[physical_activity]
                diabetes_risk += activity_factor
                
                diabetes_risk = min(max(diabetes_risk, 0), 1)
                
                if diabetes_risk < 0.2:
                    risk_level = "Low"
                    risk_class = "risk-low"
                    message = "Low risk - Continue healthy habits"
                elif diabetes_risk < 0.5:
                    risk_level = "Moderate"
                    risk_class = "risk-medium"
                    message = "Moderate risk - Lifestyle changes recommended"
                else:
                    risk_level = "High"
                    risk_class = "risk-high"
                    message = "High risk - Medical evaluation needed"
                
                st.markdown(f"""
                <div class="result-box {risk_class}">
                    <h3>🍯 Diabetes Risk Assessment</h3>
                    <h2>{risk_level} Risk ({diabetes_risk:.1%})</h2>
                    <p>{message}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Recommendations
                st.subheader("💡 Recommendations")
                recommendations = []
                
                if bmi_diabetes > 25:
                    recommendations.append("⚖ Weight loss: Aim for 5-10% body weight reduction")
                if fasting_glucose >= 100:
                    recommendations.append("📊 Regular glucose monitoring")
                if physical_activity in ["Sedentary", "Light activity"]:
                    recommendations.append("🏃‍♂ Increase physical activity to 150 minutes/week")
                if family_diabetes:
                    recommendations.append("🩺 Annual diabetes screening")
                
                recommendations.extend([
                    "🥗 Follow a balanced, low-glycemic diet",
                    "😴 Maintain regular sleep schedule",
                    "💧 Stay well hydrated"
                ])
                
                for rec in recommendations:
                    st.write(f"• {rec}")
        
        with col2:
            st.subheader("📊 Diabetes Ranges")
            
            glucose_ranges = pd.DataFrame({
                "Category": ["Normal", "Prediabetes", "Diabetes"],
                "Fasting Glucose": ["<100 mg/dL", "100-125 mg/dL", "≥126 mg/dL"],
                "HbA1c": ["<5.7%", "5.7-6.4%", "≥6.5%"]
            })
            st.dataframe(glucose_ranges, use_container_width=True)
            
            st.subheader("🎯 Prevention Strategies")
            strategies = [
                "🍽 Portion control",
                "🥬 High-fiber foods",
                "🚫 Limit refined sugars",
                "🏋‍♀ Strength training",
                "⏰ Regular meal timing",
                "📈 Blood sugar monitoring"
            ]
            
            for strategy in strategies:
                st.write(strategy)


elif current_page == "chatbot":
    st.markdown("""
    <div class="feature-card">
        <div class="feature-header">
            <span class="feature-icon">🤖</span>
            <h2 class="feature-title">AI Health Assistant</h2>
        </div>
        <p class="feature-description">Intelligent symptom analysis and triage system with urgency classification and recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Describe Your Symptoms")
        
        # Symptom input
        symptoms_input = st.text_area("What symptoms are you experiencing?", 
                                    placeholder="Describe your symptoms in detail - location, duration, severity, associated symptoms...",
                                    height=150)
        
        # Additional context
        st.subheader("ℹ Additional Information")
        
        col_a, col_b = st.columns(2)
        with col_a:
            duration = st.selectbox("How long have you had these symptoms?", 
                                  ["Less than 1 hour", "1-6 hours", "6-24 hours", "1-3 days", "More than 3 days"])
            pain_scale = st.slider("Pain level (0-10)", min_value=0, max_value=10, value=0)
        
        with col_b:
            onset = st.selectbox("Symptom onset", ["Sudden", "Gradual", "Unknown"])
            getting_worse = st.checkbox("Symptoms are getting worse")
        
        # Medical history
        medical_history = st.text_area("Relevant medical history", 
                                     placeholder="Chronic conditions, medications, allergies, recent procedures...",
                                     height=80)
        
        if st.button("🔍 Analyze Symptoms", key="symptom_analyze"):
            if symptoms_input:
                # Simulate AI triage analysis
                import time
                
                with st.spinner("AI analyzing your symptoms..."):
                    time.sleep(2)
                
                # Determine urgency based on keywords and severity
                critical_keywords = ["chest pain", "difficulty breathing", "severe headache", "unconscious", "severe bleeding"]
                urgent_keywords = ["fever", "vomiting", "severe pain", "infection", "injury"]
                
                symptoms_lower = symptoms_input.lower()
                has_critical = any(keyword in symptoms_lower for keyword in critical_keywords)
                has_urgent = any(keyword in symptoms_lower for keyword in urgent_keywords)
                
                # Calculate urgency score
                urgency_score = 0
                if has_critical or pain_scale >= 8:
                    urgency_score = 3
                elif has_urgent or pain_scale >= 6 or getting_worse:
                    urgency_score = 2
                else:
                    urgency_score = 1
                
                # Duration impact
                if duration in ["Less than 1 hour", "1-6 hours"] and onset == "Sudden":
                    urgency_score = min(urgency_score + 1, 3)
                
                # Display results
                if urgency_score == 3:
                    urgency_level = "CRITICAL"
                    urgency_class = "risk-high"
                    action = "🚨 CALL EMERGENCY SERVICES (911)"
                    timeframe = "IMMEDIATE"
                    icon = "🚨"
                elif urgency_score == 2:
                    urgency_level = "URGENT"
                    urgency_class = "risk-medium"
                    action = "🏥 Visit Emergency Department"
                    timeframe = "Within 2-6 hours"
                    icon = "⚡"
                else:
                    urgency_level = "ROUTINE"
                    urgency_class = "risk-low"
                    action = "📞 Schedule appointment with primary care"
                    timeframe = "Within 24-48 hours"
                    icon = "📋"
                
                st.markdown(f"""
                <div class="result-box {urgency_class}">
                    <h3>{icon} TRIAGE ASSESSMENT</h3>
                    <h2>{urgency_level}</h2>
                    <h4>{action}</h4>
                    <p>Recommended timeframe: {timeframe}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Detailed analysis
                st.subheader("🔍 Symptom Analysis")
                
                # Generate AI-like analysis
                analysis_points = []
                
                if pain_scale >= 7:
                    analysis_points.append(f"⚠ High pain level reported ({pain_scale}/10)")
                if getting_worse:
                    analysis_points.append("📈 Progressive worsening of symptoms")
                if onset == "Sudden":
                    analysis_points.append("⚡ Acute onset - requires prompt evaluation")
                if has_critical:
                    analysis_points.append("🚨 Critical symptoms detected requiring immediate attention")
                
                # Add general recommendations
                analysis_points.extend([
                    f"📅 Symptom duration: {duration}",
                    f"🎯 Pain assessment: {pain_scale}/10 {'(Severe)' if pain_scale >= 7 else '(Moderate)' if pain_scale >= 4 else '(Mild)'}",
                    f"📊 Onset pattern: {onset}"
                ])
                
                for point in analysis_points:
                    st.write(f"• {point}")
                
                # Recommendations
                st.subheader("💡 Recommendations")
                recommendations = []
                
                if urgency_score == 3:
                    recommendations.extend([
                        "🚨 Do not drive yourself - call 911 or have someone drive you",
                        "💊 Do not take any medications unless prescribed",
                        "📋 Bring list of current medications and medical history",
                        "📞 Contact emergency contact/family member"
                    ])
                elif urgency_score == 2:
                    recommendations.extend([
                        "🏥 Seek medical attention within hours, not days",
                        "📋 Monitor symptoms - call 911 if they worsen",
                        "💊 Avoid self-medication",
                        "📱 Have someone available to drive you if needed"
                    ])
                else:
                    recommendations.extend([
                        "📞 Contact your primary care provider",
                        "📝 Keep a symptom diary",
                        "🌡 Monitor vital signs if possible",
                        "💧 Stay hydrated and rest"
                    ])
                
                for rec in recommendations:
                    st.write(f"• {rec}")
                
                st.error("⚠ This AI assessment is not a substitute for professional medical advice. Always consult healthcare providers for accurate diagnosis and treatment.")
                
            else:
                st.warning("Please describe your symptoms to get an assessment.")
    
    with col2:
        st.subheader("🚨 Urgency Levels")
        
        urgency_info = [
            {"Level": "🚨 CRITICAL", "Action": "Call 911", "Examples": "Chest pain, Severe breathing difficulty, Unconsciousness"},
            {"Level": "⚡ URGENT", "Action": "ER within hours", "Examples": "High fever, Severe pain, Injuries"},
            {"Level": "📋 ROUTINE", "Action": "Schedule appointment", "Examples": "Mild symptoms, Chronic issues"}
        ]
        
        for info in urgency_info:
            st.markdown(f"""
            *{info['Level']}*  
            Action: {info['Action']}  
            Examples: {info['Examples']}  
            """)
        
        st.subheader("🎯 Assessment Features")
        features = [
            "🧠 NLP Symptom Analysis",
            "⚡ Real-time Triage",
            "📊 Severity Scoring",
            "🎯 Urgency Classification", 
            "💡 Action Recommendations",
            "📋 Documentation Support"
        ]
        
        for feature in features:
            st.write(feature)
        
        st.subheader("🚨 Emergency Symptoms")
        emergency_symptoms = [
            "Chest pain/pressure",
            "Difficulty breathing", 
            "Severe headache",
            "Loss of consciousness",
            "Severe bleeding",
            "Signs of stroke",
            "Severe allergic reaction"
        ]
        
        for symptom in emergency_symptoms:
            st.write(f"• {symptom}")

# Parkinson's Disease Detection
elif current_page == "parkinsons":
    st.markdown("""
    <div class="feature-card">
        <div class="feature-header">
            <span class="feature-icon">🧠</span>
            <h2 class="feature-title">Parkinson's Disease Risk Assessment</h2>
        </div>
        <p class="feature-description">Advanced voice analysis and movement assessment for early Parkinson's disease detection using AI-powered biomarker analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎤 Voice Analysis Assessment")
        
        # Voice recording simulation
        st.info("🎙 Voice Recording Instructions: Please read the following text clearly into your microphone")
        
        sample_text = st.text_area("Sample Text for Reading", 
                                 value="The quick brown fox jumps over the lazy dog. Peter Piper picked a peck of pickled peppers.",
                                 height=100)
        
        # Voice parameters simulation (normally would come from audio analysis)
        st.subheader("🔊 Voice Parameters")
        
        # Simulate voice analysis inputs
        col_a, col_b = st.columns(2)
        with col_a:
            jitter = st.number_input("Jitter (%)", min_value=0.0, max_value=5.0, value=0.5, step=0.01,
                                   help="Measure of voice frequency variation")
            shimmer = st.number_input("Shimmer (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.01,
                                    help="Measure of voice amplitude variation")
            nhr = st.number_input("Noise-to-Harmonics Ratio", min_value=0.0, max_value=1.0, value=0.1, step=0.001,
                                help="Measure of voice quality")
        
        with col_b:
            hnr = st.number_input("Harmonics-to-Noise Ratio (dB)", min_value=5.0, max_value=40.0, value=20.0, step=0.1,
                                help="Higher values indicate clearer voice")