import subprocess
import sys

# Try to install pinecone-client by directly calling pip's install method
try:
    subprocess.check_call([
        sys.executable, 
        "-m", 
        "pip", 
        "install", 
        "--disable-pip-version-check",
        "--no-warn-script-location",
        "pinecone-client"
    ], env={**dict(subprocess.os.environ), "PYTHONWARNINGS": "ignore"})
    print("Successfully installed pinecone-client")
except Exception as e:
    print(f"Installation failed: {e}")
    print("\nTrying alternative method...")
    
    # Alternative: try using ensurepip and upgrade pip first
    try:
        import pip._internal
        pip._internal.main(["install", "pinecone-client"])
        print("Successfully installed pinecone-client using internal method")
    except Exception as e2:
        print(f"Alternative method also failed: {e2}")
