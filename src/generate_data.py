import pandas as pd
import numpy as np

# Synthetic CPT dataset generator for demonstration purposes
# Generates multiple CPT profiles with random noise

N_PROFILES = 50
DEPTH_MAX = 25.0
DEPTH_STEP = 0.5


def generate_single_profile(profile_id: int):
    depth = np.arange(0, DEPTH_MAX + DEPTH_STEP, DEPTH_STEP)
    qc = 0.5 + 0.1 * depth + np.random.normal(0, 0.05, size=depth.shape)
    fs = 0.05 * qc + np.random.normal(0, 0.005, size=depth.shape)
    u = 0.02 * qc + np.random.normal(0, 0.002, size=depth.shape)

    soil_type = []
    for q in qc:
        if q < 2:
            soil_type.append('soft_clay')
        elif q < 5:
            soil_type.append('silt')
        else:
            soil_type.append('sand')

    df = pd.DataFrame({
        'profile_id': profile_id,
        'depth_m': depth,
        'qc_MPa': qc,
        'fs_kPa': fs,
        'u_kPa': u,
        'soil_type': soil_type
    })
    return df


def generate_dataset(n_profiles=N_PROFILES):
    profiles = [generate_single_profile(i) for i in range(n_profiles)]
    return pd.concat(profiles, ignore_index=True)


if __name__ == '__main__':
    df = generate_dataset()
    df.to_csv('data/raw/generated_cpt_data.csv', index=False)
    print('Generated dataset saved to data/raw/generated_cpt_data.csv')
