import os
import shutil

def read_env_file(env_file_path):
    """Read environment variables from a .env file."""
    if not os.path.exists(env_file_path):
        raise FileNotFoundError(f"{env_file_path} not found.")
    
    with open(env_file_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

def ensure_migrations_folder(app_name):
    """Ensure the migrations folder and __init__.py exist for a given app."""
    migrations_path = os.path.join(app_name, 'migrations')
    init_file = os.path.join(migrations_path, '__init__.py')
    
    if not os.path.exists(migrations_path):
        os.makedirs(migrations_path)
        print(f"Created migrations directory: {migrations_path}")
    
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('')
        print(f"Created __init__.py in {migrations_path}")

def delete_migration_files(app):
    """Delete migration files (except __init__.py) and __pycache__ directories for the given app."""
    base_dir = os.getcwd()  # Get the current directory dynamically
    app_dir = os.path.join(base_dir, app)

    # Deleting migration files
    migrations_path = os.path.join(app_dir, 'migrations')
    if os.path.exists(migrations_path):
        for root, dirs, files in os.walk(migrations_path):
            for file_name in files:
                if file_name != '__init__.py':  # Keep the __init__.py
                    file_path = os.path.join(root, file_name)
                    try:
                        shutil.rmtree(file_path)
                        print(f"Deleted migration file: {file_path}")
                    except Exception as Ops:
                        print(Ops)
            
            # Deleting __pycache__ inside migrations
            for dir_name in dirs:
                if dir_name == '__pycache__':
                    pycache_path = os.path.join(root, dir_name)
                    try:
                        shutil.rmtree(pycache_path)
                        print(f"Deleted __pycache__ directory: {pycache_path}")
                    except Exception as Ops:
                        print(Ops)
    
    # Deleting __pycache__ directly under the app directory
    pycache_app_dir = os.path.join(app_dir, '__pycache__')
    if os.path.exists(pycache_app_dir):
        try:
            os.rmdir(pycache_app_dir)
            print(f"Deleted __pycache__ directory in {app}")
        except Exception as Ops:
            print(Ops)

def main():
    # Path to the .env file
    read_env_file('.env')
   
    apps = os.getenv('APPS', '').split()
    print(f"Apps to process: {apps}")
    
    for app in apps:
        ensure_migrations_folder(app)
        delete_migration_files(app)

if __name__ == '__main__':
    main()
