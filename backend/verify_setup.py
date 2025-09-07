#!/usr/bin/env python3
"""
Project Hermes Package Verification
----------------------------------

This script verifies that the pyproject.toml setup is working correctly.
"""

import importlib
import subprocess
import sys


def check_package_info():
    """Print information about the installed package."""
    print("Python Version:", sys.version)
    print("\nPython Path:")
    for path in sys.path:
        print(f"  - {path}")

    # Try to import key modules
    print("\nChecking for required dependencies:")
    dependencies = [
        "crewai",
        "fastapi",
        "dotenv",
        "uvicorn",
        "pydantic",
        "langchain",
        "langchain.chat_models",
        "google.generativeai",
        "anthropic",
        "requests",
    ]

    for dep in dependencies:
        try:
            # Try to import the module
            module_name = dep.split(".")[0]  # Get the top-level module name
            importlib.import_module(module_name)
            print(f"  ✓ {module_name} is installed")
        except ImportError:
            print(f"  ✗ {module_name} is not installed")

    # Try to run pip list to show installed packages
    print("\nInstalled packages (via pip list):")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"], capture_output=True, text=True, check=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError:
        print("  Unable to run 'pip list'")

    print("\nVerification completed.")
    print("\nTo install dependencies using uv and pyproject.toml, run:")
    print("  1. Create virtual environment:  uv venv")
    print("  2. Activate virtual environment: source .venv/bin/activate")
    print("     (On Windows: .venv\\Scripts\\activate)")
    print("  3. Install dependencies:         uv pip install -e .")
    print("\nThis will install all required packages defined in pyproject.toml.")


if __name__ == "__main__":
    check_package_info()


if __name__ == "__main__":
    check_package_info()
