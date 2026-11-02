import sys
import os

# Ensure the project root directory is in the Python search path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Expose the FastAPI application instance at the root level
from backend.main import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
