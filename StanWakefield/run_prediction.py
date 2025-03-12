#!/usr/bin/env python3
"""
Runner script for the SEC Basketball Championship Predictor.

This script provides a simple way to run the predictor with default settings.
"""

import os
import sys
import subprocess
import webbrowser

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import numpy
        import pandas
        import PIL
        import pytesseract
        import matplotlib
        print("All required Python packages are installed.")
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install the required packages using:")
        print("pip install -r requirements.txt")
        return False

def check_tesseract():
    """Check if Tesseract OCR is installed and working."""
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        print("Tesseract OCR is installed and working.")
        return True
    except Exception:
        print("Warning: Tesseract OCR not found or not working.")
        print("The predictor will use fallback data instead of image processing.")
        return False

def run_predictor(use_fallback=False):
    """Run the SEC Tournament Predictor."""
    script_path = os.path.join(os.path.dirname(__file__), "sec_tournament_predictor.py")
    
    if not os.path.exists(script_path):
        print(f"Error: Could not find {script_path}")
        return False
        
    cmd = [sys.executable, script_path]
    if use_fallback:
        cmd.append("--fallback")
    
    print("Running SEC Tournament Predictor...")
    result = subprocess.run(cmd, check=False)
    
    if result.returncode != 0:
        print("Error: Predictor exited with an error.")
        return False
    
    return True

def open_results():
    """Open the results visualization."""
    results_path = os.path.join(os.path.dirname(__file__), "sec_championship_prediction.png")
    
    if not os.path.exists(results_path):
        print("Warning: Results visualization not found.")
        return False
    
    print("Opening results visualization...")
    webbrowser.open(f"file://{os.path.abspath(results_path)}")
    return True

def main():
    """Main function to run the predictor."""
    print("SEC Basketball Championship Predictor Runner")
    print("==========================================")
    
    if not check_dependencies():
        print("Error: Missing dependencies. Please install them and try again.")
        return False
    
    tesseract_available = check_tesseract()
    success = run_predictor(use_fallback=not tesseract_available)
    
    if success:
        open_results()
        print("\nPrediction completed successfully!")
        return True
    else:
        print("\nError running the predictor. Please check the error messages above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 