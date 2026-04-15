# 🚨 Attack Detection System

## 📌 Overview

This project is a **Machine Learning-based Attack Detection System** designed to identify malicious activities in data.

It uses a trained **XGBoost model** along with preprocessing pipelines to classify whether an input represents an attack or normal behavior.

---

## 🧠 Features

* Pretrained ML model (XGBoost)
* Data preprocessing pipeline
* API for predictions
* Simple user interface
* Ready-to-use saved models

---

## 🗂️ Project Structure

```bash
attack_detection/
│── app/
│   ├── api.py              # API for model inference
│   ├── ui.py               # User interface
│
│── artifacts/
│   ├── xgb_model.pkl       # Trained XGBoost model
│   ├── scaler.pkl          # Feature scaler
│   ├── label_encoders.pkl  # Encoders for categorical data
│   ├── attack_label_encoder.pkl # Target encoder
│
│── src/
│   ├── config.py           # Configuration settings
│   ├── preprocessing.py    # Data preprocessing logic
│
│── train.py                # Model training script
│── requirements.txt        # Dependencies
│── README.md               # Project documentation
│── .gitignore.txt
```

---

## ⚙️ Installation

### 1. Clone the repository

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

### 🔹 Run the API

```bash
python app/api.py
```

### 🔹 Run the UI

```bash
python app/ui.py
```

### 🔹 Train the model (optional)

```bash
python train.py
```

---

## 🔍 How It Works

1. Input data is collected
2. Data is preprocessed using:

   * Scaling
   * Encoding
3. The trained **XGBoost model** predicts the result
4. Output is classified as:

   * Normal
   * Attack

---

## 🤖 Model Details

* Algorithm: **XGBoost**
* Saved as: `artifacts/xgb_model.pkl`
* Preprocessing:

  * Standard Scaler
  * Label Encoders

---

## 📊 Output

The system returns:

* Predicted class (Attack / Normal)
* Encoded label

---

## 🚀 Future Improvements

* Add real-time network monitoring
* Deploy API using Flask/FastAPI
* Improve UI design
* Add more advanced models (Deep Learning)

