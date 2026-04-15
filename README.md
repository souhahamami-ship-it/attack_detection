# 🛡️ Real-Time Intrusion Detection System (IDS)

## 📌 Overview

This project is a **Machine Learning-based Intrusion Detection System (IDS)** designed to detect and classify cyber attacks in real-time.

It leverages the **NSL-KDD dataset** and an **XGBoost model** to identify multiple types of network attacks and visualize them through an interactive dashboard.

---

## 🚀 Features

* 🔍 Multi-class attack detection (DoS, Probe, R2L, U2R)
* ⚡ Real-time simulation of network traffic
* 🧠 Machine Learning model (XGBoost)
* 📊 Interactive SOC-style dashboard (Streamlit)
* 🚨 Alert system (visual + sound)
* 📈 Live attack statistics and logs
* 🔄 Start/Stop real-time monitoring

---

## 🧠 Attack Categories

The system classifies traffic into:

* **Normal**
* **DoS (Denial of Service)**
* **Probe**
* **R2L (Remote to Local)**
* **U2R (User to Root)**
* **Other**

---

## 🏗️ Project Structure

```bash
attack_detection/
│── app/
│   ├── dashboard.py       # SOC dashboard (Streamlit)
│   ├── simulator.py       # Real-time traffic simulator
│   ├── api.py             # (Optional) API interface
│   ├── ui.py              # (Optional) basic UI
│
│── src/
│   ├── preprocessing.py   # Data processing pipeline
│   ├── config.py          # Feature selection & settings
│
│── artifacts/
│   ├── xgb_model.pkl
│   ├── scaler.pkl
│   ├── label_encoders.pkl
│   ├── attack_label_encoder.pkl
│
│── data/
│   └── raw/
│       └── KDDTrain+_20Percent.txt
│
│── train.py
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/souhahamami-ship-it/attack_detection.git
cd attack_detection
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### 🔹 Train the model

```bash
python train.py
```

### 🔹 Run simulator (terminal)

```bash
python app/simulator.py
```

### 🔹 Launch dashboard

```bash
python -m streamlit run app/dashboard.py
```

---

## 📊 Dashboard Features

* Real-time attack monitoring
* Attack type distribution chart
* Live logs (last 50 events)
* Start / Stop control
* Alert system (🚨 + sound)

---

## 🧪 Dataset

* **NSL-KDD Dataset**
* File used: `KDDTrain+_20Percent.txt`

---

## 🤖 Model

* Algorithm: **XGBoost Classifier**
* Multi-class classification
* Preprocessing:

  * Label Encoding
  * Feature Scaling (StandardScaler)

---

## 🚨 Alert System

* Visual alert for detected attacks
* Sound notification in browser
* Highlights attack type in real-time

---

## 👩‍💻 Author

**Souha Hammami**
🔗 https://github.com/souhahamami-ship-it

---

