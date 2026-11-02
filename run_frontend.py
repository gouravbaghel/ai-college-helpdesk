"""
Run the Streamlit frontend for College Helpdesk.
Usage: python run_frontend.py
"""
import subprocess
import sys
import os

if __name__ == "__main__":
    frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "app.py")
    print("Starting College Helpdesk Frontend...")
    print(f"Frontend path: {frontend_path}")
    print("Access the app at: http://localhost:8501")
    print("Press Ctrl+C to stop.")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", frontend_path,
        "--server.port", "8501",
        "--server.headless", "true",
        "--theme.primaryColor", "#1B4F72",
        "--theme.backgroundColor", "#F8F9FA",
        "--theme.secondaryBackgroundColor", "#FFFFFF",
        "--theme.textColor", "#333333"
    ])
