"""
Quick test to verify Npcap is working with Scapy
"""
import sys
import os

print("=" * 60)
print("NPCAP + SCAPY TEST")
print("=" * 60)

# Test 1: Check if wpcap.dll exists
print("\n[1/5] Checking for Npcap DLL files...")
npcap_dll = r"C:\Windows\System32\Npcap\wpcap.dll"
winpcap_dll = r"C:\Windows\System32\wpcap.dll"

if os.path.exists(npcap_dll):
    print(f"  ✓ Found: {npcap_dll}")
else:
    print(f"  ✗ Missing: {npcap_dll}")

if os.path.exists(winpcap_dll):
    print(f"  ✓ Found: {winpcap_dll} (WinPcap compatibility)")
else:
    print(f"  ✗ Missing: {winpcap_dll}")

# Test 2: Import Scapy (with timeout protection)
print("\n[2/5] Importing Scapy...")
try:
    import scapy
    print("  ✓ Scapy imported successfully")
except Exception as e:
    print(f"  ✗ Failed to import Scapy: {e}")
    sys.exit(1)

# Test 3: Check Scapy configuration
print("\n[3/5] Checking Scapy configuration...")
try:
    from scapy.all import conf
    print(f"  ✓ Default interface: {conf.iface}")
except Exception as e:
    print(f"  ✗ Failed to get Scapy config: {e}")

# Test 4: List available interfaces
print("\n[4/5] Listing network interfaces...")
try:
    from scapy.all import get_if_list
    interfaces = get_if_list()
    print(f"  ✓ Found {len(interfaces)} interfaces")
    if len(interfaces) > 0:
        print(f"  First interface: {interfaces[0]}")
except Exception as e:
    print(f"  ✗ Failed to list interfaces: {e}")

# Test 5: Try a simple packet capture (1 packet only)
print("\n[5/5] Testing packet capture (1 packet, 5 second timeout)...")
try:
    from scapy.all import sniff
    print("  Starting capture...")
    packets = sniff(count=1, timeout=5)
    if len(packets) > 0:
        print(f"  ✓ Successfully captured {len(packets)} packet(s)")
        print(f"  Packet summary: {packets[0].summary()}")
    else:
        print("  ⚠ No packets captured (timeout)")
except Exception as e:
    print(f"  ✗ Packet capture failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)

