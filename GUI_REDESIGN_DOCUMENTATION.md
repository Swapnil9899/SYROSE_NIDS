# QUILLBOT NIDS - Modern GUI Redesign Documentation

## 🎨 Overview

The QUILLBOT NIDS GUI has been completely redesigned with a modern, professional cybersecurity aesthetic. The new interface uses **CustomTkinter** for modern styling and **Matplotlib** for real-time data visualization.

## ✨ Key Features

### 1. **Modern UI Framework**
- **CustomTkinter**: Modern Tkinter wrapper with sleek styling
- **Dark Theme**: Professional cybersecurity-themed dark interface
- **Neon Accents**: Bright green, red, blue, and yellow accent colors
- **Smooth Animations**: Animated alert indicators and status updates

### 2. **Visual Design**
- **Color Scheme**:
  - Primary Background: `#0a0e27` (Dark blue-black)
  - Secondary Background: `#1a1f3a` (Slightly lighter)
  - Accent Green: `#00ff41` (Neon green for normal traffic)
  - Accent Red: `#ff0055` (Neon red for intrusions)
  - Accent Blue: `#00d4ff` (Cyan for UI elements)
  - Accent Yellow: `#ffff00` (Bright yellow for headers)

- **Typography**:
  - Headers: Helvetica 28pt bold (neon green)
  - Titles: Helvetica 12pt bold (cyan)
  - Metrics: Helvetica 16pt bold (neon green)
  - Feed: Courier New 9pt (monospace for packet data)

### 3. **Dashboard Sections**

#### Header Section
- **Logo**: "🛡️ QUILLBOT NIDS" in large neon green text
- **Subtitle**: "AI-Powered Network Intrusion Detection System"
- **Status Indicator**: Real-time status (● MONITORING or ● ALERT)

#### Metrics Panel
Six metric cards displaying:
1. **Total Packets**: Total packets analyzed
2. **Intrusions**: Number of intrusions detected
3. **Normal Traffic**: Number of normal packets
4. **Throughput**: Packets per second
5. **Detection Rate**: Percentage of intrusions
6. **Avg Latency**: Average prediction latency in ms

#### Alert Status Panel
- **Animated Status Indicator**: Large circle with glow effect
  - Green for normal traffic
  - Red for intrusions
  - Animated pulsing effect
- **Status Text**: "🟩 NO INTRUSION" or "🟥 INTRUSION DETECTED!"
- **Last Alert Time**: Timestamp of last alert

#### Real-Time Analytics Panel
Two interactive charts:
1. **Traffic Over Time**: Line graph showing throughput trends
   - X-axis: Time (seconds)
   - Y-axis: Packets per second
   - Green line with fill area
2. **Attack Distribution**: Pie chart showing normal vs intrusion ratio
   - Green slice for normal packets
   - Red slice for intrusions
   - Percentage labels

#### Live Packet Feed
- **Scrollable Text Widget**: Real-time packet analysis log
- **Color Coding**:
  - Green text: Normal traffic
  - Red text: Intrusions
  - Yellow text: Headers
  - Blue text: Info messages
- **Format**: `[HH:MM:SS.mmm] STATUS | SRC:PORT → DST:PORT | PROTOCOL | SIZE | CONFIDENCE`

#### Control Footer
- **Clear Feed Button**: Clears the packet feed
- **Show Statistics Button**: Displays detailed statistics in console
- **Exit Button**: Gracefully shuts down the application

## 🔧 Technical Implementation

### Dependencies
```
customtkinter>=5.0.0
pillow>=9.0.0
matplotlib>=3.6.0
```

### Class Structure

#### NIDSDashboard
Main dashboard class with the following methods:

**Initialization**
- `__init__(root)`: Initialize the dashboard with CustomTkinter root window

**UI Building**
- `_build_ui()`: Build the complete dashboard layout
- `_create_metric_card()`: Create individual metric cards

**Data Management**
- `update_metrics()`: Update dashboard metrics from NIDS system
- `add_packet_alert()`: Add packet alerts to the feed

**Display Updates**
- `_update_display()`: Update all UI elements with current data
- `_update_charts()`: Update real-time charts with historical data
- `_draw_status_indicator()`: Draw animated status indicator

**User Interactions**
- `_clear_feed()`: Clear the packet feed
- `_show_statistics()`: Display detailed statistics
- `_exit_app()`: Gracefully exit the application

**Main Loop**
- `_start_update_loop()`: Start the periodic update thread
- `run()`: Run the dashboard main loop

### Data Structures

**Metrics Dictionary**
```python
{
    'total_packets': int,
    'intrusions': int,
    'normal': int,
    'throughput': float,
    'last_status': str,  # 'NORMAL' or 'INTRUSION'
    'last_alert_time': str,
    'uptime': float,
    'avg_latency': float,
    'detection_rate': float
}
```

**Historical Data**
- `packet_history`: Last 100 packets (deque)
- `throughput_history`: Last 60 seconds of throughput (deque)
- `intrusion_history`: Last 60 seconds of intrusions (deque)
- `normal_history`: Last 60 seconds of normal packets (deque)
- `timestamp_history`: Timestamps for chart x-axis (deque)

## 📊 Real-Time Charts

### Chart 1: Traffic Over Time
- **Type**: Line graph with fill area
- **Data**: Throughput history (last 60 seconds)
- **Color**: Neon green (#00ff41)
- **Updates**: Every 100ms
- **Purpose**: Monitor traffic trends and detect anomalies

### Chart 2: Attack Distribution
- **Type**: Pie chart
- **Data**: Normal vs Intrusion ratio
- **Colors**: Green (normal), Red (intrusions)
- **Updates**: Every 100ms
- **Purpose**: Visualize attack percentage and distribution

## 🎯 Color Scheme Reference

| Element | Color | Hex Code | Purpose |
|---------|-------|----------|---------|
| Background Primary | Dark Blue-Black | #0a0e27 | Main background |
| Background Secondary | Slightly Lighter | #1a1f3a | Panel backgrounds |
| Accent Green | Neon Green | #00ff41 | Normal traffic, success |
| Accent Red | Neon Red/Pink | #ff0055 | Intrusions, alerts |
| Accent Blue | Cyan | #00d4ff | UI elements, titles |
| Accent Yellow | Bright Yellow | #ffff00 | Headers, emphasis |
| Text Primary | Light Gray | #e0e0e0 | Main text |
| Text Secondary | Medium Gray | #a0a0a0 | Secondary text |

## 🔄 Update Cycle

The dashboard updates every 100ms (10 times per second) for smooth animations:

1. **Metrics Update**: Refresh all metric cards
2. **Status Update**: Update alert indicator and status text
3. **Chart Update**: Redraw real-time charts with new data
4. **Feed Update**: Add new packet alerts to the feed
5. **Animation**: Update animation state for pulsing effects

## 🚀 Usage

### Basic Usage
```python
import customtkinter as ctk
from src.gui_dashboard import NIDSDashboard

# Create root window
root = ctk.CTk()

# Create dashboard
dashboard = NIDSDashboard(root)

# Update metrics
dashboard.update_metrics({
    'total_packets': 1000,
    'intrusions': 50,
    'normal': 950,
    'throughput': 150.5,
    'avg_latency': 45.2
})

# Add packet alert
dashboard.add_packet_alert({
    'src_ip': '192.168.1.100',
    'dst_ip': '10.0.0.1',
    'protocol': 'tcp',
    'src_port': 54321,
    'dst_port': 80,
    'confidence': 0.95,
    'packet_length': 512
}, is_intrusion=False)

# Run dashboard
dashboard.run()
```

### Integration with QUILLBOT System
The dashboard integrates seamlessly with the QUILLBOT NIDS system:

```python
# In main.py
from src.gui_dashboard import NIDSDashboard
import customtkinter as ctk

root = ctk.CTk()
dashboard = NIDSDashboard(root)

# In packet processing loop
dashboard.update_metrics({
    'total_packets': total_packets,
    'intrusions': intrusions_count,
    'normal': normal_count,
    'throughput': packets_per_second,
    'avg_latency': average_latency
})

dashboard.add_packet_alert(packet_info, is_intrusion)
```

## 🎨 Customization

### Change Color Scheme
Modify the color constants in the `NIDSDashboard` class:

```python
COLOR_BG_PRIMARY = "#0a0e27"      # Change primary background
COLOR_ACCENT_GREEN = "#00ff41"    # Change normal traffic color
COLOR_ACCENT_RED = "#ff0055"      # Change intrusion color
```

### Adjust Update Frequency
Modify the sleep time in `_start_update_loop()`:

```python
time.sleep(0.1)  # Change to 0.05 for 20 updates/sec, 0.2 for 5 updates/sec
```

### Modify Chart History Length
Change the `maxlen` parameter in `__init__()`:

```python
self.throughput_history = deque(maxlen=120)  # 2 minutes instead of 1 minute
```

## 📈 Performance Considerations

- **Update Frequency**: 100ms (10 Hz) provides smooth animations without excessive CPU usage
- **Chart History**: 60 seconds of data balances responsiveness with memory usage
- **Thread Safety**: All data access is protected with locks to prevent race conditions
- **Memory Usage**: Deques with fixed maxlen prevent unbounded memory growth

## 🐛 Troubleshooting

### Issue: Charts not displaying
**Solution**: Ensure matplotlib is installed: `pip install matplotlib`

### Issue: GUI appears frozen
**Solution**: The update loop runs in a separate thread. If frozen, check for exceptions in the console.

### Issue: Colors look different
**Solution**: Ensure CustomTkinter is properly installed: `pip install customtkinter --upgrade`

### Issue: Text is too small/large
**Solution**: Modify font sizes in `_build_ui()` and `_create_metric_card()` methods

## 📝 Future Enhancements

- [ ] Export dashboard screenshot functionality
- [ ] Customizable color themes
- [ ] Additional chart types (heatmaps, histograms)
- [ ] Real-time alerts with sound notifications
- [ ] Dashboard recording/playback
- [ ] Multi-window support for detailed views
- [ ] Dark/Light theme toggle
- [ ] Customizable metric cards

## 🔐 Security Notes

- Dashboard runs in the main thread for UI updates
- Packet processing runs in separate threads
- All data access is thread-safe with locks
- No sensitive data is logged to console by default
- Logs contain IP addresses - handle securely

## 📞 Support

For issues or questions about the GUI redesign:
1. Check the troubleshooting section above
2. Review the code comments in `gui_dashboard.py`
3. Consult the main README.md for system-wide information

---

**QUILLBOT NIDS GUI v2.0.0** - Modern Cybersecurity Dashboard
**Last Updated**: November 9, 2025

