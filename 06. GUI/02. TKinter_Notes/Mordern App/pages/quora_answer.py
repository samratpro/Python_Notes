from customtkinter import CTkFrame, CTkLabel

class QuoraAnswerPage(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = CTkLabel(self, text="Quora Ans Page", font=("Arial", 24))
        label.pack(expand=True)
