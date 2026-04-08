"""
BankSec NIDS - Main Application with Traffic Simulator
Enterprise-grade Network Intrusion Detection System for Financial Institutions.
This version uses simulated traffic to avoid Scapy interface enumeration delays.

Author: BankSec NIDS Development Team
Version: 3.0.0 (Banking Edition)
"""

import sys
import os
import logging
import time
import threading
import queue
import random
from typing import Dict, Any

# Add src to path
sys.path.insert(0, 'src')

from predict_intrusion_v2 import UnifiedIntrusionPredictor, PredictionLogger
from preprocess_features_v2 import UnifiedFeatureExtractor
from gui_dashboard import NIDSDashboard
from config_loader import get_config, get_active_dataset
from auth_system import LoginWindow

# Configure logging
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'quillbot.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TrafficSimulator:
    """Simulates network traffic for testing."""
    
    def __init__(self, packet_queue: queue.Queue, packets_per_second: int = 5):
        self.packet_queue = packet_queue
        self.packets_per_second = packets_per_second
        self.is_running = False
        self.thread = None
        
    def start(self):
        """Start generating simulated traffic."""
        self.is_running = True
        self.thread = threading.Thread(target=self._generate_traffic, daemon=True)
        self.thread.start()
        logger.info(f"Traffic simulator started ({self.packets_per_second} packets/sec)")
        
    def stop(self):
        """Stop generating traffic."""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2)
        logger.info("Traffic simulator stopped")
        
    def _generate_traffic(self):
        """Generate simulated network packets."""
        while self.is_running:
            try:
                # Generate 70% normal, 30% attack traffic
                packet_type = 'normal' if random.random() < 0.7 else 'attack'
                packet = self._create_packet(packet_type)
                self.packet_queue.put(packet)
                time.sleep(1.0 / self.packets_per_second)
            except Exception as e:
                logger.error(f"Error generating traffic: {e}")
                
    def _create_packet(self, packet_type: str) -> Dict[str, Any]:
        """Create a simulated packet with UNSW-NB15 features."""
        if packet_type == 'normal':
            # Normal traffic - matches training data
            packet_length = random.choice([64, 128, 256, 512, 800, 1500])
            return {
                'src_ip': f'192.168.1.{random.randint(100, 200)}',
                'dst_ip': f'10.0.0.{random.randint(1, 10)}',
                'src_port': random.randint(1024, 65535),
                'dst_port': random.choice([80, 443, 22, 53, 25]),
                'protocol': random.choice(['tcp', 'udp']),
                'packet_length': packet_length,
                'timestamp': time.time(),
                # UNSW-NB15 features for normal traffic
                'Spkts': 1,  # Single packet
                'ct_state_ttl': 1,
                'ct_srv_src': 1,
                'ct_srv_dst': 1,
                'ct_dst_ltm': 1,
                'ct_src_ltm': 1,
                'ct_src_dport_ltm': 1,
                'ct_dst_sport_ltm': 1,
                'ct_dst_src_ltm': 1,
                'is_sm_ips_ports': 0
            }
        else:
            # Attack traffic - DoS, Scan, or Exploit
            attack_subtype = random.choice(['dos', 'scan', 'exploit'])
            if attack_subtype == 'dos':
                # DoS: Very large packets OR many small packets
                dos_type = random.choice(['flood', 'large'])
                if dos_type == 'flood':
                    packet_length = random.randint(10, 100)  # Very small
                    spkts = random.randint(100, 1000)  # Many packets
                else:
                    packet_length = random.randint(5000, 65535)  # Very large
                    spkts = random.randint(10, 50)

                return {
                    'src_ip': f'192.168.1.{random.randint(100, 200)}',
                    'dst_ip': f'10.0.0.{random.randint(1, 10)}',
                    'src_port': random.randint(1024, 65535),
                    'dst_port': random.choice([80, 443]),
                    'protocol': 'tcp',
                    'packet_length': packet_length,
                    'timestamp': time.time(),
                    # UNSW-NB15 features for DoS
                    'Spkts': spkts,  # KEY: Many packets
                    'ct_state_ttl': random.randint(50, 200),  # KEY: High connection count
                    'ct_srv_src': random.randint(50, 200),
                    'ct_srv_dst': random.randint(50, 200),
                    'ct_dst_ltm': random.randint(50, 200),
                    'ct_src_ltm': random.randint(50, 200),
                    'ct_src_dport_ltm': random.randint(50, 200),
                    'ct_dst_sport_ltm': random.randint(50, 200),
                    'ct_dst_src_ltm': random.randint(50, 200),
                    'is_sm_ips_ports': 1  # KEY: Same IPs/ports
                }
            elif attack_subtype == 'scan':
                # Reconnaissance: Random ports
                return {
                    'src_ip': f'192.168.1.{random.randint(100, 200)}',
                    'dst_ip': f'10.0.0.{random.randint(1, 10)}',
                    'src_port': random.randint(1024, 65535),
                    'dst_port': random.randint(1, 65535),  # Random port scanning
                    'protocol': 'tcp',
                    'packet_length': 64,
                    'timestamp': time.time(),
                    # UNSW-NB15 features for reconnaissance
                    'Spkts': random.randint(10, 100),
                    'ct_state_ttl': random.randint(20, 100),
                    'ct_srv_src': random.randint(20, 100),
                    'ct_srv_dst': random.randint(20, 100),
                    'ct_dst_ltm': random.randint(20, 100),
                    'ct_src_ltm': random.randint(20, 100),
                    'ct_src_dport_ltm': random.randint(20, 100),
                    'ct_dst_sport_ltm': random.randint(20, 100),
                    'ct_dst_src_ltm': random.randint(20, 100),
                    'is_sm_ips_ports': 0
                }
            else:  # exploit
                # Exploits: Suspicious ports
                return {
                    'src_ip': f'192.168.1.{random.randint(100, 200)}',
                    'dst_ip': f'10.0.0.{random.randint(1, 10)}',
                    'src_port': random.randint(1024, 65535),
                    'dst_port': random.choice([21, 23, 3389, 445]),  # Suspicious services
                    'protocol': 'tcp',
                    'packet_length': random.randint(500, 2000),
                    'timestamp': time.time(),
                    # UNSW-NB15 features for exploits
                    'Spkts': random.randint(5, 20),
                    'ct_state_ttl': random.randint(10, 50),
                    'ct_srv_src': random.randint(10, 50),
                    'ct_srv_dst': random.randint(10, 50),
                    'ct_dst_ltm': random.randint(10, 50),
                    'ct_src_ltm': random.randint(10, 50),
                    'ct_src_dport_ltm': random.randint(10, 50),
                    'ct_dst_sport_ltm': random.randint(10, 50),
                    'ct_dst_src_ltm': random.randint(10, 50),
                    'is_sm_ips_ports': 0
                }


class BankSecSystemSimulated:
    """BankSec NIDS with simulated traffic."""

    def __init__(self, username: str = "admin", session_id: str = ""):
        self.config = get_config()
        self.dataset = get_active_dataset()
        self.packet_queue = queue.Queue(maxsize=1000)
        self.is_running = False

        # User session info
        self.username = username
        self.session_id = session_id

        # Components
        self.simulator = None
        self.predictor = None
        self.logger_component = None
        self.dashboard = None

        # Threads
        self.processing_thread = None
        
    def initialize(self) -> bool:
        """Initialize all components."""
        try:
            logger.info("=" * 80)
            logger.info("BankSec NIDS - Financial Network Security Platform v3.0 (Banking Edition)")
            logger.info(f"Active Dataset: {self.dataset}")
            logger.info(f"Logged in as: {self.username}")
            logger.info("=" * 80)
            logger.info("Initializing BankSec components...")
            
            # Initialize traffic simulator
            logger.info("Initializing traffic simulator...")
            self.simulator = TrafficSimulator(self.packet_queue, packets_per_second=5)
            logger.info("Traffic simulator initialized")
            
            # Initialize predictor
            logger.info(f"Initializing unified intrusion predictor for {self.dataset}...")
            model_path = 'model/nids_model.pkl'
            scaler_path = 'model/scaler.pkl'
            encoder_path = 'model/encoder.pkl'
            
            self.predictor = UnifiedIntrusionPredictor(
                model_path=model_path,
                scaler_path=scaler_path,
                encoder_path=encoder_path
            )
            logger.info(f"Unified intrusion predictor initialized for {self.dataset}")
            
            # Initialize prediction logger
            logger.info("Initializing prediction logger...")
            log_file = os.path.join(log_dir, 'nids_log.txt')
            self.logger_component = PredictionLogger(log_file)
            logger.info(f"Prediction logger initialized: {log_file}")
            
            logger.info("All components initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    def start(self):
        """Start the BankSec system."""
        try:
            logger.info("Starting BankSec system...")
            self.is_running = True

            # Start traffic simulator
            self.simulator.start()

            # Start packet processing thread
            logger.info("Starting packet processing thread...")
            self.processing_thread = threading.Thread(target=self._process_packets, daemon=True)
            self.processing_thread.start()
            logger.info("Packet processing thread started")

            # Start GUI dashboard with user info
            logger.info("Initializing BankSec GUI dashboard...")
            import customtkinter as ctk
            root = ctk.CTk()
            self.dashboard = NIDSDashboard(root, username=self.username, session_id=self.session_id)
            logger.info("GUI dashboard initialized")
            logger.info("BankSec system started successfully")
            logger.info("=" * 80)

            # Run GUI main loop
            self.dashboard.run()

        except Exception as e:
            logger.error(f"Error starting system: {e}")
            import traceback
            traceback.print_exc()
            self.stop()
            
    def _process_packets(self):
        """Process packets from the queue."""
        while self.is_running:
            try:
                # Get packet from queue (with timeout)
                try:
                    packet_data = self.packet_queue.get(timeout=0.1)
                except queue.Empty:
                    continue
                    
                # Extract features
                features = self.predictor.feature_extractor.extract_packet_features_unsw_nb15(packet_data)
                
                # Predict
                prediction, confidence, attack_type = self.predictor.predict(features)
                
                # Log prediction
                is_intrusion = (prediction == 'INTRUSION' or prediction == True or prediction == 1)
                self.logger_component.log_prediction(
                    packet_data=packet_data,
                    is_intrusion=is_intrusion,
                    confidence=confidence,
                    attack_type=attack_type
                )
                
                # Update dashboard
                if self.dashboard:
                    metrics = {
                        'total_packets': self.predictor.stats['total_predictions'],
                        'intrusions': self.predictor.stats['intrusions_detected'],
                        'normal': self.predictor.stats['normal_packets'],
                        'throughput': self.predictor.stats.get('throughput_pps', 0),
                        'detection_rate': self.predictor.stats['intrusion_rate'],
                        'avg_latency': self.predictor.stats['avg_latency_ms'],
                        'last_status': prediction
                    }
                    self.dashboard.update_metrics(metrics)

                    # Add confidence and attack_type to packet_data
                    packet_data['confidence'] = confidence
                    packet_data['attack_type'] = attack_type

                    # Add packet to feed
                    self.dashboard.add_packet_alert(
                        packet=packet_data,
                        is_intrusion=is_intrusion
                    )
                    
            except Exception as e:
                logger.error(f"Error processing packet: {e}")
                
    def stop(self):
        """Stop the BankSec system."""
        logger.info("Stopping BankSec system...")
        self.is_running = False

        if self.simulator:
            self.simulator.stop()

        logger.info("BankSec system stopped")


def main():
    """Main entry point with authentication."""
    logger.info("=" * 80)
    logger.info("BankSec NIDS - Financial Network Security Platform")
    logger.info("Enterprise-Grade Intrusion Detection for Banking Infrastructure")
    logger.info("=" * 80)

    # Global variables to store credentials
    authenticated_username = None
    authenticated_session_id = None

    def on_login_success(username: str, session_id: str):
        """Callback for successful login."""
        nonlocal authenticated_username, authenticated_session_id
        authenticated_username = username
        authenticated_session_id = session_id
        logger.info(f"User '{username}' authenticated successfully")

    try:
        # Show login window first
        logger.info("Launching authentication system...")
        import customtkinter as ctk

        login_window = LoginWindow(on_success_callback=on_login_success)
        login_window.run()

        # Check if authentication was successful
        if not authenticated_username or not authenticated_session_id:
            logger.info("Authentication cancelled or failed")
            return 0

        # Initialize system with authenticated user
        logger.info(f"Initializing BankSec system for user: {authenticated_username}")
        system = BankSecSystemSimulated(
            username=authenticated_username,
            session_id=authenticated_session_id
        )

        if not system.initialize():
            logger.error("Failed to initialize system")
            return 1

        # Start the system
        system.start()

    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Error in main: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())

