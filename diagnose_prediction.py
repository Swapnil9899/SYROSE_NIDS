"""
Diagnostic script to test feature extraction and prediction.
"""
import sys
import os
sys.path.insert(0, 'src')

from preprocess_features_v2 import UnifiedFeatureExtractor
from predict_intrusion_v2 import UnifiedIntrusionPredictor
import numpy as np

# Test packet data (simulating what packet_sniffer provides)
test_packets = [
    {
        'timestamp': '2025-11-09T10:00:00',
        'src_ip': '192.168.1.100',
        'dst_ip': '10.0.0.1',
        'protocol': 'tcp',
        'src_port': 54321,
        'dst_port': 80,
        'packet_length': 1500,
        'tcp_flags': 0x02,  # SYN
        'payload_size': 0
    },
    {
        'timestamp': '2025-11-09T10:00:01',
        'src_ip': '192.168.1.101',
        'dst_ip': '10.0.0.2',
        'protocol': 'tcp',
        'src_port': 54322,
        'dst_port': 443,
        'packet_length': 800,
        'tcp_flags': 0x10,  # ACK
        'payload_size': 500
    },
    {
        'timestamp': '2025-11-09T10:00:02',
        'src_ip': '192.168.1.102',
        'dst_ip': '10.0.0.3',
        'protocol': 'udp',
        'src_port': 54323,
        'dst_port': 53,
        'packet_length': 100,
        'tcp_flags': 0,
        'payload_size': 50
    }
]

print("=" * 80)
print("QUILLBOT NIDS - PREDICTION DIAGNOSTIC")
print("=" * 80)
print()

# Initialize feature extractor
print("1. Initializing feature extractor...")
extractor = UnifiedFeatureExtractor(dataset='UNSW-NB15')
print(f"   Dataset: {extractor.dataset}")
print(f"   Features expected: {len(extractor.feature_columns)}")
print()

# Test feature extraction
print("2. Testing feature extraction...")
for i, packet in enumerate(test_packets):
    print(f"\n   Packet {i+1}:")
    print(f"   Input: {packet['src_ip']}:{packet['src_port']} -> {packet['dst_ip']}:{packet['dst_port']} ({packet['protocol']})")
    
    features = extractor.extract_packet_features(packet)
    print(f"   Extracted features: {len(features)} features")
    
    # Show first 10 features
    feature_items = list(features.items())[:10]
    for key, value in feature_items:
        print(f"     {key}: {value}")
    print(f"     ... ({len(features) - 10} more features)")
    
    # Check if all features are zeros/defaults
    non_zero_count = sum(1 for v in features.values() if isinstance(v, (int, float)) and v != 0)
    print(f"   Non-zero features: {non_zero_count}/{len(features)}")

print()
print("=" * 80)
print("3. Testing prediction...")
print()

# Initialize predictor
predictor = UnifiedIntrusionPredictor(
    model_path='model/nids_model.pkl',
    scaler_path='model/scaler.pkl',
    encoder_path='model/encoder.pkl'
)

# Test predictions
for i, packet in enumerate(test_packets):
    print(f"\n   Packet {i+1}: {packet['src_ip']}:{packet['src_port']} -> {packet['dst_ip']}:{packet['dst_port']}")
    is_intrusion, confidence, attack_type = predictor.predict(packet)
    
    print(f"   Prediction: {'INTRUSION' if is_intrusion else 'NORMAL'}")
    print(f"   Confidence: {confidence:.2%}")
    print(f"   Attack Type: {attack_type}")

print()
print("=" * 80)
print("4. Analyzing model...")
print()

# Load and analyze model
import pickle
with open('model/nids_model.pkl', 'rb') as f:
    model = pickle.load(f)

print(f"   Model type: {type(model).__name__}")
print(f"   Model classes: {model.classes_}")
print(f"   Number of estimators: {model.n_estimators}")

# Test with random features
print()
print("5. Testing with random features...")
random_features = np.random.rand(1, len(extractor.feature_columns))
prediction = model.predict(random_features)
probabilities = model.predict_proba(random_features)

print(f"   Random features prediction: {prediction[0]}")
print(f"   Probabilities: {probabilities[0]}")

print()
print("=" * 80)
print("DIAGNOSIS COMPLETE")
print("=" * 80)

