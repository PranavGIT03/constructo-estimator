import pandas as pd
import os

# Test Excel file reading
excel_file = 'Constructo.xlsx'
print(f"Excel file exists: {os.path.exists(excel_file)}")

if os.path.exists(excel_file):
    try:
        df = pd.read_excel(excel_file)
        print(f"Columns: {df.columns.tolist()}")
        print(f"Rows: {len(df)}")
        print("First few rows:")
        print(df.head())
    except Exception as e:
        print(f"Error reading Excel: {e}")
else:
    print("Creating sample Excel file...")
    sample_data = {
        'ID': [1, 2, 3],
        'Category': ['RCC', 'Electrical', 'Plumbing'],
        'Material': ['Cement', 'Wire', 'Pipe'],
        'Unit': ['bag', 'meter', 'meter'],
        'Price': [350, 12, 45]
    }
    df = pd.DataFrame(sample_data)
    df.to_excel(excel_file, index=False)
    print("Sample Excel file created!")