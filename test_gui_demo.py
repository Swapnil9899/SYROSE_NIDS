#!/usr/bin/env python3
"""
QUILLBOT NIDS - Modern GUI Demo and Test Script

This script demonstrates the new modern GUI dashboard with simulated data.
Run this to see the dashboard in action with realistic packet data.

Usage:
    python test_gui_demo.py
"""

import customtkinter as ctk
import threading
import time
import random
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, 'src')

from gui_dashboard import NIDSDashboard


def run_demo():
    """Run the GUI demo with simulated NIDS data."""
    
    print("=" * 70)
    print("QUILLBOT NIDS - Modern GUI Dashboard Demo")
    print("=" * 70)
    print("\nInitializing dashboard...")
    
    # Create root window
    root = ctk.CTk()
    
    # Create dashboard
    dashboard = NIDSDashboard(root)
    
    print("Dashboard initialized successfully!")
    print("\nStarting data simulation...")
    print("The dashboard will display simulated network traffic for 5 minutes.")
    print("\nFeatures to observe:")
    print("  • Real-time metrics updating")
    print("  • Green/Red alert indicators")
    print("  • Live packet feed with color coding")
    print("  • Real-time traffic charts")
    print("  • Attack distribution pie chart")
    print("\nClose the window to exit.\n")
    
    # Simulate NIDS data
    def simulate_nids_data():
        """Simulate realistic NIDS data."""
        packet_count = 0
        intrusion_count = 0
        normal_count = 0
        start_time = time.time()
        
        for i in range(300):  # Run for 5 minutes
            if not dashboard.is_running:
                break
            
            time.sleep(1)
            
            # Simulate packet generation (50-200 packets per second)
            packets_this_second = random.randint(50, 200)
            packet_count += packets_this_second
            
            # Simulate intrusions (5% chance per packet)
            intrusions_this_second = sum(1 for _ in range(packets_this_second) 
                                        if random.random() < 0.05)
            normal_this_second = packets_this_second - intrusions_this_second
            
            intrusion_count += intrusions_this_second
            normal_count += normal_this_second
            
            # Update metrics
            uptime = time.time() - start_time
            metrics = {
                'total_packets': packet_count,
                'intrusions': intrusion_count,
                'normal': normal_count,
                'throughput': packets_this_second,
                'avg_latency': random.uniform(10, 100),
                'uptime': uptime
            }
            dashboard.update_metrics(metrics)
            
            # Add packet alerts
            for _ in range(min(packets_this_second, 10)):  # Show max 10 per second
                is_intrusion = random.random() < 0.05
                
                packet_info = {
                    'src_ip': f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}",
                    'dst_ip': f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}",
                    'protocol': random.choice(['tcp', 'udp', 'icmp']),
                    'src_port': random.randint(1024, 65535),
                    'dst_port': random.choice([80, 443, 22, 3306, 8080, 8443, 5432]),
                    'confidence': random.uniform(0.7, 1.0),
                    'packet_length': random.randint(64, 1500)
                }
                
                dashboard.add_packet_alert(packet_info, is_intrusion)
            
            # Print progress
            if (i + 1) % 30 == 0:
                print(f"[{i+1}s] Packets: {packet_count} | "
                      f"Intrusions: {intrusion_count} | "
                      f"Normal: {normal_count} | "
                      f"Throughput: {packets_this_second} pps")
    
    # Start simulation in background thread
    sim_thread = threading.Thread(target=simulate_nids_data, daemon=True)
    sim_thread.start()
    
    # Run dashboard
    try:
        dashboard.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
        dashboard._exit_app()
    except Exception as e:
        print(f"Error: {e}")
        dashboard._exit_app()


def main():
    """Main entry point."""
    try:
        run_demo()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

