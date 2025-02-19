from customtkinter import *
import sqlite3

class SettingsPage(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)



        self.default_chatgpt_api = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxx'
        self.default_chatgpt_model = 'model name'
        self.default_deepseek_api = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxx'
        self.default_deepseek_model = 'model name'
        self.default_gemni_api = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxx'
        self.default_gemni_model = 'model name'
        self.default_api_select = "ChatGPT"
        self.default_title_prompt = '''Write an SEO title about this keyword within 55 characters. The keyword must be included directly in the title keyword: ((keyword))'''
        self.default_intro_prompt = '''Write a compelling blog post introduction about the keyword: ((keyword)) The introduction should begin with technical terms related to the topic, avoiding casual phrases like "Are you...". The keyword should be naturally included throughout the introduction. Do not provide a direct solution in the intro. The final sentence should intrigue readers to continue reading the full article. Aim for a length of approximately 120 words. '''
        self.default_product_prompt = """
        default product section writing prompt
        """
        self.default_buying_outline_prompt = "default_buyin_outline_prompt \n"
        self.default_buying_paragraph_prompt = "default buying paragraph prompt"

        self.default_faq_prompt = "default faq prompt"
        self.default_conclusion_prompt = "default faq prompt"

        con = sqlite3.connect('postdb.db')
        cur = con.cursor()
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS Postdata (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        chatgpt_api CHAR(200),
                        chatgpt_model CHAR(200),
                        deepseek_api CHAR(200),
                        deepseek_model CHAR(200),
                        gemni_api CHAR(200),
                        gemni_model CHAR(200),
                        api_select CHAR(200),
                        title_prompt TEXT,
                        intro_prompt TEXT,
                        product_prompt TEXT,
                        buying_outline_prompt TEXT,
                        buying_paragraph_prompt TEXT,
                        faq_prompt TEXT,
                        conclusion_prompt TEXT
                    )  
                    ''')

        self.data_check = cur.execute('''SELECT chatgpt_api FROM Postdata WHERE ID=1''').fetchone()
        print(self.data_check)

        if self.data_check is None:
            cur.execute('''
                INSERT INTO Postdata (
                    chatgpt_api,
                    chatgpt_model,
                    deepseek_api,
                    deepseek_model,
                    gemni_api,
                    gemni_model,
                    api_select,
                    title_prompt,
                    intro_prompt,
                    product_prompt,
                    buying_outline_prompt,
                    buying_paragraph_prompt,
                    faq_prompt,
                    conclusion_prompt
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.default_chatgpt_api,
                self.default_chatgpt_model,
                self.default_deepseek_api,
                self.default_deepseek_model,
                self.default_gemni_api,
                self.default_gemni_model,
                self.default_api_select,
                self.default_title_prompt,
                self.default_intro_prompt,
                self.default_product_prompt,
                self.default_buying_outline_prompt,
                self.default_buying_paragraph_prompt,
                self.default_faq_prompt,
                self.default_conclusion_prompt
            ))
            con.commit()

        print("Done")

        # Title Label
        self.label = CTkLabel(self, text="Settings Page", font=("Arial", 20))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        # Create a scrollable frame
        self.scrollable_frame = CTkScrollableFrame(self, width=500, height=400, border_width=1)
        self.scrollable_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Configure row and column weights for resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create Labels and Entries for each field inside the scrollable frame
        self.fields = [
                ("ChatGPT API", "chatgpt_api_entry", "chatgpt_api"),
                ("ChatGPT model", "chatgpt_model_entry", "chatgpt_model"),
                ("DeepSeek API", "deepseek_api_entry", "deepseek_api"),
                ("DeepSeek model", "deepseek_model_entry", "deepseek_model"),
                ("Gemni API", "gemni_api_entry", "gemni_api"),
                ("Gemni model", "gemni_model_entry", "gemni_model"),
                ("Select API", "api_select_entry", "api_select"),
                ("title prompt", "title_prompt_entry", "title_prompt"),
                ("intro prompt", "intro_prompt_entry", "intro_prompt"),
                ("product prompt", "product_prompt_entry", "product_prompt"),
                ("buying outline prompt", "buying_outline_prompt_entry", "buying_outline_prompt"),
                ("buying paragraph prompt", "buying_paragraph_prompt_entry","buying_paragraph_prompt"),
                ("faq prompt", "faq_prompt_entry","faq_prompt"),
                ("conclusion prompt", "conclusion_prompt_entry","conclusion_prompt")
            ]

        self.entries = {}
        self.row = 0
        for field, var_name, db_value in self.fields:
            self.label = CTkLabel(self.scrollable_frame, text=field + ":")
            self.label.grid(row=self.row, column=0, padx=10, pady=5, sticky="w")
            if "prompt" in field:
                self.entry = CTkTextbox(self.scrollable_frame, height=150, width=400)
                self.entry.insert("1.0", str(cur.execute(f'''SELECT {db_value} FROM Postdata WHERE ID=1''').fetchone()[0]))  # Insert the value from the database
            elif "title" in field or "intro" in field:
                self.entry = CTkTextbox(self.scrollable_frame, height=100, width=400)
                self.entry.insert("1.0", str(cur.execute(f'''SELECT {db_value} FROM Postdata WHERE ID=1''').fetchone()[0]))  # Insert the value from the database
            elif "Select" in field:
                self.entry = CTkComboBox(self.scrollable_frame, state="readonly", values=['ChatGPT', 'DeepSeek', 'Gemni'], )
                self.entry.set(str(cur.execute(f'''SELECT {db_value} FROM Postdata WHERE ID=1''').fetchone()[0]))
                self.entry.configure()
            else:
                self.entry = CTkEntry(self.scrollable_frame, placeholder_text=f"Enter {field.lower()}")
                self.entry.insert(0, str(cur.execute(f'''SELECT {db_value} FROM Postdata WHERE ID=1''').fetchone()[0]))  # Insert the value from the database
            self.entry.grid(row=self.row, column=1, padx=10, pady=5, sticky="ew")
            self.entries[var_name] = self.entry
            self.row += 1

        # Add Save and Reset buttons
        self.save_button = CTkButton(self.scrollable_frame, width=100, text="Save Changes", command=self.save_changes)
        self.save_button.grid(row=self.row, column=0, padx=(10, 5), pady=(20,350), sticky="ew")

        self.reset_button = CTkButton(self.scrollable_frame, width=100, text="Reset Data", command=self.reset_data)
        self.reset_button.grid(row=self.row, column=1, padx=(5, 10), pady=(20, 350), sticky="ew")

        # Configure resizing behavior -- Responsive
        def on_resize(event):
            new_width = self.winfo_width()
            for entry_name, entry_widget in self.entries.items():
                if isinstance(entry_widget, CTkEntry) or isinstance(entry_widget, CTkTextbox):
                    if new_width < 800:
                        entry_widget.configure(width=400)  # Adjust width for smaller windows
                    elif new_width > 799 and new_width < 1200:
                        entry_widget.configure(width=600)
                    else:
                        entry_widget.configure(width=1000)  # Adjust width for larger windows

        self.bind("<Configure>", on_resize)
        con.close()

    def save_changes(self):
        # Gather all values from entries
        values = {var_name: entry.get(1.0, "end-1c") if isinstance(entry, CTkTextbox) else entry.get() for var_name, entry in self.entries.items()}

        con = sqlite3.connect('postdb.db')
        cur = con.cursor()
        cur.execute('''
            UPDATE Postdata SET
                chatgpt_api = ?,
                chatgpt_model = ?,
                deepseek_api = ?,
                deepseek_model = ?,
                gemni_api = ?,
                gemni_model = ?,
                api_select = ?,
                title_prompt = ?,
                intro_prompt = ?,
                product_prompt = ?,
                buying_outline_prompt = ?,
                buying_paragraph_prompt = ?,
                faq_prompt = ?,
                conclusion_prompt = ?
            WHERE ID = 1
        ''', (
            values["chatgpt_api_entry"],
            values["chatgpt_model_entry"],
            values["deepseek_api_entry"],
            values["deepseek_model_entry"],
            values["gemni_api_entry"],
            values["gemni_model_entry"],
            values["api_select_entry"],
            values["title_prompt_entry"],
            values["intro_prompt_entry"],
            values["product_prompt_entry"],
            values["buying_outline_prompt_entry"],
            values["buying_paragraph_prompt_entry"],
            values["faq_prompt_entry"],
            values["conclusion_prompt_entry"]
        ))
        con.commit()
        con.close()
        # print(f"Saved settings: {values}")

    def reset_data(self):
        """Reset data to default values."""
        try:
            # Connect to the database
            con = sqlite3.connect('postdb.db')
            cur = con.cursor()

            # Update the database with default values
            cur.execute('''
                UPDATE Postdata SET
                    chatgpt_api = ?,
                    chatgpt_model = ?,
                    deepseek_api = ?,
                    deepseek_model = ?,
                    gemni_api = ?,
                    gemni_model = ?,
                    api_select = ?,
                    title_prompt = ?,
                    intro_prompt = ?,
                    product_prompt = ?,
                    buying_outline_prompt = ?,
                    buying_paragraph_prompt = ?,
                    faq_prompt = ?,
                    conclusion_prompt = ?
                WHERE ID = 1
            ''', (
                self.default_chatgpt_api,
                self.default_chatgpt_model,
                self.default_deepseek_api,
                self.default_deepseek_model,
                self.default_gemni_api,
                self.default_gemni_model,
                self.default_api_select,
                self.default_title_prompt,
                self.default_intro_prompt,
                self.default_product_prompt,
                self.default_buying_outline_prompt,
                self.default_buying_paragraph_prompt,
                self.default_faq_prompt,
                self.default_conclusion_prompt
            ))

            # Commit the transaction
            con.commit()

            # Reset the UI entries to default values
            self.entries['chatgpt_api_entry'].delete(0, END)
            self.entries['chatgpt_api_entry'].insert(0, self.default_chatgpt_api)

            self.entries['chatgpt_model_entry'].delete(0, END)
            self.entries['chatgpt_model_entry'].insert(0, self.default_chatgpt_model)

            self.entries['deepseek_api_entry'].delete(0, END)
            self.entries['deepseek_api_entry'].insert(0, self.default_chatgpt_api)

            self.entries['deepseek_model_entry'].delete(0, END)
            self.entries['deepseek_model_entry'].insert(0, self.default_deepseek_model)

            self.entries['gemni_api_entry'].delete(0, END)
            self.entries['gemni_api_entry'].insert(0, self.default_chatgpt_api)

            self.entries['gemni_model_entry'].delete(0, END)
            self.entries['gemni_model_entry'].insert(0, self.default_gemni_model)

            self.entries['api_select_entry'].delete(0, END)
            self.entries['api_select_entry'].insert(0, self.default_gemni_model)

            self.entries['title_prompt_entry'].delete(0, END)
            self.entries['title_prompt_entry'].insert(0, self.default_title_prompt)

            self.entries['intro_prompt_entry'].delete(0, END)
            self.entries['intro_prompt_entry'].insert(0, self.default_intro_prompt)

            self.entries['product_prompt_entry'].delete(0, END)
            self.entries['product_prompt_entry'].insert(0, self.default_product_prompt)

            self.entries['buying_outline_prompt_entry'].delete(0, END)
            self.entries['buying_outline_prompt_entry'].insert(0, self.default_buying_outline_prompt)

            self.entries['buying_paragraph_prompt_entry'].delete(0, END)
            self.entries['buying_paragraph_prompt_entry'].insert(0, self.default_buying_paragraph_prompt)

            self.entries['faq_prompt_entry'].delete(0, END)
            self.entries['faq_prompt_entry'].insert(0, self.default_faq_prompt)

            self.entries['conclusion_prompt_entry'].delete(0, END)
            self.entries['conclusion_prompt_entry'].insert(0, self.default_conclusion_prompt)

        except Exception as e:
            print(f"Error in reset_data: {e}")

        finally:
            # Close the database connection
            if con:
                con.close()
        
