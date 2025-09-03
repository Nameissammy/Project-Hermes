#!/usr/bin/env python
"""Dev helper to run FastAPI server ensuring package path is set."""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
SRC = os.path.join(ROOT, 'src')
if SRC not in sys.path:
    sys.path.insert(0, SRC)

def main():
    import uvicorn
    uvicorn.run("project_hermes.api:app", host="127.0.0.1", port=8001, reload=True)

if __name__ == "__main__":
    main()