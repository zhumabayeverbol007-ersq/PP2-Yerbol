import os

def test_path_details(path):
    if os.path.exists(path):
        print("Path exists.")
        print("Directory:", os.path.dirname(path))
        print("Filename:", os.path.basename(path))
    else:
        print("Path does not exist.")

test_path_details(r"C:\Users\LENOVO\OneDrive\Документы\PP2_lab6_os.docx")