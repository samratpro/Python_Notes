import os
import shutil
import subprocess


EXCLUDE_DIRS = ['venv', '.git', '__pycache__', 'dist']
def log_message(message):
    print(message)


def obfuscate_file(file_path, output_dir):
    try:
        # Generate the output directory structure
        relative_path = os.path.relpath(file_path, start='.')
        output_path = os.path.join(output_dir, os.path.dirname(relative_path))
        os.makedirs(output_path, exist_ok=True)
        # Obfuscate the file
        log_message(f"Obfuscating file: {file_path}")
        subprocess.run(["pyarmor", "gen", "-O", output_path, file_path], check=True, encoding='utf-8')
        project_file = os.path.join(output_path, os.path.basename(file_path) + ".json")
        subprocess.run(["pyarmor", "cfg", project_file], check=True, encoding='utf-8')
        log_message(f"Successfully obfuscated: {file_path}")
    except subprocess.CalledProcessError as e:
        log_message(f"Error obfuscating file: {file_path}. Error: {e}")

def obfuscate_directory(directory, output_dir):
    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith(".py") and file not in ["replace_with_obfuscated.py", "setup.py", "convert_to_utf8.py"]:
                file_path = os.path.join(root, file)
                obfuscate_file(file_path, output_dir)


def move_obfuscated_files(src_dir, dest_dir):
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, os.path.relpath(src_file, start=src_dir))
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.move(src_file, dest_file)
            log_message(f"Moved obfuscated file: {src_file} to {dest_file}")


if __name__ == "__main__":
    source_directory = "."
    obfuscated_directory = "dist"
    # Step 1: Obfuscate the source code
    log_message("Starting obfuscation process...")
    obfuscate_directory(source_directory, obfuscated_directory)
    # Step 2: Move the obfuscated files to the original location, replacing original files
    log_message("Moving obfuscated files to original locations...")
    move_obfuscated_files(obfuscated_directory, source_directory)
    log_message("Source code replaced with obfuscated files.")