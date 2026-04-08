"""Check model metadata."""
import joblib

metadata = joblib.load('model/model_metadata.pkl')
print('Model Metadata:')
for key, value in metadata.items():
    print(f'  {key}: {value}')

