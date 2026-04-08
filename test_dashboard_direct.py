"""
Test dashboard directly without login
"""
import sys
import os

# Add src to path
sys.path.insert(0, 'src')

print("Importing modules...")
try:
    import customtkinter as ctk
    print("✓ CustomTkinter imported")
    
    from gui_dashboard import NIDSDashboard
    print("✓ NIDSDashboard imported")
    
    print("\nCreating root window...")
    root = ctk.CTk()
    print("✓ Root window created")
    
    print("\nInitializing dashboard...")
    dashboard = NIDSDashboard(root, username="admin", session_id="test123")
    print("✓ Dashboard initialized")
    
    print("\nStarting dashboard...")
    dashboard.run()
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

