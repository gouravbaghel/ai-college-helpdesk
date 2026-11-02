"""
Unified Runner for AI-Powered College Helpdesk & Student Assistant.
Starts both the FastAPI Backend and Streamlit Frontend concurrently.

Usage:
    python run_all.py
"""
import subprocess
import sys
import time
import os
import signal

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def main():
    os.chdir(PROJECT_ROOT)
    print("=" * 60)
    print("  AI-Powered College Helpdesk - Unified Launcher")
    print("=" * 60)
    print()

    # 1. Start Backend
    print("[1/2] Starting FastAPI Backend on http://0.0.0.0:8000...")
    backend_cmd = [
        sys.executable, "-m", "uvicorn", "backend.main:app",
        "--host", "0.0.0.0",
        "--port", "8000"
    ]
    backend_proc = subprocess.Popen(backend_cmd, cwd=PROJECT_ROOT)

    # Allow backend 2 seconds to initialize database & tables
    time.sleep(2)

    # 2. Start Frontend
    print("[2/2] Starting Streamlit Frontend on http://localhost:8501...")
    frontend_path = os.path.join(PROJECT_ROOT, "frontend", "app.py")
    frontend_cmd = [
        sys.executable, "-m", "streamlit", "run", frontend_path,
        "--server.port", "8501",
        "--server.headless", "true",
        "--theme.primaryColor", "#0f2439",
        "--theme.backgroundColor", "#f8fafc",
        "--theme.secondaryBackgroundColor", "#ffffff",
        "--theme.textColor", "#1e293b"
    ]
    frontend_proc = subprocess.Popen(frontend_cmd, cwd=PROJECT_ROOT)

    print()
    print("=" * 60)
    print("  Services Live:")
    print("  - Backend API:    http://localhost:8000 (Docs: /docs)")
    print("  - Frontend UI:    http://localhost:8501")
    print("  Press Ctrl+C to terminate both services.")
    print("=" * 60)
    print()

    try:
        while True:
            # Check if either process terminated unexpectedly
            if backend_proc.poll() is not None:
                print("[ERROR] Backend process terminated unexpectedly.")
                break
            if frontend_proc.poll() is not None:
                print("[INFO] Frontend process closed.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down services gracefully...")
    finally:
        for proc in [frontend_proc, backend_proc]:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    proc.kill()
        print("[OK] All services stopped.")

if __name__ == "__main__":
    main()
