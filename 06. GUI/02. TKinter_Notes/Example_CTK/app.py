from customtkinter import *
from pages.settings import SettingsPage
from pages.amazon import AmazonPage
from datetime import datetime


target_date = datetime(2024, 12, 13)
current_date = datetime.now()

set_appearance_mode("Light")  # Modes: "System" (default), "Dark", "Light"
set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

class DashboardApp(CTk):
    def __init__(self):
        super().__init__()

        self.title("Amazon App Dashboard")
        self.geometry("1000x700")
        
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)  # Main content area
        self.grid_rowconfigure(0, weight=1)

        # Create Left Side Menu
        self.menu_frame = CTkFrame(self, width=200, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, sticky="nswe")

        self.current_button = None  # Track the currently selected button
        self.menu_buttons = {}  # Store menu buttons for resetting colors

        self.create_menu_buttons()

        # Create Main Content Frame
        self.content_frame = CTkFrame(self, corner_radius=10)
        self.content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

        # Pages Dictionary
        self.pages = {
            "Settings": SettingsPage(self.content_frame),
            "Amazon Post": AmazonPage(self.content_frame),
        }

        # Default page
        self.show_page("Settings")

    def create_menu_buttons(self):
        """Creates buttons for the menu individually without a loop."""
        # Create Settings button
        settings_button = CTkButton(
            self.menu_frame,
            text="Settings",
            command=lambda: self.on_button_click("Settings", "Settings"),
            fg_color="black",
            hover_color="black",
        )
        settings_button.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
        self.menu_buttons["Settings"] = settings_button


        # Create Medium Post button
        Amazon_post_button = CTkButton(
            self.menu_frame,
            text="Amazon Post",
            command=lambda: self.on_button_click("Amazon Post", "Amazon Post"),
            fg_color=None,
            hover_color="black",
        )
        Amazon_post_button.grid(row=2, column=0, pady=10, padx=10, sticky="ew")
        self.menu_buttons["Amazon Post"] = Amazon_post_button


    def on_button_click(self, page_name, button_label):
        """Handles button click events."""
        self.show_page(page_name)

        # Reset the colors of all buttons
        for btn_label, btn in self.menu_buttons.items():
            btn.configure(fg_color="#3B8ED0")  # Reset to default

        # Highlight the selected button
        selected_button = self.menu_buttons.get(button_label)
        if selected_button:
            selected_button.configure(fg_color="black")
            self.current_button = selected_button

    def show_page(self, page_name):
        """Displays the selected page."""
        # Destroy existing widgets
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()

        # Add the selected page
        page = self.pages.get(page_name)
        if page:
            page.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()
