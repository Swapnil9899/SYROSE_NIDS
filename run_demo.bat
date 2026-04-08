@echo off
echo Starting QUILLBOT NIDS Demo...
cd /d %~dp0
call pip install -r requirements.txt
python main_with_simulator.py
pause
