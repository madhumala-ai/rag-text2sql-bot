import subprocess
import sys
import tempfile
import urllib.request
import os

def install_wheel_directly(package_name):
    """Download and install package wheel directly."""
    print(f"Attempting to install {package_name}...")
    
    # Try using easy_install as a fallback
    try:
        result = subprocess.run(
            [sys.executable, "-m", "easy_install", package_name],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"Successfully installed {package_name} using easy_install")
            return True
        else:
            print(f"easy_install failed: {result.stderr}")
    except Exception as e:
        print(f"easy_install not available: {e}")
    
    # Try downloading with pip download and installing manually
    try:
        temp_dir = tempfile.mkdtemp()
        print(f"Using temp directory: {temp_dir}")
        
        # Download the package
        download_result = subprocess.run(
            [sys.executable, "-m", "pip", "download", "--dest", temp_dir, package_name],
            capture_output=True,
            text=True,
            env={**os.environ, "PIP_NO_INPUT": "1"}
        )
        
        if download_result.returncode != 0:
            print(f"Download failed: {download_result.stderr}")
            return False
        
        # Find wheel files
        wheel_files = [f for f in os.listdir(temp_dir) if f.endswith('.whl') or f.endswith('.tar.gz')]
        
        if not wheel_files:
            print("No package files found")
            return False
        
        print(f"Found packages: {wheel_files}")
        
        # Install each wheel
        for wheel_file in wheel_files:
            wheel_path = os.path.join(temp_dir, wheel_file)
            install_result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--no-deps", "--no-index", wheel_path],
                capture_output=True,
                text=True
            )
            if install_result.returncode == 0:
                print(f"Installed {wheel_file}")
            else:
                print(f"Failed to install {wheel_file}: {install_result.stderr}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

# Try to install pinecone-client and grpcio
packages = ["pinecone-client", "grpcio", "grpcio-tools", "protobuf"]

for package in packages:
    try:
        __import__(package.replace("-", "_"))
        print(f"{package} is already installed")
    except ImportError:
        print(f"\n{'='*50}")
        print(f"Installing {package}")
        print('='*50)
        install_wheel_directly(package)

print("\n" + "="*50)
print("Installation attempt complete!")
print("="*50)
