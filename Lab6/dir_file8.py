import os

def delete_file(path):
    if os.path.exists(path) and os.access(path, os.W_OK):
        os.remove(path)
        print("File deleted.")
    else:
        print("File does not exist or is not accessible.")

delete_file(r"C:\Users\LENOVO\OneDrive\Документы\GitHub\PP2-Yerbol\B.txt")