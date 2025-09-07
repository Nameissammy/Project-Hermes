#!/usr/bin/env python3
"""
Project Hermes Demo Launcher
----------------------------

This script launches the Project Hermes demo using one of the test scripts.
"""

import os
import sys
import subprocess


def main():
    """Run one of the test scripts as a demo."""
    # Display available demos
    print("Project Hermes Demo")
    print("===================")
    print("\nAvailable demo types:")
    print("1. Mocked Travel Crew (no API key needed - works without real API keys)")
    print("2. Simple Crew Test (works with Gemini, Claude, or OpenAI)")
    print("3. Direct Travel Crew Test (works with Gemini, Claude, or OpenAI)")
    print("\nNote: For options 2 and 3, the system will try Gemini first,")
    print("      then Claude, then OpenAI based on available API keys.")

    # Get user choice
    choice = input("\nSelect a demo type (1-3) or press Enter for default (1): ").strip()
    if not choice:
        choice = "1"

    # Map choices to scripts
    scripts = {
        "1": "test_mocked_travel_crew.py",
        "2": "test_simple_crew.py",
        "3": "test_direct_travel_crew.py",
    }

    # Validate choice
    if choice not in scripts:
        print(f"Invalid choice: {choice}. Using default (1).")
        choice = "1"

    script_name = scripts[choice]

    # Get the absolute path to the test script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, script_name)

    # Check if the script exists
    if not os.path.exists(script_path):
        print(f"Error: Script not found at {script_path}")
        return 1

    print(f"\nRunning {script_name}...")
    print("=" * 50)

    # Execute the test script
    result = subprocess.call([sys.executable, script_path])
    return result


if __name__ == "__main__":
    sys.exit(main())
