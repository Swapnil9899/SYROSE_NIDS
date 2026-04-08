"""
Download Real UNSW-NB15 Dataset from Kaggle

This script downloads the real UNSW-NB15 dataset from Kaggle and prepares it for use.

Requirements:
- Kaggle API credentials (kaggle.json)
- kaggle package: pip install kaggle

Author: QUILLBOT Development Team
Version: 1.0.0
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path

print("=" * 80)
print("UNSW-NB15 Real Dataset Download Script")
print("=" * 80)

# Check if kaggle is installed
try:
    import kaggle
    print("✓ Kaggle package found")
except ImportError:
    print("✗ Kaggle package not found")
    print("\nPlease install kaggle:")
    print("  pip install kaggle")
    print("\nThen configure your Kaggle API credentials:")
    print("  1. Go to https://www.kaggle.com/settings")
    print("  2. Click 'Create New API Token'")
    print("  3. Save kaggle.json to ~/.kaggle/ (Linux/Mac) or C:\\Users\\<username>\\.kaggle\\ (Windows)")
    sys.exit(1)

# Create directories
data_dir = Path("data/UNSW-NB15")
raw_dir = data_dir / "raw"
raw_dir.mkdir(parents=True, exist_ok=True)

print(f"\nData directory: {data_dir}")
print(f"Raw data directory: {raw_dir}")

# Download from Kaggle
print("\n" + "=" * 80)
print("Downloading UNSW-NB15 dataset from Kaggle...")
print("=" * 80)

try:
    # Download dataset
    print("\nDownloading... (this may take a few minutes)")
    os.system(f'kaggle datasets download -d alextamboli/unsw-nb15 -p {raw_dir} --unzip')
    print("✓ Download complete")
except Exception as e:
    print(f"✗ Error downloading dataset: {e}")
    print("\nManual download instructions:")
    print("1. Visit: https://www.kaggle.com/datasets/alextamboli/unsw-nb15")
    print("2. Click 'Download' button")
    print(f"3. Extract files to: {raw_dir}")
    print("4. Run this script again")
    sys.exit(1)

# Process the dataset
print("\n" + "=" * 80)
print("Processing dataset...")
print("=" * 80)

try:
    # Find CSV files
    csv_files = list(raw_dir.glob("*.csv"))
    print(f"\nFound {len(csv_files)} CSV files:")
    for f in csv_files:
        print(f"  - {f.name}")
    
    # Look for the main dataset files
    train_file = None
    test_file = None
    
    for f in csv_files:
        if 'train' in f.name.lower():
            train_file = f
        elif 'test' in f.name.lower():
            test_file = f
    
    if train_file and test_file:
        print(f"\n✓ Found training file: {train_file.name}")
        print(f"✓ Found testing file: {test_file.name}")
        
        # Load datasets
        print("\nLoading training data...")
        train_df = pd.read_csv(train_file)
        print(f"  Training samples: {len(train_df)}")
        print(f"  Features: {len(train_df.columns)}")
        
        print("\nLoading testing data...")
        test_df = pd.read_csv(test_file)
        print(f"  Testing samples: {len(test_df)}")
        print(f"  Features: {len(test_df.columns)}")
        
        # Combine datasets
        print("\nCombining datasets...")
        combined_df = pd.concat([train_df, test_df], ignore_index=True)
        print(f"  Total samples: {len(combined_df)}")
        
        # Check for label column
        label_col = None
        for col in ['label', 'Label', 'attack_cat', 'class']:
            if col in combined_df.columns:
                label_col = col
                break
        
        if label_col:
            print(f"\n✓ Found label column: {label_col}")
            print(f"  Label distribution:")
            print(combined_df[label_col].value_counts())
        
        # Save processed files
        print("\nSaving processed files...")
        train_df.to_csv(data_dir / "unsw_nb15_train_processed.csv", index=False)
        print(f"  ✓ Saved: {data_dir / 'unsw_nb15_train_processed.csv'}")
        
        test_df.to_csv(data_dir / "unsw_nb15_test_processed.csv", index=False)
        print(f"  ✓ Saved: {data_dir / 'unsw_nb15_test_processed.csv'}")
        
        combined_df.to_csv(data_dir / "unsw_nb15_combined.csv", index=False)
        print(f"  ✓ Saved: {data_dir / 'unsw_nb15_combined.csv'}")
        
        print("\n" + "=" * 80)
        print("✓ DATASET DOWNLOAD AND PROCESSING COMPLETE!")
        print("=" * 80)
        
        print("\nNext steps:")
        print("1. Retrain the model:")
        print("   python src/train_model_v2.py")
        print("\n2. Test the system:")
        print("   python test_unsw_integration.py")
        print("\n3. Run the NIDS:")
        print("   python main.py")
        
    else:
        print("\n✗ Could not find train/test files")
        print("\nAvailable files:")
        for f in csv_files:
            print(f"  - {f.name}")
        
        print("\nPlease check the file names and update this script if needed.")

except Exception as e:
    print(f"\n✗ Error processing dataset: {e}")
    import traceback
    traceback.print_exc()
    
    print("\nManual processing instructions:")
    print("1. Locate the CSV files in:", raw_dir)
    print("2. Identify training and testing files")
    print("3. Copy them to:")
    print(f"   - {data_dir / 'unsw_nb15_train_processed.csv'}")
    print(f"   - {data_dir / 'unsw_nb15_test_processed.csv'}")
    print("4. Combine them into:")
    print(f"   - {data_dir / 'unsw_nb15_combined.csv'}")

print("\n" + "=" * 80)

