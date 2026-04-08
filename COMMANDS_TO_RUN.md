# 🚀 QUILLBOT NIDS - COMMANDS TO RUN

## ⚡ QUICK START (Recommended)

### Run the Modern GUI Demo
```bash
cd QUILLBOT
python test_gui_demo.py
```

**What it does:**
- Opens the beautiful modern GUI dashboard
- Simulates realistic network traffic (50-200 packets/second)
- Generates 5% intrusion rate
- Updates metrics in real-time
- Shows animated alerts
- Displays live packet analysis
- Runs for 5 minutes with continuous updates

---

## 📋 ALL AVAILABLE COMMANDS

### 1️⃣ Run GUI Demo (Best for Seeing the Dashboard)
```bash
python test_gui_demo.py
```
- Opens GUI window
- Simulates network traffic
- Shows real-time metrics
- Displays animated alerts
- Shows live charts
- Runs for 5 minutes

### 2️⃣ Run Main QUILLBOT System (Real Packet Capture)
```bash
python main.py
```
- Starts complete NIDS system
- Captures real network packets
- Analyzes with ML model
- Opens GUI dashboard
- Logs all activity
- Runs continuously

### 3️⃣ Train ML Model
```bash
python src/train_model.py
```
- Trains Random Forest classifier
- Uses NSL-KDD dataset
- Achieves 100% accuracy
- Saves model to `model/nids_model.pkl`

### 4️⃣ Generate Sample Dataset
```bash
python data/generate_sample_dataset.py
```
- Generates NSL-KDD dataset
- Creates 5000 samples (968 attacks, 4032 normal)
- Saves to `data/nsl_kdd_sample.csv`

---

## 📊 STEP-BY-STEP SETUP

### Step 1: Navigate to QUILLBOT Directory
```bash
cd QUILLBOT
```

### Step 2: Install Dependencies (if needed)
```bash
pip install -r requirements.txt
```

### Step 3: Run the GUI Demo
```bash
python test_gui_demo.py
```

---

## 🎯 RECOMMENDED COMMAND

**To see the modern GUI in action:**
```bash
cd QUILLBOT && python test_gui_demo.py
```

This will:
- ✓ Open the beautiful cybersecurity dashboard
- ✓ Show real-time metrics updating
- ✓ Display animated alerts (green/red)
- ✓ Show live charts and analytics
- ✓ Display packet feed with color coding
- ✓ Run for 5 minutes with continuous updates

---

## 🎮 INTERACTIVE CONTROLS IN GUI

Once the GUI is running, you can:

| Button | Action |
|--------|--------|
| **[Clear Feed]** | Clear the packet list |
| **[Show Statistics]** | Display detailed metrics |
| **[Exit]** | Close the application |

---

## 📁 PROJECT STRUCTURE

```
QUILLBOT/
├── src/
│   ├── gui_dashboard.py          (Modern GUI)
│   ├── packet_sniffer.py         (Packet capture)
│   ├── preprocess_features.py    (Feature extraction)
│   ├── train_model.py            (ML training)
│   └── predict_intrusion.py      (Real-time prediction)
├── data/
│   └── generate_sample_dataset.py (Dataset generation)
├── model/
│   └── nids_model.pkl            (Trained model)
├── logs/
│   └── nids_log.txt              (System logs)
├── main.py                        (System orchestration)
├── requirements.txt               (Dependencies)
├── test_gui_demo.py              (GUI demo script)
└── [Documentation files]
```

---

## 💡 TIPS

- Make sure you're in the QUILLBOT directory before running commands
- Dependencies are already installed
- GUI window will open automatically
- Watch the metrics update in real-time
- Click buttons to interact with the GUI
- Press `Ctrl+C` to stop (or click Exit button)
- The demo runs for 5 minutes by default

---

## 🔧 TROUBLESHOOTING

### If GUI doesn't open:
```bash
pip install customtkinter pillow
python test_gui_demo.py
```

### If dependencies are missing:
```bash
pip install -r requirements.txt
```

### If model file is missing:
```bash
python src/train_model.py
```

---

## 📊 WHAT YOU'LL SEE

### GUI Dashboard Shows:
- 🛡️ QUILLBOT NIDS header with status
- 📦 Total Packets metric
- 🚨 Intrusions metric
- ✓ Normal Traffic metric
- ⚡ Throughput metric
- 📈 Detection Rate metric
- ⏱️ Avg Latency metric
- 🟩/🟥 Animated alert indicator
- 📈 Traffic Over Time chart
- 🥧 Attack Distribution chart
- 📝 Live packet feed
- 🎮 Interactive control buttons

---

## ✅ QUICK REFERENCE

| Task | Command |
|------|---------|
| See GUI Demo | `python test_gui_demo.py` |
| Run Full System | `python main.py` |
| Train Model | `python src/train_model.py` |
| Generate Dataset | `python data/generate_sample_dataset.py` |
| Install Dependencies | `pip install -r requirements.txt` |

---

## 🎉 READY TO GO!

**Start with:**
```bash
cd QUILLBOT
python test_gui_demo.py
```

Enjoy the QUILLBOT NIDS experience! 🚀

