from tkinter import messagebox

class ProfileManager:
    def route_audio(self, selected_app, selected_device):
        messagebox.showinfo("Routing Audio", f"Routing {selected_app} to {selected_device}")

    def save_profile(self, profile_name):
        if profile_name:
            messagebox.showinfo("Profile Saved", f"Profile '{profile_name}' saved!")
        else:
            messagebox.showwarning("Save Profile", "Please enter a profile name!")
