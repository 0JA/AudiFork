import tkinter as tk
from tkinter import ttk, messagebox
from audio_device_manager import AudioDeviceManager
from application_manager import ApplicationManager
from profile_manager import ProfileManager
import sounddevice as sd
from pycaw.pycaw import AudioUtilities

class AudioRouterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.audio_device_manager = AudioDeviceManager()
        self.application_manager = ApplicationManager()
        self.profile_manager = ProfileManager()

        self.title("Audio Router")
        self.geometry("900x600")

        # Frame for Device Details
        self.device_detail_frame = ttk.LabelFrame(self, text="Device Details", padding=(10, 5))
        self.device_detail_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # Frame for Application Details
        self.app_detail_frame = ttk.LabelFrame(self, text="Application Details", padding=(10, 5))
        self.app_detail_frame.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # Frame for Device Handling
        self.device_frame = ttk.LabelFrame(self, text="Devices", padding=(10, 5))
        self.device_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.device_listbox = tk.Listbox(self.device_frame)
        self.device_listbox.pack(fill=tk.BOTH, expand=True)
        self.audio_device_manager.populate_devices(self.device_listbox)

        self.device_mute_button = ttk.Button(self.device_frame, text="Mute Device", command=lambda: self.audio_device_manager.mute_device(self.device_listbox.get(tk.ACTIVE)))
        self.device_mute_button.pack(pady=5)

        self.device_unmute_button = ttk.Button(self.device_frame, text="Unmute Device", command=lambda: self.audio_device_manager.unmute_device(self.device_listbox.get(tk.ACTIVE)))
        self.device_unmute_button.pack(pady=5)

        # Frame for Audio Management
        self.audio_frame = ttk.LabelFrame(self, text="Active Applications", padding=(10, 5))
        self.audio_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.audio_tree = ttk.Treeview(self.audio_frame, columns=('Application'), show='headings')
        self.audio_tree.heading('Application', text='Application')
        self.audio_tree.pack(fill=tk.BOTH, expand=True)
        self.application_manager.populate_audio_streams(self.audio_tree)

        self.audio_mute_button = ttk.Button(self.audio_frame, text="Mute App", command=lambda: self.application_manager.mute_audio_stream(self.audio_tree.item(self.audio_tree.selection())['values'][0], AudioUtilities.GetAllSessions()))
        self.audio_mute_button.pack(pady=5)

        self.audio_unmute_button = ttk.Button(self.audio_frame, text="Unmute App", command=lambda: self.application_manager.unmute_audio_stream(self.audio_tree.item(self.audio_tree.selection())['values'][0], AudioUtilities.GetAllSessions()))
        self.audio_unmute_button.pack(pady=5)

        # Frame for User Profiles
        self.profile_frame = ttk.LabelFrame(self, text="Profiles", padding=(10, 5))
        self.profile_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.profile_combobox = ttk.Combobox(self.profile_frame)
        self.profile_combobox.pack(fill=tk.X)

        # Buttons
        self.route_button = ttk.Button(self, text="Route Audio", command=lambda: self.profile_manager.route_audio(self.audio_tree.item(self.audio_tree.selection())['values'][0], self.device_listbox.get(tk.ACTIVE)))
        self.route_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.save_profile_button = ttk.Button(self, text="Save Profile", command=lambda: self.profile_manager.save_profile(self.profile_combobox.get()))
        self.save_profile_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Bind listbox and treeview to update detail frames
        self.device_listbox.bind('<<ListboxSelect>>', self.update_device_details)
        self.audio_tree.bind('<<TreeviewSelect>>', self.update_app_details)

        self.volume_progress = None
        self.volume_progress = ttk.Progressbar(self.app_detail_frame, orient='horizontal', length=200, mode='determinate') # Dont understand any of these settings 10/10
        self.volume_progress.pack() # wtf does pack do?
        

    def update_device_details(self, event): # event?
        selected_device_index = self.device_listbox.curselection()[0] # why 0
        device_info = sd.query_devices()[selected_device_index] # I think I get it

        # Clear previous details
        for widget in self.device_detail_frame.winfo_children():
            widget.destroy()

        # Display new details
        ttk.Label(self.device_detail_frame, text=f"Selected Device: {device_info['name']}").pack()
        ttk.Label(self.device_detail_frame, text=f"Sample Rate: {device_info['default_samplerate']} Hz").pack()
        ttk.Label(self.device_detail_frame, text=f"Max Input Channels: {device_info['max_input_channels']}").pack()
        ttk.Label(self.device_detail_frame, text=f"Max Output Channels: {device_info['max_output_channels']}").pack()
        ttk.Label(self.device_detail_frame, text=f"Latency: {device_info['default_low_output_latency']} s").pack()

    def update_app_details(self, event):
        selected_app = self.audio_tree.item(self.audio_tree.selection())['values'][0]
        sessions = AudioUtilities.GetAllSessions()
        
        # Clear previous details
        for widget in self.app_detail_frame.winfo_children():
            widget.destroy()

        # Initialize Progress Bar
        self.volume_progress = ttk.Progressbar(self.app_detail_frame, orient='horizontal', length=200, mode='determinate')
        self.volume_progress.pack()

        # Initialize Labels
        self.volume_percent_label = ttk.Label(self.app_detail_frame, text="")
        self.volume_percent_label.pack()

        self.mute_status_label = ttk.Label(self.app_detail_frame, text="")
        self.mute_status_label.pack()

        self.update_volume_progress()

        # Display new details
        for session in sessions:
            app_name = session.Process and session.Process.name() or 'System Sounds'
            if app_name == selected_app:
                volume = session.SimpleAudioVolume
                volume_percent = round(volume.GetMasterVolume() * 100, 1)
                self.volume_progress['value'] = volume_percent
                self.volume_percent_label.config(text=f"Current Volume: {volume_percent}%")

                mute_status = "Muted" if volume.GetMute() else "Unmuted"
                self.mute_status_label.config(text=f"Mute Status: {mute_status}")

                break

    def update_volume_progress(self):
        if not hasattr(self, 'volume_percent_label') or not hasattr(self, 'mute_status_label'):
            return

        selected_app = self.audio_tree.item(self.audio_tree.selection())['values'][0]
        sessions = AudioUtilities.GetAllSessions()

        for session in sessions:
            app_name = session.Process and session.Process.name() or 'System Sounds'
            if app_name == selected_app:
                volume = session.SimpleAudioVolume
                volume_percent = round(volume.GetMasterVolume() * 100, 1)
                self.volume_progress['value'] = volume_percent
                self.volume_percent_label.config(text=f"Current Volume: {volume_percent}%")
                self.mute_status_label.config(text="Muted" if volume.GetMute() else "Unmuted")
                break

        # Schedule the update every 500 milliseconds (adjust as needed)
        self.after(1, self.update_volume_progress)
