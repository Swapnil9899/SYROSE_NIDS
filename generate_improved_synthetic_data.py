"""
Generate improved synthetic UNSW-NB15 data with realistic attack patterns.

This script creates synthetic network traffic data that mimics real-world patterns,
with distinct characteristics for different attack types to enable proper model training.
"""
import pandas as pd
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Attack category mapping
ATTACK_CATEGORIES = {
    'Normal': 0,
    'Generic': 1,
    'Exploits': 2,
    'Fuzzers': 3,
    'DoS': 4,
    'Reconnaissance': 5,
    'Analysis': 6,
    'Backdoor': 7,
    'Shellcode': 8,
    'Worms': 9
}

def generate_normal_traffic():
    """Generate normal traffic with typical patterns - MATCHES REAL PACKET CAPTURE."""
    # Real packets from packet sniffer have mostly zeros for advanced features
    # This matches what we actually see from live network traffic
    return {
        'sport': np.random.randint(1024, 65535),
        'dsport': np.random.choice([80, 443, 22, 53, 25, 8080, 3389]),  # Common services
        'proto': np.random.choice(['tcp', 'udp', 'icmp'], p=[0.7, 0.25, 0.05]),
        'state': 'CON',  # Most real packets show CON state
        'dur': 0.0,  # Single packet capture = 0 duration
        'sbytes': np.random.choice([64, 128, 256, 512, 800, 1500]),  # Common packet sizes
        'dbytes': 0,  # Single packet = no response yet
        'sttl': 64,  # Standard TTL
        'dttl': 64,
        'sloss': 0,
        'dloss': 0,
        'service': '-',  # Most packets show '-'
        'Sload': 0,  # Single packet
        'Dload': 0,
        'Spkts': 1,  # Single packet
        'Dpkts': 0,
        'swin': 0,
        'dwin': 0,
        'stcpb': 0,
        'dtcpb': 0,
        'smeansz': np.random.choice([64, 128, 256, 512, 800, 1500]),
        'dmeansz': 0,
        'trans_depth': 0,
        'res_bdy_len': 0,
        'Sjit': 0,
        'Djit': 0,
        'Stime': 0,
        'Ltime': 0,
        'Sintpkt': 0,
        'Dintpkt': 0,
        'tcprtt': 0,
        'synack': 0,
        'ackdat': 0,
        'is_sm_ips_ports': 0,
        'ct_state_ttl': 1,
        'ct_flw_http_mthd': 0,
        'is_ftp_login': 0,
        'ct_ftp_cmd': 0,
        'ct_srv_src': 1,
        'ct_srv_dst': 1,
        'ct_dst_ltm': 1,
        'ct_src_ltm': 1,
        'ct_src_dport_ltm': 1,
        'ct_dst_sport_ltm': 1,
        'ct_dst_src_ltm': 1,
        'attack_cat': 'Normal',
        'Label': 0
    }

def generate_dos_attack():
    """Generate DoS attack - VERY LARGE PACKETS or MANY SMALL PACKETS."""
    # Key distinguishing features: abnormally large sbytes OR very small packets
    attack_type = np.random.choice(['flood', 'large'])

    if attack_type == 'flood':
        # Flood attack: many small packets
        sbytes = np.random.randint(10, 100)  # Very small
        Spkts = np.random.randint(100, 1000)  # Many packets
    else:
        # Large packet attack
        sbytes = np.random.randint(5000, 65535)  # Very large
        Spkts = np.random.randint(10, 50)

    return {
        'sport': np.random.randint(1024, 65535),
        'dsport': np.random.choice([80, 443, 22]),
        'proto': 'tcp',
        'state': 'CON',
        'dur': 0.0,
        'sbytes': sbytes,  # KEY DIFFERENCE
        'dbytes': 0,
        'sttl': 64,
        'dttl': 64,
        'sloss': 0,
        'dloss': 0,
        'service': '-',
        'Sload': 0,
        'Dload': 0,
        'Spkts': Spkts,  # KEY DIFFERENCE
        'Dpkts': 0,
        'swin': 0,
        'dwin': 0,
        'stcpb': 0,
        'dtcpb': 0,
        'smeansz': sbytes,
        'dmeansz': 0,
        'trans_depth': 0,
        'res_bdy_len': 0,
        'Sjit': 0,
        'Djit': 0,
        'Stime': 0,
        'Ltime': 0,
        'Sintpkt': 0,
        'Dintpkt': 0,
        'tcprtt': 0,
        'synack': 0,
        'ackdat': 0,
        'is_sm_ips_ports': 1,  # KEY DIFFERENCE: same IPs/ports
        'ct_state_ttl': np.random.randint(50, 200),  # KEY DIFFERENCE: many connections
        'ct_flw_http_mthd': 0,
        'is_ftp_login': 0,
        'ct_ftp_cmd': 0,
        'ct_srv_src': np.random.randint(50, 200),  # KEY DIFFERENCE
        'ct_srv_dst': np.random.randint(50, 200),  # KEY DIFFERENCE
        'ct_dst_ltm': np.random.randint(50, 200),  # KEY DIFFERENCE
        'ct_src_ltm': np.random.randint(50, 200),  # KEY DIFFERENCE
        'ct_src_dport_ltm': np.random.randint(50, 200),  # KEY DIFFERENCE
        'ct_dst_sport_ltm': np.random.randint(50, 200),  # KEY DIFFERENCE
        'ct_dst_src_ltm': np.random.randint(50, 200),  # KEY DIFFERENCE
        'attack_cat': 'DoS',
        'Label': 1
    }

def generate_reconnaissance():
    """Generate reconnaissance/scanning attack."""
    return {
        'sport': np.random.randint(1024, 65535),
        'dsport': np.random.randint(1, 65535),  # Random ports (scanning)
        'proto': np.random.choice(['tcp', 'udp', 'icmp']),
        'state': 'INT',
        'dur': np.random.uniform(0.001, 0.5),
        'sbytes': np.random.randint(40, 100),  # Small probes
        'dbytes': 0,
        'sttl': np.random.choice([64, 128, 255]),
        'dttl': 0,
        'sloss': 0,
        'dloss': 0,
        'service': '-',
        'Sload': np.random.uniform(100, 1000),
        'Dload': 0,
        'Spkts': 1,  # Single packet probes
        'Dpkts': 0,
        'swin': 0,
        'dwin': 0,
        'stcpb': 0,
        'dtcpb': 0,
        'smeansz': np.random.uniform(40, 100),
        'dmeansz': 0,
        'trans_depth': 0,
        'res_bdy_len': 0,
        'Sjit': 0,
        'Djit': 0,
        'Stime': np.random.randint(0, 1000000),
        'Ltime': np.random.randint(0, 1000000),
        'Sintpkt': np.random.uniform(0, 10),
        'Dintpkt': 0,
        'tcprtt': 0,
        'synack': 0,
        'ackdat': 0,
        'is_sm_ips_ports': 0,
        'ct_state_ttl': np.random.randint(10, 100),  # Many different connections
        'ct_flw_http_mthd': 0,
        'is_ftp_login': 0,
        'ct_ftp_cmd': 0,
        'ct_srv_src': 1,
        'ct_srv_dst': np.random.randint(10, 100),  # Many destinations
        'ct_dst_ltm': np.random.randint(10, 100),
        'ct_src_ltm': 1,
        'ct_src_dport_ltm': np.random.randint(10, 100),
        'ct_dst_sport_ltm': 1,
        'ct_dst_src_ltm': np.random.randint(10, 100),
        'attack_cat': 'Reconnaissance',
        'Label': 1
    }

def generate_exploits():
    """Generate exploit attack."""
    return {
        'sport': np.random.randint(1024, 65535),
        'dsport': np.random.choice([80, 443, 22, 21, 3389]),
        'proto': 'tcp',
        'state': 'CON',
        'dur': np.random.uniform(1, 30),
        'sbytes': np.random.lognormal(8, 2),
        'dbytes': np.random.lognormal(6, 2),
        'sttl': np.random.choice([64, 128]),
        'dttl': np.random.choice([64, 128]),
        'sloss': 0,
        'dloss': 0,
        'service': np.random.choice(['http', 'https', 'ssh', 'ftp']),
        'Sload': np.random.uniform(1000, 10000),
        'Dload': np.random.uniform(100, 5000),
        'Spkts': np.random.randint(10, 100),
        'Dpkts': np.random.randint(5, 50),
        'swin': np.random.randint(0, 255),
        'dwin': np.random.randint(0, 255),
        'stcpb': np.random.randint(0, 2147483647),
        'dtcpb': np.random.randint(0, 2147483647),
        'smeansz': np.random.uniform(100, 1500),
        'dmeansz': np.random.uniform(50, 500),
        'trans_depth': np.random.randint(1, 10),
        'res_bdy_len': np.random.randint(100, 50000),
        'Sjit': np.random.uniform(0, 20),
        'Djit': np.random.uniform(0, 20),
        'Stime': np.random.randint(0, 1000000),
        'Ltime': np.random.randint(0, 1000000),
        'Sintpkt': np.random.uniform(10, 100),
        'Dintpkt': np.random.uniform(10, 100),
        'tcprtt': np.random.uniform(10, 200),
        'synack': np.random.uniform(10, 200),
        'ackdat': np.random.uniform(10, 200),
        'is_sm_ips_ports': 0,
        'ct_state_ttl': np.random.randint(1, 10),
        'ct_flw_http_mthd': np.random.randint(1, 10),
        'is_ftp_login': np.random.choice([0, 1]),
        'ct_ftp_cmd': np.random.randint(0, 10),
        'ct_srv_src': np.random.randint(1, 10),
        'ct_srv_dst': np.random.randint(1, 10),
        'ct_dst_ltm': np.random.randint(1, 10),
        'ct_src_ltm': np.random.randint(1, 10),
        'ct_src_dport_ltm': np.random.randint(1, 10),
        'ct_dst_sport_ltm': np.random.randint(1, 10),
        'ct_dst_src_ltm': np.random.randint(1, 10),
        'attack_cat': 'Exploits',
        'Label': 1
    }

def generate_generic_attack():
    """Generate generic attack."""
    base = generate_normal_traffic()
    # Modify to make it suspicious
    base['sbytes'] = np.random.lognormal(9, 2)  # Higher than normal
    base['Spkts'] = np.random.randint(50, 200)  # More packets
    base['Sload'] = np.random.uniform(5000, 20000)  # Higher load
    base['ct_srv_src'] = np.random.randint(20, 100)  # More connections
    base['attack_cat'] = 'Generic'
    base['Label'] = 1
    return base

def generate_dataset(num_samples=20000, intrusion_ratio=0.3):
    """Generate complete synthetic dataset."""
    logger.info(f"Generating {num_samples} samples with {intrusion_ratio*100}% intrusions...")
    
    num_intrusions = int(num_samples * intrusion_ratio)
    num_normal = num_samples - num_intrusions
    
    data = []
    
    # Generate normal traffic
    for _ in range(num_normal):
        data.append(generate_normal_traffic())
    
    # Generate attacks (distribute across types)
    attack_generators = {
        'DoS': generate_dos_attack,
        'Reconnaissance': generate_reconnaissance,
        'Exploits': generate_exploits,
        'Generic': generate_generic_attack
    }
    
    samples_per_attack = num_intrusions // len(attack_generators)
    
    for attack_type, generator in attack_generators.items():
        for _ in range(samples_per_attack):
            data.append(generator())
    
    # Add remaining samples
    remaining = num_intrusions - (samples_per_attack * len(attack_generators))
    for _ in range(remaining):
        generator = np.random.choice(list(attack_generators.values()))
        data.append(generator())
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add IP addresses
    df['srcip'] = [f"192.168.{np.random.randint(1,255)}.{np.random.randint(1,255)}" for _ in range(len(df))]
    df['dstip'] = [f"10.0.{np.random.randint(1,255)}.{np.random.randint(1,255)}" for _ in range(len(df))]
    
    # Add attack_cat_encoded
    df['attack_cat_encoded'] = df['attack_cat'].map(ATTACK_CATEGORIES)
    
    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    logger.info(f"Generated {len(df)} samples")
    logger.info(f"Label distribution:\n{df['Label'].value_counts()}")
    logger.info(f"Attack type distribution:\n{df['attack_cat'].value_counts()}")
    
    return df

if __name__ == '__main__':
    # Generate dataset
    df = generate_dataset(num_samples=20000, intrusion_ratio=0.3)
    
    # Save
    output_dir = Path('data/UNSW-NB15')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Split into train/test
    train_size = int(len(df) * 0.75)
    df_train = df.iloc[:train_size]
    df_test = df.iloc[train_size:]
    
    df_train.to_csv(output_dir / 'unsw_nb15_train_processed.csv', index=False)
    df_test.to_csv(output_dir / 'unsw_nb15_test_processed.csv', index=False)
    df.to_csv(output_dir / 'unsw_nb15_combined.csv', index=False)
    
    logger.info(f"Saved to {output_dir}")
    logger.info(f"Train: {len(df_train)} samples")
    logger.info(f"Test: {len(df_test)} samples")

