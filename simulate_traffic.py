"""
Network Traffic Simulator for QUILLBOT NIDS

This script simulates network traffic for testing the NIDS system
when real packet capture is not available (e.g., Npcap not installed).

Author: QUILLBOT Development Team
Version: 1.0.0
"""

import sys
import os
import time
import random
import threading
from datetime import datetime
from typing import Dict, Any

# Suppress scapy warnings about Npcap
import warnings
warnings.filterwarnings('ignore')

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set environment variable to suppress scapy Npcap warnings
os.environ['SCAPY_USE_PCAPDNET'] = '0'

try:
    import customtkinter as ctk
    from predict_intrusion_v2 import UnifiedIntrusionPredictor, PredictionLogger
    from gui_dashboard import NIDSDashboard
    from config_loader import get_config, get_active_dataset
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all dependencies are installed:")
    print("  pip install customtkinter matplotlib numpy pandas scikit-learn pyyaml")
    sys.exit(1)


class TrafficSimulator:
    """Simulates network traffic for testing."""
    
    def __init__(self, packets_per_second: int = 5):
        """
        Initialize traffic simulator.
        
        Args:
            packets_per_second: Number of packets to generate per second
        """
        self.packets_per_second = packets_per_second
        self.is_running = False
        self.packet_count = 0
        self.intrusion_count = 0
        self.normal_count = 0
        self.dashboard = None
        self.predictor = None
        self.logger_obj = None
        self.start_time = None
        self.lock = threading.Lock()
        
        # Load configuration
        self.config = get_config()
        self.active_dataset = get_active_dataset()
        
        print("=" * 80)
        print("QUILLBOT NIDS - Traffic Simulator Mode")
        print(f"Active Dataset: {self.active_dataset}")
        print("=" * 80)
    
    def generate_packet(self) -> Dict[str, Any]:
        """Generate a simulated network packet."""
        # Random IP addresses
        src_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        dst_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        
        # Random ports
        src_port = random.randint(1024, 65535)
        dst_port = random.choice([80, 443, 22, 21, 25, 53, 3389, 8080, random.randint(1024, 65535)])
        
        # Random protocol
        protocol = random.choice(['tcp', 'udp', 'icmp'])
        
        # Random packet characteristics
        packet = {
            'timestamp': datetime.now().isoformat(),
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'src_port': src_port,
            'dst_port': dst_port,
            'protocol': protocol,
            'packet_length': random.randint(64, 1500),
            'tcp_flags': random.randint(0, 63) if protocol == 'tcp' else 0,
            'payload_size': random.randint(0, 1400)
        }
        
        return packet
    
    def initialize_components(self) -> bool:
        """Initialize predictor and logger."""
        try:
            print("\nInitializing components...")
            
            # Initialize predictor
            model_path = os.path.join(os.path.dirname(__file__), 'model', 'nids_model.pkl')
            scaler_path = os.path.join(os.path.dirname(__file__), 'model', 'scaler.pkl')
            encoder_path = os.path.join(os.path.dirname(__file__), 'model', 'encoder.pkl')
            
            if not os.path.exists(model_path):
                print(f"❌ Model file not found: {model_path}")
                print("Please train the model first: python src/train_model_v2.py")
                return False
            
            self.predictor = UnifiedIntrusionPredictor(model_path, scaler_path, encoder_path)
            print(f"✓ Predictor initialized for {self.active_dataset}")
            
            # Initialize logger
            log_path = os.path.join(os.path.dirname(__file__), 'logs', 'nids_log.txt')
            self.logger_obj = PredictionLogger(log_path)
            print(f"✓ Logger initialized: {log_path}")
            
            return True
        except Exception as e:
            print(f"❌ Error initializing components: {e}")
            return False
    
    def _generate_traffic(self) -> None:
        """Generate simulated traffic in a separate thread."""
        print(f"\n🚀 Generating {self.packets_per_second} packets per second...")
        print("Press Ctrl+C or close the GUI window to stop.\n")
        
        sleep_time = 1.0 / self.packets_per_second
        
        while self.is_running:
            try:
                # Generate packet
                packet = self.generate_packet()
                
                # Make prediction
                is_intrusion, confidence, attack_type = self.predictor.predict(packet)
                
                # Log prediction
                packet['confidence'] = confidence
                packet['attack_type'] = attack_type
                self.logger_obj.log_prediction(packet, is_intrusion, confidence, attack_type)
                
                # Update statistics
                with self.lock:
                    self.packet_count += 1
                    if is_intrusion:
                        self.intrusion_count += 1
                    else:
                        self.normal_count += 1
                
                # Update dashboard
                if self.dashboard:
                    self.dashboard.add_packet_alert(packet, is_intrusion)
                
                time.sleep(sleep_time)
            except Exception as e:
                print(f"Error generating packet: {e}")
                time.sleep(0.1)
    
    def _update_dashboard_metrics(self) -> None:
        """Update dashboard metrics periodically."""
        while self.is_running:
            try:
                if self.dashboard:
                    with self.lock:
                        elapsed_time = time.time() - self.start_time if self.start_time else 0
                        throughput = self.packet_count / elapsed_time if elapsed_time > 0 else 0
                        
                        metrics = {
                            'total_packets': self.packet_count,
                            'intrusions': self.intrusion_count,
                            'normal': self.normal_count,
                            'throughput': throughput
                        }
                    
                    self.dashboard.update_metrics(metrics)
                
                time.sleep(0.5)
            except Exception as e:
                print(f"Error updating dashboard: {e}")
    
    def start(self) -> None:
        """Start the traffic simulator."""
        try:
            if not self.initialize_components():
                return
            
            self.is_running = True
            self.start_time = time.time()
            
            # Start traffic generation thread
            traffic_thread = threading.Thread(target=self._generate_traffic, daemon=True)
            traffic_thread.start()
            
            # Start dashboard update thread
            update_thread = threading.Thread(target=self._update_dashboard_metrics, daemon=True)
            update_thread.start()
            
            # Initialize and run dashboard
            print("\n✓ Initializing GUI dashboard...")
            root = ctk.CTk()
            self.dashboard = NIDSDashboard(root)
            
            print("✓ System started successfully!")
            print("=" * 80)
            
            # Run dashboard (blocking)
            self.dashboard.run()
        except KeyboardInterrupt:
            print("\n\nStopping simulator...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.stop()
    
    def stop(self) -> None:
        """Stop the traffic simulator."""
        self.is_running = False
        
        print("\n" + "=" * 80)
        print("SIMULATION SUMMARY")
        print("=" * 80)
        print(f"Total Packets: {self.packet_count}")
        print(f"Intrusions: {self.intrusion_count}")
        print(f"Normal: {self.normal_count}")
        
        if self.packet_count > 0:
            detection_rate = (self.intrusion_count / self.packet_count) * 100
            print(f"Detection Rate: {detection_rate:.2f}%")
        
        elapsed = time.time() - self.start_time if self.start_time else 0
        if elapsed > 0:
            print(f"Throughput: {self.packet_count / elapsed:.2f} packets/sec")
        
        print("=" * 80)


def main():
    """Main function."""
    print("\n" + "=" * 80)
    print("QUILLBOT NIDS - SIMULATED TRAFFIC MODE")
    print("=" * 80)
    print("\n⚠️  This mode generates SIMULATED network traffic for testing.")
    print("For real packet capture, install Npcap and run: python main.py\n")
    
    # Create and start simulator
    simulator = TrafficSimulator(packets_per_second=5)
    simulator.start()


if __name__ == '__main__':
    main()

