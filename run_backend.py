import uvicorn
import os
from pathlib import Path

if __name__ == '__main__':
    os.chdir(Path(__file__).resolve().parent)
    uvicorn.run('backend.main:app', host='0.0.0.0', port=8000, reload=True)
