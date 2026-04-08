"""
QUILLBOT NIDS - Main Orchestration Script

This is the main entry point for the QUILLBOT Network Intrusion Detection System.
Integrates all modules: packet capture, feature extraction, ML prediction, and visualization.

Author: QUILLBOT Development Team
Version: 2.0.0 (UNSW-NB15 Integration)
"""

import logging
import sys
import os
import time
import threading
import customtkinter as ctk
from datetime import datetime
from typing import Optional

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from packet_sniffer import PacketSniffer
from predict_intrusion_v2 import UnifiedIntrusionPredictor, PredictionLogger
from preprocess_features_v2 import UnifiedFeatureExtractor
from gui_dashboard import NIDSDashboard
from config_loader import get_config, get_active_dataset

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


class QUILLBOTSystem:
    """
    Main QUILLBOT NIDS System orchestrator.
    
    Coordinates:
    - Packet capture
    - Feature extraction
    - ML-based intrusion detection
    - Real-time visualization
    - Logging and reporting
    """
    
    def __init__(self, interface: Optional[str] = None):
        """
        Initialize QUILLBOT system.

        Args:
            interface: Network interface to monitor (None = default)
        """
        self.interface = interface
        self.sniffer = None
        self.predictor = None
        self.logger_obj = None
        self.dashboard = None
        self.is_running = False
        self.start_time = None
        self.packet_count = 0
        self.intrusion_count = 0
        self.normal_count = 0
        self.lock = threading.Lock()

        # Load configuration
        self.config = get_config()
        self.active_dataset = get_active_dataset()

        logger.info("=" * 80)
        logger.info("QUILLBOT NIDS - Network Intrusion Detection System v2.0")
        logger.info(f"Active Dataset: {self.active_dataset}")
        logger.info("=" * 80)
    
    def initialize_components(self) -> bool:
        """
        Initialize all system components.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            logger.info("Initializing QUILLBOT components...")
            
            # Initialize packet sniffer
            logger.info("Initializing packet sniffer...")
            self.sniffer = PacketSniffer(interface=self.interface)

            # Note: interface=None is valid for scapy (uses default interface)
            if self.sniffer.interface is None:
                logger.info("Using scapy's default network interface")
            else:
                logger.info(f"Using specified interface: {self.sniffer.interface}")

            logger.info("Packet sniffer initialized successfully")
            
            # Initialize predictor
            logger.info(f"Initializing unified intrusion predictor for {self.active_dataset}...")
            model_path = os.path.join(os.path.dirname(__file__), 'model', 'nids_model.pkl')
            scaler_path = os.path.join(os.path.dirname(__file__), 'model', 'scaler.pkl')
            encoder_path = os.path.join(os.path.dirname(__file__), 'model', 'encoder.pkl')

            # Check if model files exist
            if not os.path.exists(model_path):
                logger.warning(f"Model file not found: {model_path}")
                logger.info("Please train the model first using: python src/train_model_v2.py")
                return False

            self.predictor = UnifiedIntrusionPredictor(model_path, scaler_path, encoder_path)
            logger.info(f"Unified intrusion predictor initialized for {self.active_dataset}")
            
            # Initialize prediction logger
            logger.info("Initializing prediction logger...")
            log_path = os.path.join(os.path.dirname(__file__), 'logs', 'nids_log.txt')
            self.logger_obj = PredictionLogger(log_path)
            logger.info(f"Prediction logger initialized: {log_path}")
            
            logger.info("All components initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            return False
    
    def _process_packets(self) -> None:
        """Process captured packets in a separate thread."""
        try:
            logger.info("Starting packet processing thread...")
            
            while self.is_running:
                try:
                    # Get buffered packets
                    packets = self.sniffer.get_buffered_packets(count=10)
                    
                    if not packets:
                        time.sleep(0.01)
                        continue
                    
                    # Process each packet
                    for packet in packets:
                        try:
                            # Make prediction using v2 predictor
                            is_intrusion, confidence, attack_type = self.predictor.predict(packet)

                            # Convert to old format for compatibility
                            prediction = 1 if is_intrusion else 0

                            # Log prediction with attack type
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
                        except Exception as e:
                            logger.error(f"Error processing packet: {e}")
                except Exception as e:
                    logger.error(f"Error in packet processing loop: {e}")
                    time.sleep(0.1)
        except Exception as e:
            logger.error(f"Error in packet processing thread: {e}")
    
    def _update_dashboard_metrics(self) -> None:
        """Update dashboard metrics periodically."""
        try:
            logger.info("Starting dashboard update thread...")
            
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
                    logger.error(f"Error updating dashboard: {e}")
        except Exception as e:
            logger.error(f"Error in dashboard update thread: {e}")
    
    def start(self) -> None:
        """Start the QUILLBOT system."""
        try:
            if not self.initialize_components():
                logger.error("Failed to initialize components")
                return
            
            self.is_running = True
            self.start_time = time.time()
            
            logger.info("Starting QUILLBOT system...")
            
            # Start packet sniffer
            self.sniffer.start_sniffing()
            logger.info("Packet sniffer started")
            
            # Start packet processing thread
            processing_thread = threading.Thread(target=self._process_packets, daemon=True)
            processing_thread.start()
            logger.info("Packet processing thread started")
            
            # Start dashboard update thread
            update_thread = threading.Thread(target=self._update_dashboard_metrics, daemon=True)
            update_thread.start()
            logger.info("Dashboard update thread started")
            
            # Initialize and run dashboard
            logger.info("Initializing modern GUI dashboard...")
            root = ctk.CTk()
            self.dashboard = NIDSDashboard(root)
            logger.info("GUI dashboard initialized")
            
            logger.info("QUILLBOT system started successfully")
            logger.info("=" * 80)
            
            # Run dashboard (blocking)
            self.dashboard.run()
        except Exception as e:
            logger.error(f"Error starting system: {e}")
        finally:
            self.stop()
    
    def stop(self) -> None:
        """Stop the QUILLBOT system."""
        try:
            logger.info("Stopping QUILLBOT system...")
            self.is_running = False
            
            # Stop sniffer
            if self.sniffer:
                self.sniffer.stop_sniffing()
                logger.info("Packet sniffer stopped")
            
            # Generate final report
            self._generate_report()
            
            logger.info("QUILLBOT system stopped")
            logger.info("=" * 80)
        except Exception as e:
            logger.error(f"Error stopping system: {e}")
    
    def _generate_report(self) -> None:
        """Generate final system report."""
        try:
            elapsed_time = time.time() - self.start_time if self.start_time else 0
            
            report = f"""
{'=' * 80}
QUILLBOT NIDS - FINAL REPORT
{'=' * 80}
Runtime Duration: {elapsed_time:.2f} seconds
Total Packets Analyzed: {self.packet_count}
Intrusions Detected: {self.intrusion_count}
Normal Packets: {self.normal_count}
Detection Rate: {(self.intrusion_count / max(self.packet_count, 1) * 100):.2f}%
Average Throughput: {(self.packet_count / max(elapsed_time, 1)):.2f} packets/sec

Predictor Statistics:
{self.predictor.get_statistics() if self.predictor else 'N/A'}

Sniffer Statistics:
{self.sniffer.get_statistics() if self.sniffer else 'N/A'}
{'=' * 80}
"""
            logger.info(report)
            
            # Save report to file
            report_path = os.path.join(os.path.dirname(__file__), 'logs', 'final_report.txt')
            with open(report_path, 'w') as f:
                f.write(report)
            logger.info(f"Final report saved to {report_path}")
        except Exception as e:
            logger.error(f"Error generating report: {e}")


def main():
    """Main entry point."""
    try:
        # Create system instance
        system = QUILLBOTSystem(interface=None)
        
        # Start system
        system.start()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

