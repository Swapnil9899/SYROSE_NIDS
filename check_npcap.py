"""
Npcap Installation Checker and Guide

This script checks if Npcap is installed and provides installation instructions.
Npcap is required for packet capture on Windows.

Author: QUILLBOT Development Team
Version: 1.0.0
"""

import sys
import os
import platform


def check_npcap_installed():
    """Check if Npcap is installed on Windows."""
    if platform.system() != "Windows":
        print("✓ Not on Windows - Npcap not required")
        return True
    
    # Check for Npcap installation
    npcap_paths = [
        r"C:\Windows\System32\Npcap",
        r"C:\Windows\SysWOW64\Npcap",
        r"C:\Program Files\Npcap"
    ]
    
    for path in npcap_paths:
        if os.path.exists(path):
            print(f"✓ Npcap found at: {path}")
            return True
    
    return False


def print_installation_guide():
    """Print Npcap installation guide."""
    print("\n" + "=" * 80)
    print("NPCAP NOT INSTALLED - PACKET CAPTURE WILL NOT WORK!")
    print("=" * 80)
    print("\nNpcap is required for packet capture on Windows.")
    print("Without it, the QUILLBOT NIDS system cannot capture network traffic.\n")
    
    print("📥 INSTALLATION STEPS:")
    print("-" * 80)
    print("1. Download Npcap from: https://npcap.com/#download")
    print("   (Direct link: https://npcap.com/dist/npcap-1.79.exe)")
    print()
    print("2. Run the installer as Administrator")
    print()
    print("3. During installation, make sure to check:")
    print("   ✓ Install Npcap in WinPcap API-compatible Mode")
    print("   ✓ Support raw 802.11 traffic (optional)")
    print()
    print("4. Restart your computer after installation")
    print()
    print("5. Run this script again to verify installation:")
    print("   python check_npcap.py")
    print("-" * 80)
    
    print("\n⚠️  ALTERNATIVE: Use Simulated Traffic Mode")
    print("-" * 80)
    print("If you want to test the system without capturing real packets,")
    print("you can use the simulated traffic generator:")
    print()
    print("   python simulate_traffic.py")
    print()
    print("This will generate synthetic network packets for testing purposes.")
    print("=" * 80)


def main():
    """Main function."""
    print("\n🔍 Checking for Npcap installation...\n")
    
    if check_npcap_installed():
        print("\n✅ Npcap is installed!")
        print("\nYou can now run the QUILLBOT NIDS system:")
        print("   python main.py")
        print("\n⚠️  IMPORTANT: Run as Administrator for packet capture!")
        print("   Right-click Command Prompt/PowerShell → 'Run as Administrator'")
        return 0
    else:
        print("\n❌ Npcap is NOT installed!")
        print_installation_guide()
        return 1


if __name__ == '__main__':
    sys.exit(main())

