import streamlit as st
import requests
import time
from datetime import datetime, timedelta
import json

st.set_page_config(
    page_title="Quantum Eavesdropping Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI/UX
st.markdown("""
<style>
    :root {
        --primary-color: #00d4ff;
        --success-color: #00ff88;
        --danger-color: #ff3366;
        --warning-color: #ffaa00;
        --dark-bg: #0a0e27;
        --card-bg: #1a1f3a;
        --text-primary: #ffffff;
        --text-secondary: #a0aec0;
    }

    body {
        background-color: var(--dark-bg);
        color: var(--text-primary);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(0, 212, 255, 0.2);
    }

    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5em;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        margin: 10px 0 0 0;
        font-size: 1em;
    }

    .metric-card {
        background: linear-gradient(135deg, var(--card-bg) 0%, #252d4a 100%);
        padding: 25px;
        border-radius: 12px;
        border-left: 4px solid var(--primary-color);
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 20px;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2);
    }

    .metric-label {
        color: var(--text-secondary);
        font-size: 0.9em;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    .metric-value {
        color: var(--primary-color);
        font-size: 2.2em;
        font-weight: 700;
        font-family: 'Monaco', monospace;
    }

    .status-secure {
        background: linear-gradient(135deg, #0f5132 0%, #1a7e4a 100%);
        padding: 25px;
        border-radius: 12px;
        border: 2px solid #00ff88;
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.2);
        text-align: center;
        margin: 20px 0;
    }

    .status-secure h2 {
        color: #00ff88;
        margin: 0;
        font-size: 1.8em;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }

    .status-attack {
        background: linear-gradient(135deg, #842029 0%, #d63031 100%);
        padding: 25px;
        border-radius: 12px;
        border: 2px solid var(--danger-color);
        box-shadow: 0 0 30px rgba(255, 51, 102, 0.3);
        text-align: center;
        margin: 20px 0;
        animation: pulse-danger 2s infinite;
    }

    .status-attack h2 {
        color: var(--danger-color);
        margin: 0;
        font-size: 1.8em;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }

    @keyframes pulse-danger {
        0%, 100% { box-shadow: 0 0 30px rgba(255, 51, 102, 0.3); }
        50% { box-shadow: 0 0 50px rgba(255, 51, 102, 0.6); }
    }

    .info-section {
        background: var(--card-bg);
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 4px solid var(--warning-color);
    }

    .info-section h3 {
        color: var(--warning-color);
        margin: 0 0 10px 0;
        font-size: 1.1em;
    }

    .info-section p {
        color: var(--text-secondary);
        margin: 5px 0;
        line-height: 1.6;
    }

    .risk-meter {
        width: 100%;
        height: 8px;
        background: #2a3a5a;
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
    }

    .risk-fill {
        height: 100%;
        background: linear-gradient(90deg, #00ff88 0%, #ffaa00 50%, #ff3366 100%);
        border-radius: 10px;
        transition: width 0.5s ease;
    }

    .sidebar-section {
        background: var(--card-bg);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 3px solid var(--primary-color);
    }

    .control-group {
        background: var(--card-bg);
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
    }

    .timestamp {
        color: var(--text-secondary);
        font-size: 0.85em;
        margin-top: 10px;
    }

    .metric-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for history
if 'history' not in st.session_state:
    st.session_state.history = []
if 'attack_mode' not in st.session_state:
    st.session_state.attack_mode = False

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    with st.container():
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.session_state.attack_mode = st.toggle(
            "🎯 Simulate Eavesdropping Attack",
            value=st.session_state.attack_mode,
            help="Enable this to test detection with an active eavesdropping simulation"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("📊 History", use_container_width=True):
            st.session_state.show_history = not st.session_state.get('show_history', False)

    st.markdown("---")
    st.markdown("### 📖 About")
    st.markdown("""
    **Quantum Eavesdropping Detector** uses quantum key distribution (BB84) protocol analysis to detect potential eavesdropping attempts.
    
    **Key Features:**
    - Real-time QBER monitoring
    - Anomaly detection via ML
    - Entropy analysis
    - Secure channel verification
    """)

    st.markdown("---")
    st.markdown("### 💡 How to Use")
    st.markdown("""
    1. Use the toggle to simulate eavesdropping
    2. Click "Refresh Data" for new analysis
    3. Monitor real-time metrics
    4. Review status indicators
    5. Check detailed metrics below
    """)

# Main content
st.markdown("""
<div class="main-header">
    <h1>🛡️ Quantum Eavesdropping Detector</h1>
    <p>Real-time BB84 Protocol Security Analysis & Threat Detection</p>
</div>
""", unsafe_allow_html=True)

# Fetch data from API
try:
    response = requests.get(
        "http://localhost:8000/detect",
        params={"attack": st.session_state.attack_mode},
        timeout=10
    )
    data = response.json()
    
    # Store in history
    st.session_state.history.append({
        'timestamp': datetime.now(),
        'data': data,
        'attack_mode': st.session_state.attack_mode
    })
    # Keep only last 50 records
    if len(st.session_state.history) > 50:
        st.session_state.history = st.session_state.history[-50:]
    
except Exception as e:
    st.error(f"❌ Connection Error: {str(e)}")
    st.info("Make sure the backend server is running on http://localhost:8000")
    st.stop()

# Status indicator
col_status = st.container()
with col_status:
    if data["Eavesdropping"]:
        st.markdown("""
        <div class="status-attack">
            <h2>🚨 EAVESDROPPING DETECTED</h2>
        </div>
        """, unsafe_allow_html=True)
        st.warning("⚠️ **Alert**: Potential quantum eavesdropping detected on the channel. Investigate immediately.")
    else:
        st.markdown("""
        <div class="status-secure">
            <h2>✅ CHANNEL SECURE</h2>
        </div>
        """, unsafe_allow_html=True)
        st.success("✓ No eavesdropping detected. Channel integrity verified.")

# Main metrics
st.markdown("### 📊 Real-time Metrics")

metric_cols = st.columns(3)
with metric_cols[0]:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Quantum Bit Error Rate (QBER)</div>', unsafe_allow_html=True)
    qber_value = round(data["QBER"], 4)
    st.markdown(f'<div class="metric-value">{qber_value}</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color: #a0aec0; margin-top: 8px; font-size: 0.9em;">
    Lower values indicate better channel security. Threshold: 0.11
    </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with metric_cols[1]:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Shannon Entropy</div>', unsafe_allow_html=True)
    entropy_value = round(data["Entropy"], 4)
    st.markdown(f'<div class="metric-value">{entropy_value}</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color: #a0aec0; margin-top: 8px; font-size: 0.9em;">
    Measures randomness/unpredictability. Higher = more secure
    </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with metric_cols[2]:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Anomaly Score</div>', unsafe_allow_html=True)
    anomaly_value = round(data["AnomalyScore"], 6)
    st.markdown(f'<div class="metric-value">{anomaly_value}</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color: #a0aec0; margin-top: 8px; font-size: 0.9em;">
    ML-based detection. Lower = normal, Higher = suspicious
    </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Risk visualization
st.markdown("### 🎯 Security Risk Assessment")
risk_level = min(100, int(data["AnomalyScore"] * 1000))
risk_percentage = risk_level
st.markdown(f"""
<div style="background: var(--card-bg); padding: 20px; border-radius: 10px; border-left: 4px solid var(--primary-color);">
    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
        <span style="color: var(--text-secondary);">Risk Level</span>
        <span style="color: #00d4ff; font-weight: bold;">{risk_percentage}%</span>
    </div>
    <div class="risk-meter">
        <div class="risk-fill" style="width: {risk_percentage}%"></div>
    </div>
    <p style="color: var(--text-secondary); margin-top: 10px; font-size: 0.9em;">
    Based on anomaly detection model trained on BB84 protocol patterns
    </p>
</div>
""", unsafe_allow_html=True)

# Detailed analysis section
st.markdown("### 📈 Detailed Analysis")
with st.expander("🔍 Channel Statistics & Interpretation", expanded=True):
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("""
        **🔹 QBER (Quantum Bit Error Rate)**
        - **Value**: """ + str(qber_value) + """
        - **Ideal Range**: 0.00 - 0.11
        - **Status**: """ + ("⚠️ **High** (Possible eavesdropping)" if qber_value > 0.11 else "✅ **Normal**") + """
        
        QBER measures the error rate in quantum bit transmission. A sudden increase indicates potential eavesdropping attempts.
        """)
        
        st.markdown("""
        **🔹 Anomaly Score**
        - **Value**: """ + str(anomaly_value) + """
        - **Model**: Neural Network Autoencoder
        - **Threshold**: 0.5
        - **Status**: """ + ("🚨 **Anomalous**" if anomaly_value > 0.5 else "✅ **Normal**") + """
        
        Machine learning model detects patterns that deviate from normal BB84 operation.
        """)
    
    with col_right:
        st.markdown("""
        **🔹 Shannon Entropy**
        - **Value**: """ + str(entropy_value) + """
        - **Ideal Range**: High (closer to 1.0)
        - **Status**: """ + ("✅ **High Randomness**" if entropy_value > 0.8 else "⚠️ **Check Randomness**") + """
        
        Entropy quantifies the randomness of the quantum key distribution. Higher entropy indicates secure, unpredictable key generation.
        """)
        
        st.markdown("""
        **🔹 Eavesdropping Detection**
        - **Current Status**: """ + ("🚨 **ATTACK DETECTED**" if data["Eavesdropping"] else "✅ **SECURE**") + """
        - **Algorithm**: Combined QBER + Anomaly Detection
        - **Confidence**: Based on multiple factors
        
        Final verdict combining classical and ML-based detection methods.
        """)

# History section
if st.session_state.get('show_history', False) and len(st.session_state.history) > 1:
    st.markdown("### 📜 Detection History")
    st.info(f"Showing last {len(st.session_state.history)} readings")
    
    history_data = []
    for record in st.session_state.history[-10:]:
        history_data.append({
            'Time': record['timestamp'].strftime('%H:%M:%S'),
            'QBER': round(record['data']['QBER'], 4),
            'Entropy': round(record['data']['Entropy'], 4),
            'Anomaly': round(record['data']['AnomalyScore'], 6),
            'Attack Mode': '🎯 ON' if record['attack_mode'] else '✅ OFF',
            'Detected': '🚨 YES' if record['data']['Eavesdropping'] else '✅ NO'
        })
    
    st.dataframe(history_data, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #a0aec0; font-size: 0.9em; margin-top: 20px;">
    <p>🔬 Quantum Eavesdropping Detector | Powered by BB84 Protocol Analysis & Machine Learning</p>
    <p>Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
</div>
""", unsafe_allow_html=True)
