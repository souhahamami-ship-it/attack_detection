
# app/dashboard.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import time
import joblib

from src.preprocessing import preprocess

# ======================
# LOAD ARTIFACTS
# ======================
model = joblib.load("artifacts/xgb_model.pkl")
attack_le = joblib.load("artifacts/attack_label_encoder.pkl")

# ======================
# DATA PATH
# ======================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "KDDTrain+_20Percent.txt")

columns = [
    'duration','protocol_type','service','flag','src_bytes','dst_bytes',
    'land','wrong_fragment','urgent','hot','num_failed_logins','logged_in',
    'num_compromised','root_shell','su_attempted','num_root','num_file_creations',
    'num_shells','num_access_files','num_outbound_cmds','is_host_login',
    'is_guest_login','count','srv_count','serror_rate','srv_serror_rate',
    'rerror_rate','srv_rerror_rate','same_srv_rate','diff_srv_rate',
    'srv_diff_host_rate','dst_host_count','dst_host_srv_count',
    'dst_host_same_srv_rate','dst_host_diff_srv_rate',
    'dst_host_same_src_port_rate','dst_host_srv_diff_host_rate',
    'dst_host_serror_rate','dst_host_srv_serror_rate',
    'dst_host_rerror_rate','dst_host_srv_rerror_rate','label','difficulty'
]

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, header=None)
    df.columns = columns
    return df

df = load_data()

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(page_title="SOC Dashboard", layout="wide")

st.title("🛡️ SOC - Real-Time Intrusion Detection")

# ======================
# SESSION STATE INIT
# ======================
if "attack_count" not in st.session_state:
    st.session_state.attack_count = 0
    st.session_state.normal_count = 0
    st.session_state.total = 0
    st.session_state.logs = []
    st.session_state.attack_stats = {}
    st.session_state.running = False

# ======================
# CONTROL BUTTONS
# ======================
col1, col2 = st.columns(2)

if col1.button("▶ Start"):
    st.session_state.running = True

if col2.button("⏹ Stop"):
    st.session_state.running = False

# ======================
# STATUS INDICATOR
# ======================
if st.session_state.running:
    st.success("🟢 System Running")
else:
    st.error("🔴 System Stopped")

# ======================
# MAIN PROCESS (STEP)
# ======================
if st.session_state.running:

    row = df.sample(1)

    X_scaled, y = preprocess(row, training=False)
    prediction = model.predict(X_scaled)[0]

    pred_class = attack_le.inverse_transform([prediction])[0]

    st.session_state.total += 1

    if pred_class != "Normal":
        st.session_state.attack_count += 1
        status = f"🚨 {pred_class}"
    else:
        st.session_state.normal_count += 1
        status = "✅ Normal"

    # Update stats
    if pred_class not in st.session_state.attack_stats:
        st.session_state.attack_stats[pred_class] = 0

    st.session_state.attack_stats[pred_class] += 1

    # Logs
    st.session_state.logs.append({
        "Step": st.session_state.total,
        "Prediction": pred_class,
        "Status": status
    })

    st.session_state.logs = st.session_state.logs[-50:]

# ======================
# DASHBOARD DISPLAY
# ======================
col1, col2, col3 = st.columns(3)

col1.metric("🚨 Attacks", st.session_state.attack_count)
col2.metric("✅ Normal", st.session_state.normal_count)
col3.metric("📊 Total", st.session_state.total)

# Chart
st.subheader("📊 Attack Distribution")
if st.session_state.attack_stats:
    st.bar_chart(pd.DataFrame.from_dict(st.session_state.attack_stats, orient="index"))

# Logs
st.subheader("📜 Live Logs")
st.dataframe(pd.DataFrame(st.session_state.logs))

# ======================
# AUTO REFRESH
# ======================
if st.session_state.running:
    time.sleep(0.3)
    st.rerun()

