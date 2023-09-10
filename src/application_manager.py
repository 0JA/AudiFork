from pycaw.pycaw import AudioUtilities
from tkinter import messagebox

class ApplicationManager:
    def populate_audio_streams(self, audio_tree):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            app_name = session.Process and session.Process.name() or 'System Sounds'
            audio_tree.insert('', 'end', values=(app_name,))

    def mute_audio_stream(self, selected_app, sessions):
        for session in sessions:
            app_name = session.Process and session.Process.name() or 'System Sounds'
            if app_name == selected_app:
                volume = session.SimpleAudioVolume
                volume.SetMute(1, None)
                return

    def unmute_audio_stream(self, selected_app, sessions):
        for session in sessions:
            app_name = session.Process and session.Process.name() or 'System Sounds'
            if app_name == selected_app:
                volume = session.SimpleAudioVolume
                volume.SetMute(0, None)
                return
