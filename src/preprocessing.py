import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from src.config import SELECTED_FEATURES, CATEGORICAL_COLUMNS

# Attack mapping
dos_attacks = [...]
probe_attacks = [...]
r2l_attacks = [...]
u2r_attacks = [...]

def map_attack_type(label):
    if label == 'normal':
        return 'Normal'
    elif label in dos_attacks:
        return 'DoS'
    elif label in probe_attacks:
        return 'Probe'
    elif label in r2l_attacks:
        return 'R2L'
    elif label in u2r_attacks:
        return 'U2R'
    return 'Other'


def clean_data(df):
    drop_cols = [
        'land','is_guest_login','is_host_login','su_attempted',
        'root_shell','num_outbound_cmds','urgent','wrong_fragment','difficulty'
    ]
    df = df.drop(columns=drop_cols, errors='ignore')
    df = df.drop_duplicates().dropna()
    return df


def encode_features(df, training=True):
    if training:
        label_encoders = {}
        for col in CATEGORICAL_COLUMNS:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            label_encoders[col] = le
        joblib.dump(label_encoders, "artifacts/label_encoders.pkl")
    else:
        label_encoders = joblib.load("artifacts/label_encoders.pkl")
        for col in CATEGORICAL_COLUMNS:
            le = label_encoders[col]
            df[col] = df[col].astype(str).apply(
                lambda x: x if x in le.classes_ else 'unknown'
            )
            if 'unknown' not in le.classes_:
                le.classes_ = np.append(le.classes_, 'unknown')
            df[col] = le.transform(df[col])

    return df


def encode_target(df, training=True):
    df['attack_type'] = df['label'].apply(map_attack_type)

    if training:
        attack_le = LabelEncoder()
        attack_le.fit(['DoS','Normal','Other','Probe','R2L','U2R'])
        joblib.dump(attack_le, "artifacts/attack_label_encoder.pkl")
    else:
        attack_le = joblib.load("artifacts/attack_label_encoder.pkl")

    df['attack_type_encoded'] = attack_le.transform(df['attack_type'])
    return df


def scale_features(X, training=True):
    if training:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        joblib.dump(scaler, "artifacts/scaler.pkl")
    else:
        scaler = joblib.load("artifacts/scaler.pkl")
        X_scaled = scaler.transform(X)

    return X_scaled


def preprocess(df, training=True):
    df = clean_data(df)
    df = encode_features(df, training)
    df = encode_target(df, training)

    X = df[SELECTED_FEATURES]
    y = df['attack_type_encoded']

    X_scaled = scale_features(X, training)

    return X_scaled, y