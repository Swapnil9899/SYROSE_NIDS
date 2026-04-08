"""
Generate comprehensive evaluation metrics and visualizations for QUILLBOT NIDS documentation.
This script creates all necessary graphs, tables, and metrics for the documentation.
"""
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix, classification_report, roc_curve, auc,
    precision_recall_curve, average_precision_score, matthews_corrcoef,
    cohen_kappa_score, accuracy_score, precision_score, recall_score, f1_score
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os
import json

# Set style for professional-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create output directory for graphs
os.makedirs('docs/images', exist_ok=True)

print("=" * 80)
print("QUILLBOT NIDS - Documentation Metrics Generator")
print("=" * 80)

# Load the trained model, scaler, and encoders
print("\n[1/8] Loading trained model and preprocessors...")
model = joblib.load('model/nids_model.pkl')
scaler = joblib.load('model/scaler.pkl')
encoder = joblib.load('model/encoder.pkl')
metadata = joblib.load('model/model_metadata.pkl')

print(f"✅ Model loaded: {metadata['model_type']}")
print(f"✅ Dataset: {metadata['dataset']}")
print(f"✅ Number of features: {metadata['num_features']}")

# Load the dataset
print("\n[2/8] Loading dataset...")
data_path = 'data/UNSW-NB15/unsw_nb15_combined.csv'
df = pd.read_csv(data_path)

print(f"✅ Dataset loaded: {len(df)} samples")
print(f"   - Normal: {len(df[df['Label'] == 0])} ({len(df[df['Label'] == 0])/len(df)*100:.1f}%)")
print(f"   - Intrusion: {len(df[df['Label'] == 1])} ({len(df[df['Label'] == 1])/len(df)*100:.1f}%)")

# Prepare features and labels
print("\n[3/8] Preparing features and labels...")
# Drop columns that shouldn't be used as features
cols_to_drop = ['Label', 'attack_cat', 'srcip', 'dstip', 'attack_cat_encoded']
X_raw = df.drop([col for col in cols_to_drop if col in df.columns], axis=1)
y = df['Label']
attack_types = df['attack_cat']

# Categorical features that need encoding
categorical_features = ['proto', 'service', 'state']

# Encode categorical features
X = X_raw.copy()
for col in categorical_features:
    if col in X.columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))

# Split into train and test sets (same split as training)
X_train, X_test, y_train, y_test, attack_train, attack_test = train_test_split(
    X, y, attack_types, test_size=0.2, random_state=42, stratify=y
)

print(f"✅ Train set: {len(X_train)} samples")
print(f"✅ Test set: {len(X_test)} samples")

# Make predictions on test set
print("\n[4/8] Generating predictions on test set...")
y_pred = model.predict(X_test.values)
y_pred_proba = model.predict_proba(X_test.values)

print(f"✅ Predictions generated for {len(y_test)} test samples")

# Calculate comprehensive metrics
print("\n[5/8] Calculating evaluation metrics...")

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()

# Calculate all metrics
accuracy = accuracy_score(y_test, y_pred)
precision_normal = precision_score(y_test, y_pred, pos_label=0)
precision_intrusion = precision_score(y_test, y_pred, pos_label=1)
recall_normal = recall_score(y_test, y_pred, pos_label=0)
recall_intrusion = recall_score(y_test, y_pred, pos_label=1)
f1_normal = f1_score(y_test, y_pred, pos_label=0)
f1_intrusion = f1_score(y_test, y_pred, pos_label=1)
specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
mcc = matthews_corrcoef(y_test, y_pred)
kappa = cohen_kappa_score(y_test, y_pred)

# Store metrics
metrics = {
    'accuracy': accuracy,
    'precision_normal': precision_normal,
    'precision_intrusion': precision_intrusion,
    'recall_normal': recall_normal,
    'recall_intrusion': recall_intrusion,
    'f1_normal': f1_normal,
    'f1_intrusion': f1_intrusion,
    'specificity': specificity,
    'fpr': fpr,
    'fnr': fnr,
    'mcc': mcc,
    'kappa': kappa,
    'tp': int(tp),
    'tn': int(tn),
    'fp': int(fp),
    'fn': int(fn)
}

print(f"✅ Metrics calculated:")
print(f"   - Accuracy: {accuracy*100:.2f}%")
print(f"   - Precision (Intrusion): {precision_intrusion*100:.2f}%")
print(f"   - Recall (Intrusion): {recall_intrusion*100:.2f}%")
print(f"   - F1-Score (Intrusion): {f1_intrusion*100:.2f}%")

# Save metrics to JSON
with open('docs/metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)

print("\n[6/8] Generating visualization graphs...")

# 1. Confusion Matrix
print("   📊 Creating Confusion Matrix...")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True, 
            xticklabels=['Normal', 'Intrusion'],
            yticklabels=['Normal', 'Intrusion'],
            annot_kws={'size': 16, 'weight': 'bold'})
plt.title('Confusion Matrix - QUILLBOT NIDS', fontsize=18, fontweight='bold', pad=20)
plt.ylabel('Actual Label', fontsize=14, fontweight='bold')
plt.xlabel('Predicted Label', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('docs/images/confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Confusion Matrix saved")

# 2. ROC Curve
print("   📊 Creating ROC Curve...")
fpr_roc, tpr_roc, _ = roc_curve(y_test, y_pred_proba[:, 1])
roc_auc = auc(fpr_roc, tpr_roc)

fig, ax = plt.subplots(figsize=(10, 8))
plt.plot(fpr_roc, tpr_roc, color='darkorange', lw=3, 
         label=f'ROC Curve (AUC = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate', fontsize=14, fontweight='bold')
plt.ylabel('True Positive Rate', fontsize=14, fontweight='bold')
plt.title('ROC Curve - QUILLBOT NIDS', fontsize=18, fontweight='bold', pad=20)
plt.legend(loc="lower right", fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('docs/images/roc_curve.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✅ ROC Curve saved (AUC = {roc_auc:.4f})")

# 3. Precision-Recall Curve
print("   📊 Creating Precision-Recall Curve...")
precision_curve, recall_curve, _ = precision_recall_curve(y_test, y_pred_proba[:, 1])
avg_precision = average_precision_score(y_test, y_pred_proba[:, 1])

fig, ax = plt.subplots(figsize=(10, 8))
plt.plot(recall_curve, precision_curve, color='green', lw=3,
         label=f'Precision-Recall Curve (AP = {avg_precision:.4f})')
plt.xlabel('Recall', fontsize=14, fontweight='bold')
plt.ylabel('Precision', fontsize=14, fontweight='bold')
plt.title('Precision-Recall Curve - QUILLBOT NIDS', fontsize=18, fontweight='bold', pad=20)
plt.legend(loc="lower left", fontsize=12)
plt.grid(True, alpha=0.3)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.tight_layout()
plt.savefig('docs/images/precision_recall_curve.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✅ Precision-Recall Curve saved (AP = {avg_precision:.4f})")

# 4. Feature Importance
print("   📊 Creating Feature Importance Chart...")
feature_importance = model.feature_importances_
feature_names = X.columns
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': feature_importance
}).sort_values('Importance', ascending=False).head(20)

fig, ax = plt.subplots(figsize=(12, 10))
sns.barplot(data=importance_df, y='Feature', x='Importance', palette='viridis')
plt.title('Top 20 Feature Importance - QUILLBOT NIDS', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Importance Score', fontsize=14, fontweight='bold')
plt.ylabel('Feature Name', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('docs/images/feature_importance.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Feature Importance Chart saved")

# 5. Class Distribution
print("   📊 Creating Class Distribution Chart...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Test set distribution
test_dist = pd.Series(y_test).value_counts().sort_index()
labels_test = ['Normal' if i == 0 else 'Intrusion' for i in test_dist.index]
ax1.pie(test_dist.values, labels=labels_test, autopct='%1.1f%%',
        colors=['#2ecc71', '#e74c3c'], startangle=90, textprops={'fontsize': 14, 'weight': 'bold'})
ax1.set_title('Test Set Distribution', fontsize=16, fontweight='bold', pad=20)

# Prediction distribution
pred_dist = pd.Series(y_pred).value_counts().sort_index()
labels_pred = ['Normal' if i == 0 else 'Intrusion' for i in pred_dist.index]
ax2.pie(pred_dist.values, labels=labels_pred, autopct='%1.1f%%',
        colors=['#2ecc71' if i == 0 else '#e74c3c' for i in pred_dist.index],
        startangle=90, textprops={'fontsize': 14, 'weight': 'bold'})
ax2.set_title('Prediction Distribution', fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('docs/images/class_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Class Distribution Chart saved")

print("\n[7/8] Generating sample predictions table...")

# Create sample predictions with details
sample_size = min(30, len(y_test))
sample_indices = np.random.choice(len(y_test), sample_size, replace=False)

predictions_data = []
for idx in sample_indices:
    actual = y_test.iloc[idx]
    predicted = y_pred[idx]
    confidence = y_pred_proba[idx][predicted] * 100
    attack_type = attack_test.iloc[idx] if predicted == 1 else 'N/A'
    correct = '✓' if actual == predicted else '✗'
    
    predictions_data.append({
        'sample_id': idx + 1,
        'actual': 'Normal' if actual == 0 else 'Intrusion',
        'predicted': 'Normal' if predicted == 0 else 'Intrusion',
        'confidence': confidence,
        'attack_type': attack_type,
        'correct': correct
    })

predictions_df = pd.DataFrame(predictions_data)
predictions_df.to_csv('docs/sample_predictions.csv', index=False)
print(f"✅ Sample predictions saved ({sample_size} samples)")

print("\n[8/8] Saving all metrics and data...")

# Save feature importance
importance_df.to_csv('docs/feature_importance.csv', index=False)

# Save comprehensive report
report = classification_report(y_test, y_pred, target_names=['Normal', 'Intrusion'], output_dict=True)
report_df = pd.DataFrame(report).transpose()
report_df.to_csv('docs/classification_report.csv')

print("✅ All metrics and visualizations generated successfully!")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"📊 Graphs generated: 5")
print(f"   - Confusion Matrix: docs/images/confusion_matrix.png")
print(f"   - ROC Curve: docs/images/roc_curve.png")
print(f"   - Precision-Recall Curve: docs/images/precision_recall_curve.png")
print(f"   - Feature Importance: docs/images/feature_importance.png")
print(f"   - Class Distribution: docs/images/class_distribution.png")
print(f"\n📄 Data files generated: 4")
print(f"   - Metrics: docs/metrics.json")
print(f"   - Sample Predictions: docs/sample_predictions.csv")
print(f"   - Feature Importance: docs/feature_importance.csv")
print(f"   - Classification Report: docs/classification_report.csv")
print("=" * 80)

