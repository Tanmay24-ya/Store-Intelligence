import sys
import subprocess
import os

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    # Ensure pandas and openpyxl are installed
    try:
        install_and_import('pandas')
        install_and_import('openpyxl')
    except Exception as e:
        print(f"Failed to install dependencies: {e}")
        sys.exit(1)

    import pandas as pd

    # Define store layout sections and coordinate bounds (for computer vision spatial analysis)
    layout_data = {
        "Zone_ID": ["Z1", "Z2", "Z3", "Z4", "Z5", "Z6", "Z7"],
        "Zone_Name": [
            "Entrance/Exit Area",
            "Aisle 1 - Fresh Produce",
            "Aisle 2 - Packaged Goods",
            "Aisle 3 - Bakery & Dairy",
            "Aisle 4 - Cosmetics & Health",
            "Checkout Counter 1",
            "Checkout Counter 2"
        ],
        "Camera_Coverage": ["CAM1", "CAM2", "CAM2, CAM3", "CAM3", "CAM3", "CAM4", "CAM5"],
        "X_Min": [0.0, 10.0, 20.0, 30.0, 40.0, 15.0, 25.0],
        "Y_Min": [0.0, 0.0, 0.0, 0.0, 0.0, 50.0, 50.0],
        "X_Max": [10.0, 20.0, 30.0, 40.0, 50.0, 25.0, 35.0],
        "Y_Max": [15.0, 50.0, 50.0, 50.0, 50.0, 60.0, 60.0],
        "Description": [
            "Main entry point and security gate",
            "Fruits, vegetables, and organic selection",
            "Canned goods, grains, and spices",
            "Freshly baked bread and dairy coolers",
            "Personal care, pharmacy, and beauty products",
            "Primary express register",
            "Secondary assisted register"
        ]
    }

    df = pd.DataFrame(layout_data)

    # Save to Excel
    excel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "store_layout.xlsx")
    
    # We use ExcelWriter to format columns beautifully
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Store Layout Plan")
        
        # Style sheet
        workbook = writer.book
        worksheet = writer.sheets["Store Layout Plan"]
        
        # Adjust column widths automatically for visual excellence
        for col in worksheet.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = chr(65 + col[0].column - 1)
            worksheet.column_dimensions[col_letter].width = max(max_len + 3, 10)
            
    print(f"Successfully generated beautifully-styled Excel file at: {excel_path}")

if __name__ == "__main__":
    main()
