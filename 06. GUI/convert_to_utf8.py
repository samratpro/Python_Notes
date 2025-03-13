import os
EXCLUDE_DIRS = ['venv', '.git', '__pycache__', 'dist']
def convert_to_utf8(file_path):
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content.decode('utf-8'))
        print(f"Converted {file_path} to UTF-8 encoding.")
    except Exception as e:
        print(f"Error converting {file_path} to UTF-8: {e}")



def convert_directory_to_utf8(directory):
    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith('.py') and file not in ["replace_with_obfuscated.py", "setup.py", "convert_to_utf8.py"]:
                file_path = os.path.join(root, file)
                convert_to_utf8(file_path)

if __name__ == "__main__":
    source_directory = "."
    convert_directory_to_utf8(source_directory)