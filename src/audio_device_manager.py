import sounddevice as sd
from tkinter import messagebox

class AudioDeviceManager:
    def populate_devices(self, device_listbox):
        devices = sd.query_devices()
        for device in devices:
            device_listbox.insert("end", device['name'])

    def mute_device(self, selected_device):
        # Here you would put the code that actually mutes the device using the sounddevice or another library.
        # For now, a messagebox will indicate what would happen.
        messagebox.showinfo("Mute Device", f"Muting {selected_device}")

    def unmute_device(self, selected_device):
        # Here you would put the code that actually unmutes the device using the sounddevice or another library.
        # For now, a messagebox will indicate what would happen.
        messagebox.showinfo("Unmute Device", f"Unmuting {selected_device}")
