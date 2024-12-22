from customtkinter import CTkFrame, CTkLabel

class LinkedInPostPage(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = CTkLabel(self, text="Linkedin Page", font=("Arial", 24))
        label.pack(expand=True)
