from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkOptionMenu

class SettingsPage(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Title Label
        label = CTkLabel(self, text="Settings Page", font=("Arial", 24))
        label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Username Label and Entry
        username_label = CTkLabel(self, text="Username:")
        username_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.username_entry = CTkEntry(self, placeholder_text="Enter your username")
        self.username_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Email Label and Entry
        email_label = CTkLabel(self, text="Email:")
        email_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = CTkEntry(self, placeholder_text="Enter your email")
        self.email_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Role Selection (Example Dropdown)
        role_label = CTkLabel(self, text="Role:")
        role_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.role_option_menu = CTkOptionMenu(self, values=["Admin", "User", "Guest"])
        self.role_option_menu.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Save Button
        save_button = CTkButton(self, text="Save Changes", command=self.save_changes)
        save_button.grid(row=4, column=0, columnspan=2, pady=20)

    def save_changes(self):
        # Placeholder function to handle saving changes
        username = self.username_entry.get()
        email = self.email_entry.get()
        role = self.role_option_menu.get()

        # For now, just print the values (You can later connect this to your database)
        print(f"Saved settings: Username={username}, Email={email}, Role={role}")
