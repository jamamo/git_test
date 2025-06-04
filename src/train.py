import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
import argparse

PROCESSED_CSV = 'data/processed/cpt_features.csv'
MODEL_PATH = 'model_outputs/rf_model.pkl'


def load_features(csv_path=PROCESSED_CSV):
    return pd.read_csv(csv_path)


def train_model(df: pd.DataFrame, model_path: str):
    X = df.drop(columns=['soil_type', 'profile_id'])
    y = df['soil_type']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))

    pd.to_pickle(clf, model_path)
    print(f'Model saved to {model_path}')


def main(args):
    df = load_features(args.features)
    train_model(df, args.model_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train soil type classifier')
    parser.add_argument('--features', default=PROCESSED_CSV)
    parser.add_argument('--model_path', default=MODEL_PATH)
    args = parser.parse_args()
    main(args)
