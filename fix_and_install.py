import sys
import os

# Patch the platformdirs module before pip tries to use it
try:
    import pip._vendor.platformdirs.windows as windows_dirs
    
    # Save the original function
    original_get_win_folder = windows_dirs.get_win_folder_from_registry
    
    # Create a patched version that returns a default path
    def patched_get_win_folder(csidl_name):
        try:
            return original_get_win_folder(csidl_name)
        except:
            # Return a default path when registry lookup fails
            if csidl_name == "CSIDL_COMMON_APPDATA":
                return "C:\\ProgramData"
            elif csidl_name == "CSIDL_APPDATA":
                return os.path.expanduser("~\\AppData\\Roaming")
            elif csidl_name == "CSIDL_LOCAL_APPDATA":
                return os.path.expanduser("~\\AppData\\Local")
            else:
                return os.path.expanduser("~")
    
    # Apply the patch
    windows_dirs.get_win_folder_from_registry = patched_get_win_folder
    print("Successfully patched platformdirs")
    
    # Now try to use pip
    import pip._internal
    exit_code = pip._internal.main(["install", "pinecone-client"])
    
    if exit_code == 0:
        print("\nSuccessfully installed pinecone-client!")
    else:
        print(f"\nInstallation failed with exit code: {exit_code}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
