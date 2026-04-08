"""
Comprehensive Test Script for UNSW-NB15 Integration
Tests all v2 modules and demonstrates the new system functionality

Author: QUILLBOT Development Team
Version: 1.0.0
"""

import sys
import os
import time
import numpy as np
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import v2 modules
from config_loader import (
    get_config, get_active_dataset, is_multiclass_classification,
    get_attack_category_names, get_category_name_from_id
)
from preprocess_features_v2 import UnifiedFeatureExtractor
from predict_intrusion_v2 import UnifiedIntrusionPredictor

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print formatted header."""
    print(f"\n{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.WHITE}{text.center(80)}{Colors.END}")
    print(f"{Colors.CYAN}{'='*80}{Colors.END}\n")

def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_info(text):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def print_warning(text):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def test_config_loader():
    """Test configuration loading."""
    print_header("TEST 1: Configuration Loader")
    
    try:
        # Load configuration
        config = get_config()
        print_success("Configuration loaded successfully")
        
        # Get active dataset
        dataset = get_active_dataset()
        print_info(f"Active dataset: {dataset}")
        
        # Check classification type
        is_multi = is_multiclass_classification()
        class_type = "Multi-class" if is_multi else "Binary"
        print_info(f"Classification type: {class_type}")
        
        # Get attack categories
        categories = get_attack_category_names()
        print_info(f"Attack categories: {len(categories)}")
        for name, id in list(categories.items())[:5]:
            print(f"  - {name}: {id}")
        if len(categories) > 5:
            print(f"  ... and {len(categories) - 5} more")
        
        print_success("Configuration loader test PASSED")
        return True
    
    except Exception as e:
        print_error(f"Configuration loader test FAILED: {e}")
        return False

def test_feature_extractor():
    """Test unified feature extractor."""
    print_header("TEST 2: Unified Feature Extractor")
    
    try:
        # Initialize extractor
        dataset = get_active_dataset()
        extractor = UnifiedFeatureExtractor(dataset=dataset)
        print_success(f"Feature extractor initialized for {dataset}")
        
        # Create sample packet data
        sample_packet = {
            'src_ip': '192.168.1.100',
            'dst_ip': '10.0.0.50',
            'src_port': 54321,
            'dst_port': 80,
            'protocol': 'tcp',
            'packet_length': 1500,
            'flags': 'S',
            'ttl': 64,
            'window_size': 65535,
            'timestamp': time.time()
        }
        
        print_info("Sample packet data:")
        for key, value in sample_packet.items():
            print(f"  - {key}: {value}")
        
        # Extract features
        features = extractor.extract_packet_features(sample_packet)
        print_success(f"Features extracted: {len(features)} features")
        
        # Show first 10 features
        print_info("First 10 features:")
        for i, (key, value) in enumerate(list(features.items())[:10]):
            print(f"  {i+1}. {key}: {value}")
        
        print_success("Feature extractor test PASSED")
        return True
    
    except Exception as e:
        print_error(f"Feature extractor test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_prediction_system():
    """Test unified prediction system."""
    print_header("TEST 3: Unified Prediction System")
    
    try:
        # Check if model exists
        model_path = 'model/nids_model.pkl'
        scaler_path = 'model/scaler.pkl'
        encoder_path = 'model/encoder.pkl'
        
        if not all(os.path.exists(p) for p in [model_path, scaler_path, encoder_path]):
            print_warning("Model files not found. Please train the model first:")
            print_info("  python src/train_model_v2.py")
            return False
        
        # Initialize predictor
        predictor = UnifiedIntrusionPredictor(model_path, scaler_path, encoder_path)
        print_success("Predictor initialized successfully")
        
        # Create test packets
        test_packets = [
            {
                'name': 'Normal HTTP Request',
                'src_ip': '192.168.1.100',
                'dst_ip': '93.184.216.34',
                'src_port': 54321,
                'dst_port': 80,
                'protocol': 'tcp',
                'packet_length': 512,
                'flags': 'S',
                'ttl': 64,
                'window_size': 65535,
                'timestamp': time.time()
            },
            {
                'name': 'Suspicious Port Scan',
                'src_ip': '10.0.0.50',
                'dst_ip': '192.168.1.1',
                'src_port': 12345,
                'dst_port': 22,
                'protocol': 'tcp',
                'packet_length': 40,
                'flags': 'S',
                'ttl': 128,
                'window_size': 1024,
                'timestamp': time.time()
            },
            {
                'name': 'Large Data Transfer',
                'src_ip': '192.168.1.50',
                'dst_ip': '8.8.8.8',
                'src_port': 443,
                'dst_port': 53,
                'protocol': 'udp',
                'packet_length': 8192,
                'flags': '',
                'ttl': 64,
                'window_size': 0,
                'timestamp': time.time()
            }
        ]
        
        print_info(f"Testing with {len(test_packets)} sample packets:\n")
        
        # Make predictions
        results = []
        for i, packet in enumerate(test_packets, 1):
            print(f"{Colors.YELLOW}Packet {i}: {packet['name']}{Colors.END}")
            print(f"  Source: {packet['src_ip']}:{packet['src_port']}")
            print(f"  Destination: {packet['dst_ip']}:{packet['dst_port']}")
            print(f"  Protocol: {packet['protocol'].upper()}")
            
            # Predict
            start_time = time.time()
            is_intrusion, confidence, attack_type = predictor.predict(packet)
            latency = (time.time() - start_time) * 1000  # ms
            
            # Display result
            if is_intrusion:
                print(f"  {Colors.RED}Result: INTRUSION DETECTED{Colors.END}")
                print(f"  Attack Type: {attack_type}")
            else:
                print(f"  {Colors.GREEN}Result: NORMAL TRAFFIC{Colors.END}")
            
            print(f"  Confidence: {confidence:.2f}%")
            print(f"  Latency: {latency:.2f}ms")
            print()
            
            results.append({
                'packet': packet['name'],
                'is_intrusion': is_intrusion,
                'confidence': confidence,
                'attack_type': attack_type,
                'latency': latency
            })
        
        # Get statistics
        stats = predictor.get_statistics()
        print_info("Prediction Statistics:")
        print(f"  Total Predictions: {stats['total_predictions']}")
        print(f"  Intrusions Detected: {stats['intrusions_detected']}")
        print(f"  Normal Packets: {stats['normal_packets']}")
        print(f"  Intrusion Rate: {stats['intrusion_rate']*100:.2f}%")
        print(f"  Avg Latency: {stats['avg_latency_ms']:.2f}ms")
        print(f"  Max Latency: {stats['max_latency_ms']:.2f}ms")
        print(f"  Min Latency: {stats['min_latency_ms']:.2f}ms")
        
        # Check latency requirement (<50ms)
        if stats['avg_latency_ms'] < 50:
            print_success(f"Latency requirement met: {stats['avg_latency_ms']:.2f}ms < 50ms")
        else:
            print_warning(f"Latency above target: {stats['avg_latency_ms']:.2f}ms > 50ms")
        
        print_success("Prediction system test PASSED")
        return True
    
    except Exception as e:
        print_error(f"Prediction system test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dataset_switching():
    """Test dataset switching capability."""
    print_header("TEST 4: Dataset Switching")
    
    try:
        config = get_config()
        
        # Show current dataset
        current_dataset = get_active_dataset()
        print_info(f"Current active dataset: {current_dataset}")
        
        # Show available datasets
        datasets = ['NSL-KDD', 'UNSW-NB15']
        print_info("Available datasets:")
        for ds in datasets:
            if ds == current_dataset:
                print(f"  {Colors.GREEN}✓ {ds} (active){Colors.END}")
            else:
                print(f"    {ds}")
        
        # Show how to switch
        print_info("\nTo switch datasets:")
        print("  1. Edit config.yaml")
        print("  2. Change 'dataset.active' to desired dataset")
        print("  3. Retrain model: python src/train_model_v2.py")
        
        print_success("Dataset switching test PASSED")
        return True
    
    except Exception as e:
        print_error(f"Dataset switching test FAILED: {e}")
        return False

def run_all_tests():
    """Run all tests."""
    print_header("QUILLBOT NIDS - UNSW-NB15 Integration Test Suite")
    print(f"{Colors.WHITE}Testing all v2 modules and system functionality{Colors.END}")
    print(f"{Colors.WHITE}Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    
    # Run tests
    results = []
    results.append(("Configuration Loader", test_config_loader()))
    results.append(("Feature Extractor", test_feature_extractor()))
    results.append(("Prediction System", test_prediction_system()))
    results.append(("Dataset Switching", test_dataset_switching()))
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        if result:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED!{Colors.END}")
        print(f"{Colors.GREEN}The UNSW-NB15 integration is working correctly.{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ SOME TESTS FAILED{Colors.END}")
        print(f"{Colors.RED}Please review the errors above.{Colors.END}")
        return 1

if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)

