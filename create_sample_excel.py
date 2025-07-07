import pandas as pd

# Create sample Excel data if file doesn't exist
sample_data = {
    'ID': [1, 2, 3, 4, 5],
    'Category': ['RCC', 'RCC', 'Electrical', 'Plumbing', 'RCC'],
    'Material': ['Cement', 'Steel Rebar', 'Copper Wire', 'PVC Pipe', 'Sand'],
    'Unit': ['bag', 'kg', 'meter', 'meter', 'cubic_ft'],
    'Price': [350, 65, 12, 45, 45],
    'Supplier': ['ABC Corp', 'XYZ Ltd', 'ElectroMax', 'PipeCo', 'BuildMart'],
    'Stock': [100, 500, 1000, 200, 300]
}

df = pd.DataFrame(sample_data)
df.to_excel('Constructo.xlsx', index=False)
print("Sample Excel file 'Constructo.xlsx' created!")