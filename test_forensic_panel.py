"""
Test script for Packet Forensic Analysis Panel
Tests the complete workflow of opening and displaying forensic data.
"""

import sys
sys.path.insert(0, 'src')

import customtkinter as ctk
from packet_details_panel import PacketDetailsPanel
from datetime import datetime

# Create sample packet data (simulating a high-confidence intrusion)
sample_packet = {
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'src_ip': '192.168.1.100',
    'dst_ip': '10.0.0.50',
    'src_port': 54321,
    'dst_port': 22,
    'protocol': 'TCP',
    'packet_size': 1500,
    'ttl': 64,
    'flags': 'SYN',
    'duration': 0.5,
    'src_bytes': 2048,
    'dst_bytes': 1024,
    'src_packets': 10,
    'dst_packets': 8,
    'prediction': 'Intrusion',
    'confidence': 98.5,
    'attack_type': 'Exploits',
    'severity': 'CRITICAL',
    'payload': b'GET /admin HTTP/1.1\r\nHost: target.com\r\n\r\n',
    # Additional features for ML model
    'sbytes': 2048,
    'dbytes': 1024,
    'sttl': 64,
    'dttl': 64,
    'sloss': 0,
    'dloss': 0,
    'service': 'ssh',
    'sload': 100.5,
    'dload': 50.2,
    'spkts': 10,
    'dpkts': 8,
    'swin': 65535,
    'dwin': 32768,
    'stcpb': 1000000,
    'dtcpb': 500000,
    'smeansz': 204.8,
    'dmeansz': 128.0,
    'trans_depth': 1,
    'res_bdy_len': 0,
    'sjit': 0.1,
    'djit': 0.2,
    'stime': 1234567890.0,
    'ltime': 1234567890.5,
    'sintpkt': 0.05,
    'dintpkt': 0.06,
    'tcprtt': 0.01,
    'synack': 0.005,
    'ackdat': 0.003,
    'is_sm_ips_ports': 0,
    'ct_state_ttl': 1,
    'ct_flw_http_mthd': 0,
    'is_ftp_login': 0,
    'ct_ftp_cmd': 0,
    'ct_srv_src': 5,
    'ct_srv_dst': 3,
    'ct_dst_ltm': 2,
    'ct_src_ltm': 4,
    'ct_src_dport_ltm': 1,
    'ct_dst_sport_ltm': 1,
    'ct_dst_src_ltm': 2
}

def test_forensic_panel():
    """Test the forensic panel with sample data."""
    print("🔍 Testing Packet Forensic Analysis Panel...")
    print(f"📦 Sample packet: {sample_packet['src_ip']}:{sample_packet['src_port']} → {sample_packet['dst_ip']}:{sample_packet['dst_port']}")
    print(f"🚨 Attack type: {sample_packet['attack_type']} (Confidence: {sample_packet['confidence']}%)")
    
    # Create root window
    root = ctk.CTk()
    root.title("Test - BankSec NIDS")
    root.geometry("800x600")
    
    # Create a button to open forensic panel
    def open_panel():
        try:
            print("\n✅ Opening forensic panel...")
            panel = PacketDetailsPanel(sample_packet, parent=root)
            panel.show()
            print("✅ Forensic panel opened successfully!")
            print("✅ All 8 sections should be visible:")
            print("   1. Flow Identification")
            print("   2. Network Information")
            print("   3. Traffic Characteristics")
            print("   4. Threat Intelligence")
            print("   5. Banking Context & Risk Scoring")
            print("   6. GeoIP & WHOIS Information")
            print("   7. Packet Payload Analysis")
            print("   8. Recommended Actions")
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    # Create UI
    label = ctk.CTkLabel(root, text="Click button to test forensic panel", font=("Arial", 16))
    label.pack(pady=20)
    
    button = ctk.CTkButton(root, text="Open Forensic Panel", command=open_panel, font=("Arial", 14))
    button.pack(pady=10)
    
    info_label = ctk.CTkLabel(root, text=f"Test Packet: {sample_packet['src_ip']} → {sample_packet['dst_ip']}\nAttack: {sample_packet['attack_type']} ({sample_packet['confidence']}%)", font=("Arial", 12))
    info_label.pack(pady=10)
    
    print("\n✅ Test window created. Click the button to open forensic panel.")
    print("📝 Check that all sections display correctly.")
    print("📝 Test Export to PDF, Export to CSV, and Copy to Clipboard buttons.")
    
    root.mainloop()

if __name__ == "__main__":
    test_forensic_panel()

