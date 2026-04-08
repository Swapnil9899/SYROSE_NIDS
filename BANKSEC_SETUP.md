# BankSec NIDS - Setup and Integration Guide

## 🏦 Overview

**BankSec NIDS** is an enterprise-grade Network Intrusion Detection System specifically designed for financial institutions and banking Security Operations Centers (SOC). This guide covers the complete setup, configuration, and testing procedures.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Database Initialization](#database-initialization)
4. [User Management](#user-management)
5. [Configuration](#configuration)
6. [Running the System](#running-the-system)
7. [Features Overview](#features-overview)
8. [Testing Checklist](#testing-checklist)
9. [Troubleshooting](#troubleshooting)

---

## 🖥️ System Requirements

### Hardware
- **CPU**: Multi-core processor (4+ cores recommended)
- **RAM**: 8 GB minimum, 16 GB recommended
- **Storage**: 10 GB free space
- **Network**: Active network interface

### Software
- **OS**: Windows 10/11, Linux, macOS
- **Python**: 3.8 or higher
- **Internet**: Required for GeoIP lookups (optional)

---

## 📦 Installation

### Step 1: Install Python Dependencies

```bash
cd QUILLBOT
pip install -r requirements.txt
```

### Step 2: Install BankSec-Specific Dependencies

```bash
# Core authentication and security
pip install bcrypt

# GeoIP and WHOIS lookup (optional but recommended)
pip install ip2geotools
pip install python-whois

# PDF export functionality
pip install reportlab
```

### Step 3: Verify Installation

```bash
python -c "import bcrypt, customtkinter, sklearn; print('All dependencies installed successfully!')"
```

---

## 🗄️ Database Initialization

The user database is automatically created on first run. Default location: `QUILLBOT/database/users.db`

### Default Users

| Username | Password | Role | Security Question |
|----------|----------|------|-------------------|
| `admin` | `BankSec@2024` | Administrator | "What is your favorite banking system?" → "BankSec" |
| `analyst` | `Analyst@2024` | Security Analyst | "What is your security clearance level?" → "Level2" |

### Manual Database Initialization

```python
from src.user_database import UserDatabase

db = UserDatabase()
# Database is automatically initialized
print("Database initialized successfully!")
```

---

## 👥 User Management

### Adding New Users

```python
from src.user_database import UserDatabase

db = UserDatabase()
db.create_user(
    username="john.doe",
    password="SecurePass123!",
    security_question="What is your employee ID?",
    security_answer="EMP12345"
)
```

### Password Reset

1. Click "Forgot Password?" on login screen
2. Enter username
3. Answer security question
4. Set new password

### Account Lockout

- **Failed Attempts**: 5 maximum
- **Lockout Duration**: 15 minutes
- **Auto-unlock**: After lockout period expires

---

## ⚙️ Configuration

### Banking Theme Colors

Edit `config.yaml` under `banksec.theme`:

```yaml
banksec:
  theme:
    primary_bg: "#0f1c2e"      # Dark navy
    secondary_bg: "#1a202c"    # Charcoal
    accent: "#2b6cb0"          # Corporate blue
    alert_red: "#e53e3e"       # Alert red
    alert_green: "#38a169"     # Success green
```

### Risk Scoring Thresholds

```yaml
banksec:
  risk_scoring:
    critical_threshold: 90     # 90-100: CRITICAL
    high_threshold: 70         # 70-89: HIGH
    medium_threshold: 40       # 40-69: MEDIUM
    auto_popup_confidence: 0.95  # Auto-open forensic panel
```

### Critical Banking Ports

```yaml
banksec:
  critical_ports:
    - 22      # SSH
    - 443     # HTTPS
    - 1433    # MS SQL Server
    - 3306    # MySQL
    - 5432    # PostgreSQL
    - 1521    # Oracle
    - 27017   # MongoDB
```

---

## 🚀 Running the System

### Standard Launch

```bash
cd QUILLBOT
python main_with_simulator.py
```

### Launch Sequence

1. **Authentication Window** appears
2. Enter credentials (default: `admin` / `BankSec@2024`)
3. Click "Login"
4. **Main Dashboard** loads with real-time monitoring

### Logout

- Click "Logout" button in top-right corner
- Confirm logout
- Returns to login screen

---

## ✨ Features Overview

### 1. Enterprise Authentication
- ✅ Secure login with bcrypt password hashing
- ✅ Account lockout after 5 failed attempts
- ✅ Password reset with security questions
- ✅ Session management
- ✅ Login audit logging (`logs/login_audit.log`)

### 2. Real-Time Monitoring Dashboard
- ✅ Live packet feed with color-coded alerts
- ✅ Real-time metrics (packets, intrusions, throughput)
- ✅ Animated charts (traffic over time)
- ✅ Banking-themed UI with corporate colors
- ✅ User info display and logout button

### 3. Forensic Analysis Panel
- ✅ Double-click any packet to view details
- ✅ Auto-popup for high-confidence intrusions (≥95%)
- ✅ 8 detailed sections:
  - Flow Identification
  - Network Information
  - Traffic Characteristics
  - Threat Intelligence (with risk scoring)
  - Geolocation & WHOIS
  - Payload Preview (simulated)
  - Recommended Actions
  - Export & Actions

### 4. Banking-Specific Intelligence
- ✅ Risk scoring (0-100 scale)
- ✅ Banking context tags (e.g., "Core Banking Database Exploit")
- ✅ Critical port detection
- ✅ High-risk country identification
- ✅ Business impact assessment

### 5. Export Capabilities
- ✅ Export to PDF (comprehensive report)
- ✅ Export to CSV (data analysis)
- ✅ Copy to clipboard (quick sharing)
- ✅ Block IP action (simulated, logged)

---

## 🧪 Testing Checklist

### Authentication System Tests

#### Test 1: Successful Login
- [ ] Launch application
- [ ] Enter valid credentials (`admin` / `BankSec@2024`)
- [ ] Click "Login"
- [ ] **Expected**: Dashboard loads, user info shows "👤 admin"

#### Test 2: Failed Login
- [ ] Enter invalid password
- [ ] Click "Login"
- [ ] **Expected**: Error message "Invalid username or password"

#### Test 3: Account Lockout
- [ ] Enter wrong password 5 times
- [ ] **Expected**: Account locked for 15 minutes
- [ ] Try logging in again
- [ ] **Expected**: "Account is locked" message

#### Test 4: Password Reset
- [ ] Click "Forgot Password?"
- [ ] Enter username: `admin`
- [ ] Answer security question: "BankSec"
- [ ] Set new password
- [ ] **Expected**: Password reset successful
- [ ] Login with new password
- [ ] **Expected**: Login successful

#### Test 5: Logout
- [ ] Click "Logout" button
- [ ] Confirm logout
- [ ] **Expected**: Returns to login screen

---

### Dashboard Tests

#### Test 6: Real-Time Metrics
- [ ] Observe metrics cards updating
- [ ] **Expected**:
  - Total Packets increasing
  - Intrusions ~30% of total
  - Normal ~70% of total
  - Throughput ~5 pps
  - Latency <50ms

#### Test 7: Packet Feed
- [ ] Observe packet feed scrolling
- [ ] **Expected**:
  - Green entries for normal traffic
  - Red entries for intrusions
  - Confidence scores displayed
  - Attack types shown

#### Test 8: Charts
- [ ] Observe real-time charts
- [ ] **Expected**:
  - Green line (normal traffic) updating
  - Red line (intrusion rate) updating
  - Auto-scaling Y-axis

---

### Forensic Analysis Tests

#### Test 9: Manual Forensic Panel
- [ ] Double-click any packet in feed
- [ ] **Expected**: Forensic analysis panel opens
- [ ] Verify all 8 sections display data
- [ ] **Expected**: Risk score, banking context, recommendations shown

#### Test 10: Auto-Popup for High-Risk
- [ ] Wait for high-confidence intrusion (≥95%)
- [ ] **Expected**:
  - Forensic panel auto-opens
  - Alert sound plays
  - Panel shows CRITICAL or HIGH risk level

#### Test 11: Export to PDF
- [ ] Open forensic panel
- [ ] Click "📄 Export to PDF"
- [ ] Choose save location
- [ ] **Expected**: PDF file created with all sections

#### Test 12: Export to CSV
- [ ] Open forensic panel
- [ ] Click "📊 Export to CSV"
- [ ] Choose save location
- [ ] **Expected**: CSV file created with field-value pairs

#### Test 13: Copy to Clipboard
- [ ] Open forensic panel
- [ ] Click "📋 Copy to Clipboard"
- [ ] **Expected**: Success message
- [ ] Paste into text editor
- [ ] **Expected**: Formatted analysis text

#### Test 14: Block IP
- [ ] Open forensic panel
- [ ] Click "🚫 Block Source IP"
- [ ] **Expected**:
  - Confirmation dialog
  - Entry added to `logs/blocked_ips.log`

---

### Banking Intelligence Tests

#### Test 15: Risk Scoring
- [ ] Open forensic panel for intrusion
- [ ] Check "Threat Intelligence" section
- [ ] **Expected**: Risk score 0-100 with level (CRITICAL/HIGH/MEDIUM/LOW)

#### Test 16: Banking Context Tags
- [ ] Open forensic panel
- [ ] Check "Banking Context" field
- [ ] **Expected**: Banking-specific labels like:
  - "Core Banking Database Exploit Attempt"
  - "Payment Gateway Exploit Attempt"
  - "SWIFT Network Intrusion"

#### Test 17: GeoIP Lookup
- [ ] Open forensic panel
- [ ] Check "Geolocation & WHOIS" section
- [ ] **Expected**:
  - Country, region, city displayed
  - High-risk flag if applicable
  - Organization/ISP info

#### Test 18: Recommended Actions
- [ ] Open forensic panel for intrusion
- [ ] Check "Recommended Actions" section
- [ ] **Expected**:
  - Attack-specific mitigation steps
  - Escalation procedures for critical threats

---

## 🔧 Troubleshooting

### Issue: Login window doesn't appear

**Solution**:
```bash
# Check if auth_system.py exists
ls src/auth_system.py

# Verify dependencies
pip install customtkinter bcrypt
```

### Issue: "reportlab not installed" error

**Solution**:
```bash
pip install reportlab
```

### Issue: GeoIP lookups fail

**Solution**:
```bash
# Install GeoIP library
pip install ip2geotools

# Or use alternative
pip install geoip2
```

### Issue: Database locked error

**Solution**:
```bash
# Close all instances of the application
# Delete database file (will recreate with defaults)
rm database/users.db
```

### Issue: Charts not updating

**Solution**:
- Check if matplotlib is installed: `pip install matplotlib`
- Restart the application
- Check logs: `logs/quillbot.log`

### Issue: Audio alerts not working

**Solution**:
- Windows: `winsound` is built-in, should work automatically
- Linux/Mac: Audio alerts may not work (Windows-specific)

---

## 📊 Log Files

| Log File | Purpose |
|----------|---------|
| `logs/login_audit.log` | Authentication attempts and sessions |
| `logs/nids_log.txt` | Intrusion detection predictions |
| `logs/quillbot.log` | System operations and errors |
| `logs/blocked_ips.log` | IP blocking actions |

---

## 🔐 Security Best Practices

1. **Change Default Passwords**: Immediately change default user passwords
2. **Regular Backups**: Backup `database/users.db` regularly
3. **Audit Logs**: Review `login_audit.log` for suspicious activity
4. **Session Timeout**: Configure in `config.yaml` (default: 60 minutes)
5. **Network Isolation**: Run on isolated SOC network
6. **Access Control**: Limit physical access to system

---

## 📞 Support

For issues or questions:
- Check logs in `logs/` directory
- Review this documentation
- Contact BankSec NIDS support team

---

## 🎯 Quick Start Summary

```bash
# 1. Install dependencies
pip install bcrypt ip2geotools python-whois reportlab

# 2. Run the system
cd QUILLBOT
python main_with_simulator.py

# 3. Login
Username: admin
Password: BankSec@2024

# 4. Monitor and analyze
- View real-time dashboard
- Double-click packets for forensic analysis
- Export reports as needed
```

---

**BankSec NIDS v3.0 - Enterprise Security for Banking Infrastructure** 🏦🔒


