# UNSW-NB15 Real Dataset Download Guide

**Version**: 1.0.0  
**Date**: November 9, 2025  
**Purpose**: Step-by-step guide to download and integrate the real UNSW-NB15 dataset

---

## 📥 **DOWNLOAD OPTIONS**

### **Option 1: Kaggle (Recommended - Easiest)**

**Dataset**: https://www.kaggle.com/datasets/alextamboli/unsw-nb15

**Steps**:

1. **Create Kaggle Account** (if you don't have one)
   - Go to https://www.kaggle.com/
   - Click "Register" and create a free account

2. **Download Dataset**
   - Visit: https://www.kaggle.com/datasets/alextamboli/unsw-nb15
   - Click the "Download" button (top right)
   - Save the ZIP file to your computer

3. **Extract Files**
   - Extract the downloaded ZIP file
   - You should see files like:
     - `UNSW_NB15_training-set.csv`
     - `UNSW_NB15_testing-set.csv`
     - Or similar CSV files

4. **Place Files**
   - Copy the CSV files to: `QUILLBOT/data/UNSW-NB15/raw/`
   - Create the directory if it doesn't exist

5. **Process Dataset**
   ```bash
   cd QUILLBOT
   python download_real_unsw_nb15.py
   ```

---

### **Option 2: Kaggle API (For Advanced Users)**

**Requirements**:
- Kaggle account
- Kaggle API credentials

**Steps**:

1. **Install Kaggle Package**
   ```bash
   pip install kaggle
   ```

2. **Get API Credentials**
   - Go to https://www.kaggle.com/settings
   - Scroll to "API" section
   - Click "Create New API Token"
   - This downloads `kaggle.json`

3. **Configure Credentials**
   
   **Windows**:
   ```bash
   mkdir %USERPROFILE%\.kaggle
   move kaggle.json %USERPROFILE%\.kaggle\
   ```
   
   **Linux/Mac**:
   ```bash
   mkdir -p ~/.kaggle
   mv kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   ```

4. **Download Dataset**
   ```bash
   cd QUILLBOT
   python download_real_unsw_nb15.py
   ```

---

### **Option 3: Official UNSW Source**

**Dataset**: https://research.unsw.edu.au/projects/unsw-nb15-dataset

**Steps**:

1. **Visit Official Page**
   - Go to: https://research.unsw.edu.au/projects/unsw-nb15-dataset
   - Scroll to "Download" section

2. **Download Files**
   - Download these files:
     - `UNSW-NB15_1.csv`
     - `UNSW-NB15_2.csv`
     - `UNSW-NB15_3.csv`
     - `UNSW-NB15_4.csv`
     - `UNSW_NB15_features.csv` (feature descriptions)

3. **Place Files**
   - Copy all CSV files to: `QUILLBOT/data/UNSW-NB15/raw/`

4. **Combine Files** (Manual)
   ```python
   import pandas as pd
   
   # Load all parts
   df1 = pd.read_csv('data/UNSW-NB15/raw/UNSW-NB15_1.csv')
   df2 = pd.read_csv('data/UNSW-NB15/raw/UNSW-NB15_2.csv')
   df3 = pd.read_csv('data/UNSW-NB15/raw/UNSW-NB15_3.csv')
   df4 = pd.read_csv('data/UNSW-NB15/raw/UNSW-NB15_4.csv')
   
   # Combine
   combined = pd.concat([df1, df2, df3, df4], ignore_index=True)
   
   # Save
   combined.to_csv('data/UNSW-NB15/unsw_nb15_combined.csv', index=False)
   ```

---

### **Option 4: IEEE DataPort**

**Dataset**: https://ieee-dataport.org/documents/unswnb15-dataset

**Steps**:

1. **Create IEEE Account** (if needed)
   - Go to https://ieee-dataport.org/
   - Register for a free account

2. **Download Dataset**
   - Visit: https://ieee-dataport.org/documents/unswnb15-dataset
   - Click "Download" button
   - Extract the files

3. **Follow Option 3 Steps** (same file structure)

---

## 🔧 **MANUAL INTEGRATION STEPS**

If you've downloaded the dataset manually, follow these steps:

### **Step 1: Verify Files**

Check that you have these files in `QUILLBOT/data/UNSW-NB15/raw/`:
```
QUILLBOT/
└── data/
    └── UNSW-NB15/
        └── raw/
            ├── UNSW_NB15_training-set.csv  (or UNSW-NB15_1.csv, etc.)
            └── UNSW_NB15_testing-set.csv   (or UNSW-NB15_2.csv, etc.)
```

### **Step 2: Process Dataset**

**Option A: Use Automated Script**
```bash
cd QUILLBOT
python download_real_unsw_nb15.py
```

**Option B: Manual Processing**
```python
import pandas as pd

# Load training data
train_df = pd.read_csv('data/UNSW-NB15/raw/UNSW_NB15_training-set.csv')
print(f"Training samples: {len(train_df)}")

# Load testing data
test_df = pd.read_csv('data/UNSW-NB15/raw/UNSW_NB15_testing-set.csv')
print(f"Testing samples: {len(test_df)}")

# Combine
combined_df = pd.concat([train_df, test_df], ignore_index=True)
print(f"Total samples: {len(combined_df)}")

# Save processed files
train_df.to_csv('data/UNSW-NB15/unsw_nb15_train_processed.csv', index=False)
test_df.to_csv('data/UNSW-NB15/unsw_nb15_test_processed.csv', index=False)
combined_df.to_csv('data/UNSW-NB15/unsw_nb15_combined.csv', index=False)

print("✓ Processing complete!")
```

### **Step 3: Verify Dataset**

```python
import pandas as pd

# Load combined dataset
df = pd.read_csv('data/UNSW-NB15/unsw_nb15_combined.csv')

print(f"Total samples: {len(df)}")
print(f"Features: {len(df.columns)}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nLabel distribution:")
print(df['label'].value_counts())  # or 'attack_cat' depending on file
```

**Expected Output**:
```
Total samples: 257,673
Features: 49
Label distribution:
0    175,341  (Normal)
1     82,332  (Attack)
```

### **Step 4: Retrain Model**

```bash
cd QUILLBOT
python src/train_model_v2.py
```

**Expected Output**:
```
Training set: 206,138 samples
Testing set: 51,535 samples
Accuracy: 85-95%
Precision: 80-92%
Recall: 78-90%
F1-Score: 82-91%
```

### **Step 5: Test System**

```bash
python test_unsw_integration.py
```

### **Step 6: Run NIDS**

```bash
python main.py
```

---

## 📊 **DATASET INFORMATION**

### **UNSW-NB15 Dataset Details**

- **Total Records**: 2,540,044 (raw) or 257,673 (processed)
- **Training Set**: 175,341 records
- **Testing Set**: 82,332 records
- **Features**: 49 total (47 used for training)
- **Attack Categories**: 9 types
  - Generic
  - Exploits
  - Fuzzers
  - DoS
  - Reconnaissance
  - Analysis
  - Backdoor
  - Shellcode
  - Worms

### **Feature Categories**

1. **Flow Features** (5): srcip, sport, dstip, dsport, proto
2. **Basic Features** (13): state, dur, sbytes, dbytes, sttl, dttl, etc.
3. **Content Features** (9): Sload, Dload, Spkts, Dpkts, etc.
4. **Time Features** (9): Sjit, Djit, Stime, Ltime, Sintpkt, Dintpkt, etc.
5. **Connection Features** (13): ct_state_ttl, ct_flw_http_mthd, etc.

### **Label Information**

- **Binary Classification**: 0 (Normal) vs 1 (Attack)
- **Multi-class Classification**: 10 classes (Normal + 9 attack types)

---

## ⚠️ **TROUBLESHOOTING**

### **Problem 1: Download Fails**

**Error**: HTTP 403 Forbidden or Access Denied

**Solutions**:
1. Try different download option (Kaggle instead of official source)
2. Check if you're logged in to the website
3. Use manual download instead of automated script
4. Try alternative mirrors (IEEE DataPort, GitHub)

### **Problem 2: File Not Found**

**Error**: `FileNotFoundError: data/UNSW-NB15/unsw_nb15_combined.csv`

**Solutions**:
1. Verify files are in correct directory: `data/UNSW-NB15/raw/`
2. Check file names match expected names
3. Run processing script: `python download_real_unsw_nb15.py`
4. Manually combine files using Python script above

### **Problem 3: Column Mismatch**

**Error**: `KeyError: 'label'` or missing columns

**Solutions**:
1. Check column names in your CSV file:
   ```python
   import pandas as pd
   df = pd.read_csv('data/UNSW-NB15/raw/your_file.csv')
   print(df.columns)
   ```
2. Update `config.yaml` if column names differ
3. Rename columns to match expected format

### **Problem 4: Low Accuracy After Training**

**Possible Causes**:
- Still using synthetic data
- Incorrect label column
- Feature mismatch

**Solutions**:
1. Verify you're using real data:
   ```python
   import pandas as pd
   df = pd.read_csv('data/UNSW-NB15/unsw_nb15_combined.csv')
   print(f"Samples: {len(df)}")  # Should be ~257K, not 20K
   ```
2. Check label distribution
3. Retrain model: `python src/train_model_v2.py`

---

## ✅ **VERIFICATION CHECKLIST**

Before proceeding, verify:

- [ ] Dataset downloaded (257K+ samples)
- [ ] Files placed in `data/UNSW-NB15/` directory
- [ ] `unsw_nb15_combined.csv` exists
- [ ] File has 49 columns
- [ ] Label column exists (0/1 or attack categories)
- [ ] Model retrained with real data
- [ ] Accuracy improved to 85-95%
- [ ] Test script passes all tests
- [ ] Main system runs without errors

---

## 📞 **SUPPORT**

If you encounter issues:

1. **Check Logs**: Look for error messages in terminal output
2. **Verify Files**: Ensure all files are in correct locations
3. **Check Documentation**: Review `UNSW_NB15_INTEGRATION.md`
4. **Test Components**: Run `python test_unsw_integration.py`

---

## 🎯 **QUICK REFERENCE**

**Download from Kaggle**:
```
1. Visit: https://www.kaggle.com/datasets/alextamboli/unsw-nb15
2. Click "Download"
3. Extract to: QUILLBOT/data/UNSW-NB15/raw/
4. Run: python download_real_unsw_nb15.py
5. Retrain: python src/train_model_v2.py
```

**Expected Performance**:
- Accuracy: 85-95%
- Training Time: ~10 seconds
- Inference: <5ms per packet

---

**Last Updated**: November 9, 2025  
**Version**: 1.0.0  
**Author**: QUILLBOT Development Team

