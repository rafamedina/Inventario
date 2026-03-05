import sys
import os

# Add the parent of current directory to sys.path so we can import 'Inventario'
sys.path.append(os.path.dirname(os.getcwd()))

try:
    print("Attempting to import Inventario...")
    import Inventario
    print("Import success!")
    
    # Check if manifest is accessible and parseable
    import ast
    manifest_path = os.path.join(os.getcwd(), "__manifest__.py")
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_content = f.read()
            manifest_dict = ast.literal_eval(manifest_content)
            print("Manifest parsed successfully!")
            
            # Check if all files listed in manifest exist
            for key in ['data', 'demo']:
                if key in manifest_dict:
                    for file_path in manifest_dict[key]:
                        full_path = os.path.join(os.getcwd(), file_path)
                        if not os.path.exists(full_path):
                            print(f"ERROR: File {file_path} listed in manifest[{key}] does not exist at {full_path}")
                        else:
                            print(f"Verified: {file_path}")
    else:
        print("ERROR: __manifest__.py not found")

except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
