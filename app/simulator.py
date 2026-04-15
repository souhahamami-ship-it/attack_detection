
# app/simulator.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import time
import joblib
import random
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
def load_data():
    df = pd.read_csv(DATA_PATH, header=None)
    df.columns = columns
    return df


# ======================
# SIMULATION
# ======================
def simulate_stream(df, delay=1):
    print("🚀 Starting real-time simulation...\n")

    step = 0
    attack_count = 0
    normal_count = 0

    try:
        while True:
            step += 1

            row = df.sample(1)

            # ✅ preprocessing already includes scaling
            X_scaled, y = preprocess(row, training=False)

            prediction = model.predict(X_scaled)[0]

            # ✅ decode classes
            pred_class = attack_le.inverse_transform([prediction])[0]
            real_class = attack_le.inverse_transform([y.values[0]])[0]

            # ✅ logic based on class
            if pred_class != "Normal":
                attack_count += 1
                status = f"🚨 {pred_class}"
            else:
                normal_count += 1
                status = "✅ Normal"

            # ✅ fake attacker IP (for realism)
            fake_ip = f"192.168.1.{random.randint(1,255)}"

            # ======================
            # OUTPUT
            # ======================
            print(f"[{step}] {status}")
            print(f"🌐 Source IP: {fake_ip}")
            print(f"🔎 Real: {real_class} | Predicted: {pred_class}")
            print(f"📊 Stats → Attacks: {attack_count} | Normal: {normal_count}")
            print("-" * 60)

            time.sleep(delay)

    except KeyboardInterrupt:
        print("\n🛑 Simulation stopped by user")
        print(f"📊 Final Stats → Attacks: {attack_count}, Normal: {normal_count}")


# ======================
# RUN
# ======================
if __name__ == "__main__":
    df = load_data()
    simulate_stream(df, delay=1)

