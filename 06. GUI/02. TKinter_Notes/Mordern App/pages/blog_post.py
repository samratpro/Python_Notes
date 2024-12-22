from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkOptionMenu, CTkTextbox

class BlogPostPage(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Title Label
        label = CTkLabel(self, text="Blog Post Page", font=("Arial", 24))
        label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Blog Title Label and Entry
        title_label = CTkLabel(self, text="Blog Title:")
        title_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.title_entry = CTkEntry(self, placeholder_text="Enter blog title here")
        self.title_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Blog Content Label and Textbox
        content_label = CTkLabel(self, text="Blog Content:")
        content_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.content_textbox = CTkTextbox(self, height=10, width=40)
        self.content_textbox.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Category Selection (Dropdown)
        category_label = CTkLabel(self, text="Category:")
        category_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.category_option_menu = CTkOptionMenu(self, values=["Tech", "Lifestyle", "Health", "Education", "Business"])
        self.category_option_menu.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Publish Button
        publish_button = CTkButton(self, text="Publish", command=self.publish_post)
        publish_button.grid(row=4, column=0, columnspan=2, pady=20)

    def publish_post(self):
        # Placeholder function to handle publishing the blog post
        title = self.title_entry.get()
        content = self.content_textbox.get("1.0", "end-1c")  # Get all the content from the Textbox
        category = self.category_option_menu.get()

        # For now, just print the values (You can later connect this to a database or API)
        print(f"Publishing Blog Post: Title={title}, Category={category}")
        print(f"Content: {content}")
