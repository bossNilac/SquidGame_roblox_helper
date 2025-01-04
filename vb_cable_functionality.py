import json
import os
import subprocess
import tkinter as tk
from tkinter import ttk

import keyboard as keyboard
from pydub import AudioSegment

import numpy as np
import sounddevice as sd

CONFIG_FILE = "config.json"

# Parameters
BUFFER_SIZE = 1024
FORMAT = 'int16'
CHANNELS = 1
SAMPLERATE = 44100


def play_sound_to_virtual_microphone(file_path, vb_cable_device="VB-CABLE"):
    """
    Play an MP3 file into the VB-CABLE Virtual Microphone (input device).
    """
    try:
        # Load the MP3 file using pydub
        audio = AudioSegment.from_file(file_path, format="mp3")

        # Convert the audio to a NumPy array (normalize to float32 for sounddevice)
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32) / (2 ** 15)
        sample_rate = audio.frame_rate

        # Get the list of available audio devices
        devices = sd.query_devices()

        # Find the VB-CABLE device
        vb_cable_index = next(
            (i for i, device in enumerate(devices) if
             vb_cable_device in device['name'] and device['max_input_channels'] > 0),
            None
        )

        if vb_cable_index is None:
            raise ValueError(f"VB-CABLE Virtual Microphone not found. Ensure VB-CABLE is installed and active.")

        print(f"VB-CABLE Virtual Microphone found: {devices[vb_cable_index]['name']}")
        print(f"Playing {file_path} to VB-CABLE Virtual Microphone...")

        # Play the audio to the VB-CABLE Virtual Microphone
        with sd.OutputStream(
                device=vb_cable_index,
                samplerate=sample_rate,
                channels=1  # Assuming mono input for the virtual mic
        ) as stream:
            # Stream the audio data in chunks
            chunk_size = 1024
            for start in range(0, len(samples), chunk_size):
                chunk = samples[start:start + chunk_size]
                stream.write(chunk)

        print("Playback complete.")
    except Exception as e:
        print(f"Error: {e}")


def route_microphone_to_vb_cable(selected_mic):
    # Input: Real microphone
    mic_device = selected_mic

    # Output: VB-CABLE
    vb_cable_device = 'VB-CABLE'

    def callback(indata, outdata, status):
        if status:
            print(status)
        outdata[:] = indata  # Directly route microphone input to VB-CABLE

    # Open stream
    with sd.Stream(device=(mic_device, vb_cable_device),
                   samplerate=SAMPLERATE,
                   channels=CHANNELS,
                   callback=callback):
        print("Routing microphone input to VB-CABLE. Press Ctrl+C to stop.")
        while True:
            pass


def list_microphones():
    """List all available input devices."""
    devices = sd.query_devices()
    return [dev['name'] for dev in devices if dev['max_input_channels'] > 0]


def save_selected_microphone(selected_mic):
    """Save the selected microphone to the config file."""
    config = {}

    # Load existing config if it exists
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)

    # Add the selected microphone to the config
    config["real_microphone"] = selected_mic
    route_microphone_to_vb_cable(selected_mic)

    # Save the updated config
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)
    return selected_mic


def on_select(root):
    """Handle microphone selection."""
    selected_mic = mic_combobox.get()
    if selected_mic:
        print(f"Selected Microphone: {selected_mic}")
        save_selected_microphone(selected_mic)
        print("Microphone saved to config file.")
        root.destroy()  # Close the app
    else:
        print("No microphone selected.")


def start_app():
    """Create the GUI application."""
    # Initialize the main window
    root = tk.Tk()
    root.title("Microphone Selector")
    root.geometry("400x200")

    # Create a label
    label = tk.Label(root, text="Select Your Real Microphone:", font=("Arial", 14))
    label.pack(pady=10)

    # Fetch available microphones
    mic_list = list_microphones()

    # Create a combo box for microphone selection
    global mic_combobox
    mic_combobox = ttk.Combobox(root, values=mic_list, state="readonly", width=40)
    mic_combobox.pack(pady=10)

    # Set default value if there are microphones available
    if mic_list:
        mic_combobox.set(mic_list[0])

    # Create a button to confirm the selection
    select_button = tk.Button(root, text="Select", command=lambda: on_select(root), font=("Arial", 12))
    select_button.pack(pady=20)

    # Start the GUI event loop
    root.mainloop()


def set_vb_cable_as_default_mic():
    try:
        # Use PowerShell to set VB-CABLE as the default microphone
        subprocess.run(
            [
                "powershell",
                "-Command",
                "(Get-PnpDevice | Where-Object { $_.FriendlyName -like '*VB-CABLE*' -and $_.Class -eq 'AudioEndpoint' -and $_.Status -eq 'OK' }).SetAsDefault()"
            ],
            check=True
        )
        print("VB-CABLE set as the default microphone.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set VB-CABLE as default microphone: {e}")


if __name__ == '__main__':
    start_app()
