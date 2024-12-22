from customtkinter import *
from pages.settings import SettingsPage
from pages.blog_post import BlogPostPage
from pages.medium_post import MediumPostPage
from pages.linkedin_post import LinkedInPostPage
from pages.quora_post import QuoraPostPage
from pages.quora_answer import QuoraAnswerPage

set_appearance_mode("Light")  # Modes: "System" (default), "Dark", "Light"
set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

class DashboardApp(CTk):
    def __init__(self):
        super().__init__()

        self.title("CustomTkinter Dashboard")
        self.geometry("800x500")
        
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)  # Main content area
        self.grid_rowconfigure(0, weight=1)

        # Create Left Side Menu
        self.menu_frame = CTkFrame(self, width=200, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, sticky="nswe")

        self.create_menu_buttons()

        # Create Main Content Frame
        self.content_frame = CTkFrame(self, corner_radius=10)
        self.content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

        # Pages Dictionary
        self.pages = {
            "Settings": SettingsPage(self.content_frame),
            "Blog Post": BlogPostPage(self.content_frame),
            "Medium Post": MediumPostPage(self.content_frame),
            "LinkedIn Post": LinkedInPostPage(self.content_frame),
            "Quora Post": QuoraPostPage(self.content_frame),
            "Quora Answer": QuoraAnswerPage(self.content_frame),
        }

        # Default page
        self.show_page("Settings")

    def create_menu_buttons(self):
        """Creates buttons for the menu and adds them to the menu frame."""
        buttons = [
            ("Settings", "Settings"),
            ("Blog Post", "Blog Post"),
            ("Medium Post", "Medium Post"),
            ("LinkedIn Post", "LinkedIn Post"),
            ("Quora Post", "Quora Post"),
            ("Quora Answer", "Quora Answer"),
        ]

        for index, (label, page_name) in enumerate(buttons):
            button = CTkButton(
                self.menu_frame, 
                text=label, 
                command=lambda name=page_name: self.show_page(name)
            )
            button.grid(row=index, column=0, pady=10, padx=10, sticky="ew")

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
