import ctypes
import struct
import sys
import zipfile
import os
import subprocess


def extract_vb_cable(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            print(f"Extracted VB-CABLE to: {extract_to}")
    except Exception as e:
        print(f"Error extracting VB-CABLE: {e}")


def find_installer(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if struct.calcsize("P") * 8 == 64:
                if "VBCABLE_Setup_x64" in file and file.endswith(".exe"):
                    return os.path.join(root, file)
            else:
                if "VBCABLE_Setup" in file and file.endswith(".exe"):
                    return os.path.join(root, file)
    return None


def install_vb_cable(installer_path):
    try:
        if not installer_path:
            raise FileNotFoundError("Installer not found.")

        print(f"Installing VB-CABLE using: {installer_path}")
        result = subprocess.run([installer_path, "/S"], check=True)
        print("VB-CABLE installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during VB-CABLE installation: {e}")
    except Exception as e:
        print(f"General error: {e}")


def is_admin():
    """Check if the script is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def show_popup_and_wait(title, message):
    """Display a Windows popup and block execution until a button is pressed."""
    # 1 = OK, 2 = Cancel
    response = ctypes.windll.user32.MessageBoxW(
        0, message, title, 1  # 1 = OK and Cancel buttons
    )
    return response


# Example usage



def main():
    if not is_admin():
        # Relaunch the script with elevated privileges
        print("Re-launching the script with administrator privileges...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()
    zip_path = "res/VBCABLE_Driver_Pack45.zip"
    extract_to = os.path.join(os.environ["USERPROFILE"], "Desktop/vb_cable")
    response = show_popup_and_wait("Confirmation Required", "Do you want to install VBCable(needed for GreenLight mod)?")
    if response == 1:  # OK button pressed
        print("User pressed OK. Program continues...")
    else:  # Cancel button pressed
        print("User pressed Cancel. Program exits.")
        sys.exit()
    extract_vb_cable(zip_path, extract_to)
    installer_path = find_installer(extract_to)
    install_vb_cable(installer_path)
    input()

