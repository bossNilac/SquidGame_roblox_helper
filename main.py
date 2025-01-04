import threading
import tkinter as tk

import keyboard
import numpy as np
import sounddevice as sd
from pydub import AudioSegment


def get_device_channels(device_name):
    """
    Get the number of input and output channels for a specific device.
    """
    devices = sd.query_devices()
    for device in devices:
        if device_name in device['name']:
            input_channels = device['max_input_channels']
            output_channels = device['max_output_channels']
            return input_channels, output_channels
    raise ValueError(f"Device '{device_name}' not found.")


def play_sound_to_virtual_microphone(file_path, vb_cable_device="CABLE Output"):
    """
    Play an MP3 or WAV file into the VB-CABLE Virtual Microphone (input device).
    """
    try:
        # Load the audio file using pydub
        audio = AudioSegment.from_file(file_path)

        # Ensure the audio is converted to mono if the device only supports mono
        input_channels, output_channels = get_device_channels(vb_cable_device)
        print(
            f"Device '{vb_cable_device}' supports {input_channels} input channel(s) and {output_channels} output channel(s).")

        if output_channels < audio.channels:
            print(f"Converting audio to {output_channels} channel(s)...")
            audio = audio.set_channels(output_channels)

        # Convert the audio to a NumPy array (normalize to float32 for sounddevice)
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32) / (2 ** 15)
        sample_rate = audio.frame_rate

        # Get the list of available audio devices
        devices = sd.query_devices()

        # Find the VB-CABLE device
        vb_cable_index = next(
            (i for i, device in enumerate(devices) if
             vb_cable_device in device['name'] and device['max_output_channels'] > 0),
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
                channels=output_channels  # Dynamically set to device's output channels
        ) as stream:
            # Stream the audio data in chunks
            chunk_size = 1024
            for start in range(0, len(samples), chunk_size):
                chunk = samples[start:start + chunk_size]
                stream.write(chunk)

        print("Playback complete.")
    except Exception as e:
        print(f"Error: {e}")


def get_microphone_name(index):
    """
    Get the name of a microphone by its index.
    """
    devices = sd.query_devices()
    if 0 <= index < len(devices):
        return devices[index]['name']
    else:
        raise ValueError(f"Invalid device index: {index}")


def set_sound():
    mp3_file_path = "res/mixkit-arcade-retro-game-over-213.wav"  # Replace with the path to your MP3 file

    print("Press F3 to play the sound to VB-CABLE Virtual Microphone...")
    keyboard.add_hotkey("f3", lambda: play_sound_to_virtual_microphone(mp3_file_path))


thread2 = threading.Thread(target=set_sound)  #
thread2.start()


def start_main_app(selected_mic_index):
    main_app = tk.Tk()
    main_app.title("Main Application")
    main_app.geometry("500x250")

    # Display the selected microphone
    label = tk.Label(main_app, text=f"Selected Microphone : {get_microphone_name(selected_mic_index)}",
                     font=("Arial", 16))
    label.pack(pady=20)

    # Add more features in the main app here
    tk.Label(main_app, text="Welcome to the Main Application!", font=("Arial", 14)).pack(pady=10)

    # Exit button
    tk.Button(main_app, text="Exit", command=main_app.destroy, font=("Arial", 12), bg="red", fg="white").pack(pady=20)

    # Run the main app
    main_app.mainloop()
