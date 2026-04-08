# 🚀 QUILLBOT NIDS - QUICK START GUIDE

## ✅ Status: PRODUCTION READY - All Issues Fixed!

### 1. Prerequisites
```
pip install -r requirements.txt
```

### 2. Run Demo (Recommended - Simulated Traffic + GUI)
```
cd QUILLBOT
python main_with_simulator.py
```
**Expected**: Modern GUI dashboard opens with live metrics, simulated traffic analysis.

### 3. Run Live Packet Capture
```
cd QUILLBOT
python main.py
```
**Note**: Requires Npcap (Windows) or libpcap (Linux/Mac), admin privileges.

### 4. Generate Documentation
```
cd QUILLBOT
python generate_documentation_metrics.py
```

### 5. Test Individual Components
```
python test_gui_demo.py      # GUI demo
python test_packet_sniffer.py # Sniffer test
```

## 📊 What You'll See
- **GUI Dashboard**: Real-time metrics, packet feed, alerts
- **Logs**: `logs/quillbot.log`, `logs/nids_log.txt`
- **Models**: `model/nids_model.pkl` (UNSW-NB15 trained)

## 🆘 Troubleshooting
| Issue | Solution |
|-------|----------|
| GUI not appearing | Check taskbar, may be minimized |
| Npcap error | Install Npcap: https://npcap.com |
| Model missing | Run `python src/train_model_v2.py` |
| Import errors | `pip install -r requirements.txt` |

## 📚 Full Documentation
- `docs/PROJECT_REPORT.md` - Academic report
- `docs/metrics.json` - Latest model metrics (98% recall)
- Multiple READMEs for specific features

**QUILLBOT NIDS v2.0 - Ready for Demo!** 🎉

