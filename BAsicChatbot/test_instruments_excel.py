#!/usr/bin/env python3
"""
Test script for querying INSTRUMENTS.xlsx via the HimalayaWebLoaderTool.
This script checks if instrument-specific queries return correct field values from the Excel file.
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

def test_instruments_excel():
    """Test Excel-specific search functionality."""
    try:
        from langgraphagenticai.tools.webloader_tool import get_himalaya_tool

        print("Initializing Himalaya Enterprises tool...")
        himalaya_tool = get_himalaya_tool()
        print("Tool initialized successfully!")

        # Test queries for various fields and instruments
        excel_queries = [
            # Replace these with actual instrument names/fields from your Excel file
            "What is the cal report number for the WELDING MACHINE?",
            "What is the range of the VERNIER CALLIPER?",
            "What is the due date for the SURFACE PLATE?",
            "What is the cal date for the MICROMETER?",
            "Who did the calibration for the HEIGHT GAUGE?",
            "What is the machine number of the DRILL MACHINE?",
            "What is the instrument number for the TRY SQUARE?",
            "What is the list count of the DIAL GAUGE?",
            "What is the quantity of the SPIRIT LEVEL?",
            "Give all details of the WELDING MACHINE.",
            "Show all information for the VERNIER CALLIPER.",
            "What are the cal report number and due date for the MICROMETER?",
            "List all instruments in the INSTRUMENTS.xlsx file."
        ]

        print("\n" + "="*50)
        print("Testing INSTRUMENTS.xlsx-specific queries:")
        print("="*50)

        for query in excel_queries:
            print(f"\nQuery: {query}")
            print("-" * 40)
            try:
                result = himalaya_tool._run(query)
                print(f"Result: {result}")
                print("\n" + "="*50)
            except Exception as e:
                print(f"Error: {e}")

        print("\nTest completed!")

    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_instruments_excel()
