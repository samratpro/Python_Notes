from tkinter import *


window = Tk()
window.title("Automation App")  # Title
window.geometry("900x600")   # Window Area

frame = Frame(window) # Main Frame
frame.pack()

from datetime import datetime
target_date = datetime(2024, 10, 10)
current_date = datetime.now()
if current_date <= target_date:
    print("ok")
else:
    print("expired")


if __name__ == '__main__':
    window.mainloop()
