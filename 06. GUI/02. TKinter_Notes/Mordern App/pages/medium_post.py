from customtkinter import CTkFrame, CTkLabel

class MediumPostPage(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = CTkLabel(self, text="Medium Post Page", font=("Arial", 24))
        label.pack(expand=True)
