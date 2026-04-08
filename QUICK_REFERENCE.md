# BankSec NIDS - Quick Reference Card

## 🚀 Quick Start

```bash
cd QUILLBOT
python main_with_simulator.py
```

**Login**: `admin` / `BankSec@2024`

---

## 🔑 Default Users

| Username | Password | Security Question | Answer |
|----------|----------|-------------------|--------|
| admin | BankSec@2024 | What is your favorite banking system? | BankSec |
| analyst | Analyst@2024 | What is your security clearance level? | Level2 |

---

## 🎨 Key Features

### Authentication
- ✅ Secure login (bcrypt hashing)
- ✅ Account lockout (5 attempts, 15 min)
- ✅ Password reset with security questions
- ✅ Session management
- ✅ Logout button (top-right)

### Dashboard
- ✅ Real-time metrics (packets, intrusions, throughput)
- ✅ Live charts (green=normal, red=intrusions)
- ✅ Color-coded packet feed
- ✅ Banking-themed UI (navy, corporate blue)
- ✅ User info display

### Forensic Analysis
- ✅ **Double-click** any packet to view details
- ✅ **Auto-popup** for intrusions ≥95% confidence
- ✅ 8 detailed sections (flow, network, threat intel, geo, etc.)
- ✅ Risk scoring (0-100, CRITICAL/HIGH/MEDIUM/LOW)
- ✅ Banking context tags
- ✅ Export to PDF/CSV
- ✅ Copy to clipboard
- ✅ Block IP action

---

## 📊 Risk Levels

| Score | Level | Color | Action |
|-------|-------|-------|--------|
| 90-100 | CRITICAL | 🔴 Red | Immediate escalation |
| 70-89 | HIGH | 🟠 Orange | Urgent action required |
| 40-69 | MEDIUM | 🟡 Yellow | Monitor closely |
| 0-39 | LOW | 🟢 Green | Routine logging |

---

## 🔧 Critical Banking Ports

- **22** - SSH
- **443** - HTTPS
- **1433** - MS SQL Server
- **3306** - MySQL
- **5432** - PostgreSQL
- **1521** - Oracle Database
- **27017** - MongoDB
- **6379** - Redis
- **8080/8443** - HTTP/HTTPS Alternate

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `config.yaml` | System configuration |
| `database/users.db` | User credentials |
| `logs/login_audit.log` | Authentication log |
| `logs/nids_log.txt` | Intrusion detections |
| `logs/blocked_ips.log` | IP blocking actions |
| `model/nids_model.pkl` | Trained ML model |

---

## 🧪 Quick Test

1. **Login**: Use `admin` / `BankSec@2024`
2. **Observe**: Metrics updating, packets scrolling
3. **Double-click**: Any packet in feed → forensic panel opens
4. **Wait**: For high-confidence intrusion → auto-popup
5. **Export**: Click "📄 Export to PDF" in forensic panel
6. **Logout**: Click "Logout" button → returns to login

---

## 🆘 Troubleshooting

### Login window doesn't appear
```bash
pip install customtkinter bcrypt
```

### PDF export fails
```bash
pip install reportlab
```

### GeoIP lookup fails
```bash
pip install ip2geotools python-whois
```

### Database locked
```bash
# Close all instances, then:
rm database/users.db  # Will recreate with defaults
```

---

## 📞 Support

- **Documentation**: `BANKSEC_SETUP.md` (full guide)
- **Summary**: `BANKSEC_TRANSFORMATION_SUMMARY.md`
- **Logs**: Check `logs/` directory
- **Config**: Edit `config.yaml`

---

## 🎯 Attack Types Detected

1. **Normal** - Legitimate traffic
2. **Generic** - Generic attack patterns
3. **Exploits** - Vulnerability exploitation
4. **Fuzzers** - Fuzzing attacks
5. **DoS** - Denial of Service
6. **Reconnaissance** - Network scanning
7. **Analysis** - Traffic analysis
8. **Backdoor** - Backdoor access
9. **Shellcode** - Code injection
10. **Worms** - Worm propagation

---

## 🔐 Security Best Practices

1. ✅ Change default passwords immediately
2. ✅ Review `login_audit.log` regularly
3. ✅ Backup `database/users.db` daily
4. ✅ Monitor `blocked_ips.log` for patterns
5. ✅ Run on isolated SOC network
6. ✅ Limit physical access to system

---

**BankSec NIDS v3.0** 🏦🔒

