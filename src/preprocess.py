import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import os
import re
from docx import Document

RAW_CSV = 'data/raw/generated_cpt_data.csv'
SUMMER_DIR = r'C:\\Users\\ismai\\OneDrive - The University of Manchester\\Desktop\\Summer'
EXCEL_PATH = os.path.join(SUMMER_DIR, 'excel.xlsx')
DOCX_PATH = os.path.join(SUMMER_DIR, 'report.docx')
PROCESSED_CSV = 'data/processed/cpt_features.csv'


def parse_report(doc_path: str):
    """Extract simple coefficients from the report document."""
    coeffs = {'qc_a': 0.5, 'qc_b': 0.1, 'fs_ratio': 0.05, 'u_ratio': 0.02}
    try:
        doc = Document(doc_path)
        text = "\n".join(p.text for p in doc.paragraphs)
        qc_match = re.search(r"qc\s*=\s*([0-9.]+)\s*\+\s*([0-9.]+)\s*\*\s*depth", text, re.IGNORECASE)
        if qc_match:
            coeffs['qc_a'] = float(qc_match.group(1))
            coeffs['qc_b'] = float(qc_match.group(2))
        fs_match = re.search(r"fs\s*=\s*([0-9.]+)\s*\*\s*qc", text, re.IGNORECASE)
        if fs_match:
            coeffs['fs_ratio'] = float(fs_match.group(1))
        u_match = re.search(r"u\s*=\s*([0-9.]+)\s*\*\s*qc", text, re.IGNORECASE)
        if u_match:
            coeffs['u_ratio'] = float(u_match.group(1))
    except Exception:
        # Fall back to defaults if parsing fails
        pass
    return coeffs


def generate_large_dataset(excel_path: str, coeffs: dict, step: float = 0.01) -> pd.DataFrame:
    """Create a larger dataset with small depth increments using formulas."""
    base = pd.read_excel(excel_path)
    depth_max = float(base['depth_m'].max())
    depth = []
    qc = []
    fs = []
    u = []
    d = 0.0
    while d <= depth_max:
        q = coeffs['qc_a'] + coeffs['qc_b'] * d
        f = coeffs['fs_ratio'] * q
        up = coeffs['u_ratio'] * q
        depth.append(d)
        qc.append(q)
        fs.append(f)
        u.append(up)
        d += step
    df = pd.DataFrame({'profile_id': 0,
                       'depth_m': depth,
                       'qc_MPa': qc,
                       'fs_kPa': fs,
                       'u_kPa': u,
                       'soil_type': 'unknown'})
    return df


def load_data(csv_path=RAW_CSV):
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    coeffs = parse_report(DOCX_PATH)
    df = generate_large_dataset(EXCEL_PATH, coeffs)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path, index=False)
    return df


def engineer_profile(df_profile: pd.DataFrame) -> pd.Series:
    df_profile = df_profile.copy()
    df_profile['Rf'] = df_profile['fs_kPa'] / (df_profile['qc_MPa'] * 1000) * 100
    df_profile['qc_norm'] = (df_profile['qc_MPa'] - df_profile['qc_MPa'].mean()) / df_profile['qc_MPa'].std()

    df_profile['depth_window'] = (df_profile['depth_m'] // 2).astype(int)
    stats = df_profile.groupby('depth_window').agg({
        'qc_MPa': ['mean', 'min', 'max', 'std'],
        'fs_kPa': ['mean', 'min', 'max', 'std'],
        'u_kPa': ['mean', 'min', 'max', 'std'],
    })
    stats.columns = ['_'.join(col) for col in stats.columns]
    stats = stats.reset_index(drop=True)
    stats = stats.fillna(0)

    feature_vector = stats.values.flatten()
    columns = [f'{col}_w{idx}' for idx in range(stats.shape[0]) for col in stats.columns]

    global_feats = df_profile[['qc_MPa', 'fs_kPa', 'u_kPa', 'Rf', 'qc_norm']].agg(['mean', 'std', 'min', 'max']).unstack().T
    global_feats.columns = ['_'.join(col) for col in global_feats.columns]
    global_feats = global_feats.iloc[0]

    feature_series = pd.Series(feature_vector, index=columns)
    feature_series = pd.concat([feature_series, global_feats])
    feature_series['soil_type'] = df_profile['soil_type'].mode()[0]
    feature_series['profile_id'] = df_profile['profile_id'].iloc[0]

    return feature_series


def preprocess(csv_path=RAW_CSV, out_path=PROCESSED_CSV):
    df = load_data(csv_path)
    profiles = []
    for pid, group in df.groupby('profile_id'):
        profiles.append(engineer_profile(group))

    feature_df = pd.DataFrame(profiles)

    scaler = StandardScaler()
    scaled_cols = feature_df.drop(columns=['soil_type', 'profile_id'])
    scaled = scaler.fit_transform(scaled_cols)
    scaled_df = pd.DataFrame(scaled, columns=scaled_cols.columns)
    scaled_df['soil_type'] = feature_df['soil_type'].values
    scaled_df['profile_id'] = feature_df['profile_id'].values

    scaled_df.to_csv(out_path, index=False)
    print(f'Processed features saved to {out_path}')


if __name__ == '__main__':
    preprocess()
