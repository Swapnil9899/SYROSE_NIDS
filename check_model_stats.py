"""Check model training statistics."""
import pandas as pd
import os
import joblib
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

# Check training data
data_path = 'data/synthetic_unsw_nb15.csv'
print("=" * 80)
print("QUILLBOT NIDS - MODEL STATISTICS")
print("=" * 80)

if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    print(f"\n✅ Training data exists: {data_path}")
    print(f"   Total samples: {len(df):,}")
    print(f"\n📊 Label Distribution:")
    print(df['Label'].value_counts())
    print(f"\n📊 Attack Category Distribution:")
    print(df['attack_cat'].value_counts())
    
    # Calculate percentages
    normal_pct = (df['Label'] == 0).sum() / len(df) * 100
    attack_pct = (df['Label'] == 1).sum() / len(df) * 100
    print(f"\n   Normal: {normal_pct:.1f}%")
    print(f"   Attack: {attack_pct:.1f}%")
else:
    print(f"\n❌ Training data not found: {data_path}")

# Check model
model_path = 'model/nids_model.pkl'
if os.path.exists(model_path):
    model = joblib.load(model_path)
    print(f"\n✅ Model exists: {model_path}")
    print(f"   Model type: {type(model).__name__}")
    print(f"   Number of estimators: {model.n_estimators}")
    print(f"   Number of features: {model.n_features_in_}")
else:
    print(f"\n❌ Model not found: {model_path}")

print("\n" + "=" * 80)

