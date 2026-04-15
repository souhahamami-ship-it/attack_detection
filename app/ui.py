import streamlit as st
import requests
import joblib

st.title("🛡️ Network Anomaly Detection")

st.sidebar.header("Input Features")

# Load encoders
label_encoders = joblib.load("artifacts/label_encoders.pkl")

# ---------- CATEGORICAL FEATURES ----------

# protocol_type
protocol_options = list(label_encoders["protocol_type"].classes_)
protocol_type = st.sidebar.selectbox("protocol_type", protocol_options)
protocol_type_encoded = label_encoders["protocol_type"].transform([protocol_type])[0]

# service
service_options = list(label_encoders["service"].classes_)
service = st.sidebar.selectbox("service", service_options)
service_encoded = label_encoders["service"].transform([service])[0]

# flag
flag_options = list(label_encoders["flag"].classes_)
flag = st.sidebar.selectbox("flag", flag_options)
flag_encoded = label_encoders["flag"].transform([flag])[0]


# ---------- NUMERIC FEATURES ----------

inputs = {}

inputs["duration"] = st.sidebar.number_input("duration", value=0)
inputs["protocol_type"] = protocol_type_encoded
inputs["service"] = service_encoded
inputs["flag"] = flag_encoded
inputs["src_bytes"] = st.sidebar.number_input("src_bytes", value=0)
inputs["dst_bytes"] = st.sidebar.number_input("dst_bytes", value=0)
inputs["logged_in"] = st.sidebar.selectbox("logged_in", [0, 1])
inputs["num_failed_logins"] = st.sidebar.number_input("num_failed_logins", value=0)
inputs["count"] = st.sidebar.number_input("count", value=0)
inputs["srv_count"] = st.sidebar.number_input("srv_count", value=0)
inputs["serror_rate"] = st.sidebar.slider("serror_rate", 0.0, 1.0, 0.0)
inputs["rerror_rate"] = st.sidebar.slider("rerror_rate", 0.0, 1.0, 0.0)
inputs["num_compromised"] = st.sidebar.number_input("num_compromised", value=0)
inputs["num_root"] = st.sidebar.number_input("num_root", value=0)
inputs["num_file_creations"] = st.sidebar.number_input("num_file_creations", value=0)
inputs["num_shells"] = st.sidebar.number_input("num_shells", value=0)
inputs["num_access_files"] = st.sidebar.number_input("num_access_files", value=0)
inputs["hot"] = st.sidebar.number_input("hot", value=0)


# ---------- PREDICTION ----------

if st.button("🔍 Predict"):
    with st.spinner("Predicting..."):
        res = requests.post("http://127.0.0.1:8000/predict", json=inputs)
        prediction = res.json()["prediction"]

        colors = {
            "Normal": "🟢",
            "DoS": "🔴",
            "Probe": "🟡",
            "R2L": "🟠",
            "U2R": "🔴"
        }

        st.markdown(f"## {colors.get(prediction, '⚪')} Prediction: `{prediction}`")