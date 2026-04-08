#!/bin/bash
echo "Starting QUILLBOT NIDS Demo..."
cd "$(dirname "$0")"
pip install -r requirements.txt
python3 main_with_simulator.py
