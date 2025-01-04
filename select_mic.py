import json
import os
import tkinter as tk
from tkinter import ttk

import sounddevice as sd

from main import start_main_app

CONFIG_FILE = "res/config.json"

# Parameters
SAMPLERATE = 44100
CHANNELS = 1


def list_microphones():
    """
    List all available input devices with their indices.
    """
    devices = sd.query_devices()
    mic_list = [(i, dev['name'], dev['hostapi']) for i, dev in enumerate(devices) if dev['max_input_channels'] > 0]
    return mic_list


def save_selected_microphone(selected_mic_index):
    """
    Save the selected microphone to the config file.
    """
    config = {}

    # Load existing config if it exists
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)

    # Add the selected microphone to the config
    config["real_microphone_index"] = selected_mic_index

    # Save the updated config
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

    return selected_mic_index


def on_select(root, mic_combobox):
    """
    Handle microphone selection.
    """
    try:
        selected_item = mic_combobox.get()
        selected_index = int(selected_item.split(":")[0])  # Extract the index from the combobox entry
        print(f"Selected Microphone Index: {selected_index}")
        save_selected_microphone(selected_index)
        print("Microphone saved to config file.")
        root.destroy()  # Close the app
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





def start_app():
    """
    Create the GUI application.
    """
    # Initialize the main window
    root = tk.Tk()
    root.title("Microphone Selector")
    root.geometry("500x250")

    # Create a label
    label = tk.Label(root, text="Select Your Real Microphone:", font=("Arial", 16))
    label.pack(pady=10)

    # Fetch available microphones
    mic_list = list_microphones()

    # Create a combobox for microphone selection
    mic_combobox = ttk.Combobox(root, state="readonly", font=("Arial", 12), width=50)
    mic_combobox.pack(pady=10)

    # Populate the combobox with microphone options
    mic_combobox["values"] = tuple(f"{index}: {name} ({api})" for index, name, api in mic_list)

    # Set default value if there are microphones available
    if mic_list:
        mic_combobox.set(mic_combobox["values"][0])

    # Create a button to confirm the selection
    select_button = tk.Button(root, text="Select", command=lambda: on_select(root, mic_combobox),
                              font=("Arial", 14), bg="green", fg="white")
    select_button.pack(pady=20)

    # Start the GUI event loop
    root.mainloop()


if __name__ == '__main__':
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
            if config["real_microphone_index"] is not None:
                start_main_app(config["real_microphone_index"])
            else:
                start_app()
    else:
        start_app()



