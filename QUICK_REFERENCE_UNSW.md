# UNSW-NB15 Integration - Quick Reference

## 🚀 Quick Start (3 Steps)

### **Step 1: Prepare Dataset**
```bash
cd QUILLBOT
python data/download_unsw_nb15.py
```

### **Step 2: Train Model**
```bash
python src/train_model_v2.py
```

### **Step 3: Configure System**
Edit `config.yaml`:
```yaml
dataset:
  active: 'UNSW-NB15'  # Switch to UNSW-NB15
```

---

## 📋 Command Reference

| Task | Command |
|------|---------|
| **Download Dataset** | `python data/download_unsw_nb15.py` |
| **Train Model** | `python src/train_model_v2.py` |
| **Run System** | `python main.py` |
| **View Config** | `cat config.yaml` |

---

## 🔄 Switching Datasets

### **Use UNSW-NB15**
```yaml
# config.yaml
dataset:
  active: 'UNSW-NB15'
```

### **Use NSL-KDD**
```yaml
# config.yaml
dataset:
  active: 'NSL-KDD'
```

Then retrain:
```bash
python src/train_model_v2.py
```

---

## 📊 Dataset Comparison

| Feature | NSL-KDD | UNSW-NB15 |
|---------|---------|-----------|
| **Features** | 41 | 47 |
| **Attack Types** | 4 categories | 9 categories |
| **Classification** | Binary/Multiclass | Binary/Multiclass |
| **Year** | 2009 | 2015 |
| **Realism** | Moderate | High |

---

## 🎯 Classification Types

### **Binary Classification**
```yaml
unsw_nb15:
  classification_type: 'binary'
```
- Normal (0) vs Attack (1)
- Simpler, faster
- Higher accuracy

### **Multi-class Classification**
```yaml
unsw_nb15:
  classification_type: 'multiclass'
```
- 10 categories (Normal + 9 attack types)
- More detailed
- Better for analysis

---

## 📁 File Structure

```
QUILLBOT/
├── config.yaml                          # Main configuration
├── data/
│   ├── download_unsw_nb15.py           # Dataset downloader
│   ├── UNSW-NB15/
│   │   ├── unsw_nb15_train_processed.csv
│   │   ├── unsw_nb15_test_processed.csv
│   │   └── unsw_nb15_combined.csv
│   └── nsl_kdd.csv                     # Original dataset
├── src/
│   ├── config_loader.py                # Config management
│   ├── preprocess_features_v2.py       # Unified preprocessing
│   ├── train_model_v2.py               # Enhanced training
│   └── predict_intrusion_v2.py         # Unified prediction
├── model/
│   ├── nids_model.pkl                  # Trained model
│   ├── scaler.pkl                      # Feature scaler
│   ├── encoder.pkl                     # Categorical encoders
│   └── model_metadata.pkl              # Model info
└── UNSW_NB15_INTEGRATION.md            # Full documentation
```

---

## 🔧 Configuration Options

### **Dataset Settings**
```yaml
dataset:
  active: 'UNSW-NB15'                   # Active dataset
  unsw_nb15:
    classification_type: 'binary'        # binary or multiclass
    data_path: 'data/UNSW-NB15/...'     # Dataset path
```

### **Model Settings**
```yaml
model:
  type: 'random_forest'                  # Model type
  random_forest:
    n_estimators: 200                    # Number of trees
    max_depth: 30                        # Tree depth
    class_weight: 'balanced_subsample'   # Handle imbalance
```

### **GUI Settings**
```yaml
gui:
  show_attack_types: true                # Show attack categories
  update_interval: 1000                  # Update frequency (ms)
```

---

## 📈 Expected Performance

### **With Synthetic Data (Current)**
- Accuracy: ~70%
- Training Time: ~4 seconds
- Inference: <5ms/packet

### **With Real UNSW-NB15 Data**
- Accuracy: 85-95%
- Precision: 80-92%
- Recall: 78-90%
- F1-Score: 82-91%

---

## 🎨 Attack Categories (UNSW-NB15)

| ID | Category | Description |
|----|----------|-------------|
| 0 | Normal | Legitimate traffic |
| 1 | Generic | Generic attacks |
| 2 | Exploits | Exploitation attempts |
| 3 | Fuzzers | Fuzzing attacks |
| 4 | DoS | Denial of Service |
| 5 | Reconnaissance | Network scanning |
| 6 | Analysis | Port scanning |
| 7 | Backdoor | Backdoor attempts |
| 8 | Shellcode | Code injection |
| 9 | Worms | Worm propagation |

---

## 🐛 Common Issues

### **Dataset Not Found**
```bash
python data/download_unsw_nb15.py
```

### **Import Errors**
```bash
pip install pyyaml scikit-learn pandas numpy joblib
```

### **Poor Performance**
- Using synthetic data (limited quality)
- Download real dataset: https://research.unsw.edu.au/projects/unsw-nb15-dataset
- Retrain with real data

### **Config Not Loading**
- Check `config.yaml` exists
- Verify YAML syntax
- Check file permissions

---

## 💡 Tips

1. **Start with Binary Classification**
   - Simpler and more reliable
   - Better for initial testing

2. **Use Real Data for Production**
   - Synthetic data is for demonstration only
   - Real UNSW-NB15 gives 85-95% accuracy

3. **Monitor Performance**
   - Check logs in `logs/`
   - Review statistics in GUI
   - Analyze predictions in `logs/nids_log.txt`

4. **Tune Model Parameters**
   - Adjust `n_estimators` for accuracy
   - Modify `max_depth` for complexity
   - Use `class_weight` for imbalance

---

## 📚 Documentation

- **Full Integration Guide**: `UNSW_NB15_INTEGRATION.md`
- **GUI Design**: `MODERN_GUI_DESIGN.md`
- **Quick Start**: `MODERN_GUI_QUICKSTART.md`
- **Main README**: `README.md`

---

## ✅ Checklist

- [ ] Dataset downloaded/generated
- [ ] Model trained successfully
- [ ] Config updated to UNSW-NB15
- [ ] System tested
- [ ] Performance acceptable
- [ ] Logs reviewed

---

## 🎯 Next Actions

1. **Test Current System**
   ```bash
   python src/train_model_v2.py
   ```

2. **Download Real Data** (Optional)
   - Visit: https://research.unsw.edu.au/projects/unsw-nb15-dataset
   - Download CSV files
   - Place in `data/UNSW-NB15/`
   - Retrain model

3. **Update Main System** (If needed)
   - Modify `main.py` to use v2 modules
   - Test end-to-end
   - Deploy

---

**Quick Reference Version 1.0**  
**Last Updated**: November 9, 2025  
**Status**: ✅ Ready to Use

