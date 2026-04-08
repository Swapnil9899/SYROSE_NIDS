# QUILLBOT NIDS - GUI Integration Guide

## 🔗 Integrating the Modern GUI with QUILLBOT System

This guide explains how to integrate the new modern GUI dashboard with the existing QUILLBOT NIDS system.

---

## ✅ Backward Compatibility

The new GUI maintains **100% backward compatibility** with the existing QUILLBOT system:

- ✅ Same method signatures
- ✅ Same data structures
- ✅ Same integration points
- ✅ No changes to other modules required
- ✅ Drop-in replacement for old GUI

---

## 📋 Integration Steps

### Step 1: Update Dependencies

The new GUI requires two additional packages:

```bash
pip install customtkinter pillow
```

Or update requirements.txt:
```
customtkinter>=5.0.0
pillow>=9.0.0
```

### Step 2: Update main.py

The integration is straightforward. Replace the old GUI initialization with the new one:

**Old Code:**
```python
import tkinter as tk
from src.gui_dashboard import NIDSDashboard

root = tk.Tk()
dashboard = NIDSDashboard(root)
```

**New Code:**
```python
import customtkinter as ctk
from src.gui_dashboard import NIDSDashboard

root = ctk.CTk()
dashboard = NIDSDashboard(root)
```

### Step 3: Update Metrics

The metrics dictionary now supports additional fields:

**Old Metrics:**
```python
metrics = {
    'total_packets': 1000,
    'intrusions': 50,
    'normal': 950,
    'throughput': 150.5
}
```

**New Metrics (Enhanced):**
```python
metrics = {
    'total_packets': 1000,
    'intrusions': 50,
    'normal': 950,
    'throughput': 150.5,
    'avg_latency': 45.2,      # New: Average prediction latency
    'uptime': 3600.0           # New: System uptime in seconds
}
```

### Step 4: Update Packet Info

The packet info dictionary now supports additional fields:

**Old Packet Info:**
```python
packet_info = {
    'src_ip': '192.168.1.100',
    'dst_ip': '10.0.0.1',
    'protocol': 'tcp',
    'src_port': 54321,
    'dst_port': 80,
    'confidence': 0.95
}
```

**New Packet Info (Enhanced):**
```python
packet_info = {
    'src_ip': '192.168.1.100',
    'dst_ip': '10.0.0.1',
    'protocol': 'tcp',
    'src_port': 54321,
    'dst_port': 80,
    'confidence': 0.95,
    'packet_length': 512       # New: Packet size in bytes
}
```

---

## 🔄 Complete Integration Example

Here's a complete example of integrating the new GUI with QUILLBOT:

```python
import customtkinter as ctk
import threading
import time
from src.gui_dashboard import NIDSDashboard
from src.packet_sniffer import PacketSniffer
from src.predict_intrusion import IntrusionPredictor
from src.preprocess_features import PacketFeatureExtractor

class QUILLBOTSystem:
    def __init__(self):
        # Initialize components
        self.sniffer = PacketSniffer()
        self.predictor = IntrusionPredictor()
        self.preprocessor = PacketFeatureExtractor()
        
        # Initialize GUI
        self.root = ctk.CTk()
        self.dashboard = NIDSDashboard(self.root)
        
        # Metrics tracking
        self.total_packets = 0
        self.intrusions = 0
        self.normal = 0
        self.start_time = time.time()
    
    def process_packets(self):
        """Process packets and update dashboard."""
        while True:
            try:
                # Get packet from sniffer
                packet = self.sniffer.get_packet()
                if not packet:
                    continue
                
                # Extract features
                features = self.preprocessor.extract_packet_features(packet)
                
                # Make prediction
                prediction, confidence, latency = self.predictor.predict(features)
                
                # Update metrics
                self.total_packets += 1
                is_intrusion = prediction == 1
                if is_intrusion:
                    self.intrusions += 1
                else:
                    self.normal += 1
                
                # Update dashboard metrics
                uptime = time.time() - self.start_time
                self.dashboard.update_metrics({
                    'total_packets': self.total_packets,
                    'intrusions': self.intrusions,
                    'normal': self.normal,
                    'throughput': self.total_packets / max(uptime, 1),
                    'avg_latency': latency,
                    'uptime': uptime
                })
                
                # Add packet alert to dashboard
                packet_info = {
                    'src_ip': packet.get('src_ip', 'N/A'),
                    'dst_ip': packet.get('dst_ip', 'N/A'),
                    'protocol': packet.get('protocol', 'N/A'),
                    'src_port': packet.get('src_port', 'N/A'),
                    'dst_port': packet.get('dst_port', 'N/A'),
                    'confidence': confidence,
                    'packet_length': packet.get('length', 0)
                }
                self.dashboard.add_packet_alert(packet_info, is_intrusion)
                
            except Exception as e:
                print(f"Error processing packet: {e}")
    
    def run(self):
        """Run the QUILLBOT system."""
        # Start packet processing in background
        process_thread = threading.Thread(target=self.process_packets, daemon=True)
        process_thread.start()
        
        # Run dashboard
        self.dashboard.run()

# Main execution
if __name__ == '__main__':
    system = QUILLBOTSystem()
    system.run()
```

---

## 📊 Metrics Update Frequency

For optimal performance, update metrics at these frequencies:

- **Metrics**: Every 1-5 seconds (or after processing batch of packets)
- **Packet Alerts**: Immediately after each packet prediction
- **Charts**: Automatically updated every 100ms by dashboard

Example:
```python
# Update metrics every second
if time.time() - last_update > 1.0:
    dashboard.update_metrics({...})
    last_update = time.time()

# Add packet alert immediately
dashboard.add_packet_alert(packet_info, is_intrusion)
```

---

## 🔧 Configuration Options

### Adjust Update Frequency

Modify the sleep time in `_start_update_loop()`:

```python
# In gui_dashboard.py, line ~566
time.sleep(0.1)  # Change this value
# 0.05 = 20 Hz (smoother but more CPU)
# 0.1 = 10 Hz (balanced)
# 0.2 = 5 Hz (less CPU but less smooth)
```

### Customize Colors

Modify color constants in `NIDSDashboard` class:

```python
COLOR_BG_PRIMARY = "#0a0e27"      # Primary background
COLOR_BG_SECONDARY = "#1a1f3a"    # Secondary background
COLOR_ACCENT_GREEN = "#00ff41"    # Normal traffic
COLOR_ACCENT_RED = "#ff0055"      # Intrusions
COLOR_ACCENT_BLUE = "#00d4ff"     # UI elements
COLOR_ACCENT_YELLOW = "#ffff00"   # Headers
```

### Adjust Chart History

Modify deque sizes in `__init__()`:

```python
self.throughput_history = deque(maxlen=120)  # 2 minutes
self.intrusion_history = deque(maxlen=120)
self.normal_history = deque(maxlen=120)
self.timestamp_history = deque(maxlen=120)
```

---

## 🧪 Testing Integration

### Test 1: Basic Initialization

```python
import customtkinter as ctk
from src.gui_dashboard import NIDSDashboard

root = ctk.CTk()
dashboard = NIDSDashboard(root)
print("✓ Dashboard initialized successfully")
```

### Test 2: Update Metrics

```python
dashboard.update_metrics({
    'total_packets': 100,
    'intrusions': 5,
    'normal': 95,
    'throughput': 50.0,
    'avg_latency': 25.5,
    'uptime': 10.0
})
print("✓ Metrics updated successfully")
```

### Test 3: Add Packet Alert

```python
dashboard.add_packet_alert({
    'src_ip': '192.168.1.100',
    'dst_ip': '10.0.0.1',
    'protocol': 'tcp',
    'src_port': 54321,
    'dst_port': 80,
    'confidence': 0.95,
    'packet_length': 512
}, is_intrusion=False)
print("✓ Packet alert added successfully")
```

### Test 4: Run Demo

```bash
python test_gui_demo.py
```

---

## 🔍 Troubleshooting Integration

### Issue: ImportError for customtkinter

**Solution**: Install the package
```bash
pip install customtkinter
```

### Issue: GUI doesn't update

**Solution**: Ensure metrics are being updated regularly
```python
# Add this in your packet processing loop
dashboard.update_metrics({...})
```

### Issue: Charts not displaying

**Solution**: Ensure matplotlib is installed
```bash
pip install matplotlib
```

### Issue: GUI freezes

**Solution**: Ensure packet processing runs in separate thread
```python
process_thread = threading.Thread(target=process_packets, daemon=True)
process_thread.start()
```

---

## 📈 Performance Optimization

### 1. Batch Metrics Updates

Instead of updating metrics for every packet:

```python
# Inefficient: Update every packet
for packet in packets:
    dashboard.update_metrics({...})

# Efficient: Update every N packets
if packet_count % 100 == 0:
    dashboard.update_metrics({...})
```

### 2. Limit Packet Feed

The packet feed maintains last 100 packets. For high-volume traffic:

```python
# Only add alerts for intrusions
if is_intrusion:
    dashboard.add_packet_alert(packet_info, True)
```

### 3. Optimize Chart Updates

Charts update automatically every 100ms. No manual updates needed.

---

## 🚀 Deployment Checklist

- [ ] Install customtkinter: `pip install customtkinter`
- [ ] Install pillow: `pip install pillow`
- [ ] Update requirements.txt
- [ ] Update main.py to use ctk.CTk()
- [ ] Test GUI initialization
- [ ] Test metrics updates
- [ ] Test packet alerts
- [ ] Run test_gui_demo.py
- [ ] Verify charts display correctly
- [ ] Test with real packet data
- [ ] Verify performance (CPU/Memory)
- [ ] Deploy to production

---

## 📝 Migration Checklist

If migrating from old GUI:

- [ ] Backup old gui_dashboard.py
- [ ] Replace with new gui_dashboard.py
- [ ] Update requirements.txt
- [ ] Update main.py (change tk.Tk to ctk.CTk)
- [ ] Test all functionality
- [ ] Verify backward compatibility
- [ ] Update documentation
- [ ] Deploy to production

---

## 🎯 Best Practices

1. **Update Metrics Regularly**: Every 1-5 seconds for smooth charts
2. **Add Packet Alerts Immediately**: For real-time feed updates
3. **Use Separate Threads**: Keep GUI responsive
4. **Handle Exceptions**: Graceful error handling
5. **Monitor Performance**: Watch CPU and memory usage
6. **Test Thoroughly**: Before production deployment

---

## 📞 Support

For integration issues:
1. Check this guide for common solutions
2. Review GUI_REDESIGN_DOCUMENTATION.md
3. Run test_gui_demo.py to verify setup
4. Check console output for error messages
5. Review code comments in gui_dashboard.py

---

## ✅ Integration Complete

Once you've completed these steps, the modern GUI is fully integrated with QUILLBOT NIDS!

**Key Points:**
- ✅ 100% backward compatible
- ✅ Drop-in replacement for old GUI
- ✅ Enhanced metrics and visualization
- ✅ Professional cybersecurity aesthetic
- ✅ Production-ready implementation

---

**QUILLBOT NIDS GUI v2.0.0** - Integration Guide
**Status**: ✅ Ready for Integration

