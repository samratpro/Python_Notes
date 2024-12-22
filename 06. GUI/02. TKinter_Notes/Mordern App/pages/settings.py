from customtkinter import *
import sqlite3

class SettingsPage(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.defult_website_name = 'https://websitename.com/'
        self.defult_userame_name = 'admin'
        self.defult_app_pass = 'xxxx xxxx xxxx xxxx'
        self.defult_category_name = 'Blog'
        self.defult_pixabay_api = 'xxxxxxxxxxxxxxxxxxx'
        self.defult_blogspot_api = 'xxxxxxxxxxxxxxxxxxx'
        self.defult_blogspot_id = '00000000000000000'
        self.defult_title_prompt = '''Write an SEO title about this keyword within 55 characters. The keyword must be included directly in the title keyword: <<keyword>>'''
        self.defult_intro_prompt = '''Write a compelling blog post introduction about the keyword: <<keyword>> The introduction should begin with technical terms related to the topic, avoiding casual phrases like "Are you...". The keyword should be naturally included throughout the introduction. Do not provide a direct solution in the intro. The final sentence should intrigue readers to continue reading the full article. Aim for a length of approximately 120 words. '''
        self.defult_outline_prompt = '''Generate an outline for an article that can cover all relevant topics on the keyword: <<keyword>> The outline consists of one H1 heading and multiple H2's with briefing. Only an outline needed, do not give answers, unnecessary words or notes. Do not give me "Overview", "Introduction" or "Conclusion" etc. others The outline should have the following format, between 8 to12, H2 section: <H1></H1> <h2></h2> - subtopic - subtopic - subtopic - subtopic <h2></h2> - subtopic - subtopic - subtopic - subtopic <h2></h2> - subtopic - subtopic - subtopic - subtopic <h2></h2> .........
                                    '''
        self.defult_content_prompt = '''I Want You To Act As A Content Writer Very Proficient SEO Writer. Do it step by step. Bold the Heading of the Article using Markdown language. At least 10 headings and write a 1000+ words 100% Unique, SEO-optimized, Human-Written article. Write The article In Your Own Words Rather Than Copying And Pasting From Other Sources. Consider perplexity and burstiness when creating content, ensuring high levels of both without losing specificity or context. Use fully detailed paragraphs that engage the reader. Write In A Conversational Style As Written By A Human (Use An Informal Tone, Utilize Personal Pronouns, Keep It Simple, Engage The Reader, Use The Active Voice, Keep It Brief, Use Rhetorical Questions, and Incorporate Analogies And Metaphors). And please don\'t give me introduction, conclusion and faq, I want just content body. Now Write An Article On This Topic: <<keyword>>''' 
        self.defult_faq_prompt = '''Write 5 FAQ with short answer within 1 sentence on this keyword: ((keyword))\nBold the Heading of using Markdown language. And please ignore here is your output or this type sentence. I want to just my targeted output'''
        self.defult_coclusion_prompt = "keyword: ((keyword))\nWrite an web article bottom summary\nAnd length approx 60 words\n"

        con = sqlite3.connect('postdb.db')
        cur = con.cursor()
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS Postdata (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Website_name CHAR(200),
                        User_name CHAR(200),
                        App_pass CHAR(200),
                        Category_name CHAR(200),
                        Pixabay_api CHAR(200),
                        Blogspot_api CHAR(200),
                        Blogspot_id CHAR(200),
                        Title_prompt TEXT,
                        Intro_prompt TEXT,
                        Outline_prompt TEXT,
                        Content_prompt TEXT,
                        Faq_prompt TEXT,
                        Conclusion_prompt TEXT
                    )  
                    ''')

        data_check = cur.execute('''SELECT Website_name FROM Postdata WHERE ID=1''').fetchone()
        print(data_check)

        if data_check is None:
            cur.execute('''
                INSERT INTO Postdata (
                    Website_name,
                    User_name,
                    App_pass,
                    Category_name,
                    Pixabay_api,
                    Blogspot_api,
                    Blogspot_id,
                    Title_prompt,
                    Intro_prompt,
                    Outline_prompt,
                    Content_prompt,
                    Faq_prompt,
                    Conclusion_prompt
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.defult_website_name,
                self.defult_userame_name,
                self.defult_app_pass,
                self.defult_category_name,
                self.defult_pixabay_api,
                self.defult_blogspot_api,
                self.defult_blogspot_id,
                self.defult_title_prompt,
                self.defult_intro_prompt,
                self.defult_outline_prompt,
                self.defult_content_prompt,
                self.defult_faq_prompt,
                self.defult_coclusion_prompt
            ))
            con.commit()


        print("Done")

        # Title Label
        label = CTkLabel(self, text="Settings Page", font=("Arial", 20))
        label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

          # Create a scrollable frame
        scrollable_frame = CTkScrollableFrame(self, width=500, height=400)
        scrollable_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Configure row and column weights for resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create Labels and Entries for each field inside the scrollable frame
        fields = [
                ("Website Name", "website_name_entry", "Website_name"),
                ("Username", "username_entry", "User_name"),
                ("App Password", "app_pass_entry", "App_pass"),
                ("Category Name", "category_name_entry", "Category_name"),
                ("Pixabay API", "pixabay_api_entry", "Pixabay_api"),
                ("Blogspot API", "blogspot_api_entry", "Blogspot_api"),
                ("Blogspot ID", "blogspot_id_entry", "Blogspot_id"),
                ("Title Prompt", "title_prompt_entry", "Title_prompt"),
                ("Intro Prompt", "intro_prompt_entry", "Intro_prompt"),
                ("Outline Prompt", "outline_prompt_entry", "Outline_prompt"),
                ("Content Prompt", "content_prompt_entry", "Content_prompt"),
                ("FAQ Prompt", "faq_prompt_entry", "Faq_prompt"),
                ("Conclusion Prompt", "conclusion_prompt_entry","Conclusion_prompt")
            ]

        self.entries = {}
        row = 0
        for field, var_name, db_value in fields:
            label = CTkLabel(scrollable_frame, text=field + ":")
            label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            if "Prompt" in field:
                entry = CTkTextbox(scrollable_frame, height=100, width=400)
                entry.insert("1.0", str(cur.execute(f'''SELECT {db_value} FROM Postdata WHERE ID=1''').fetchone()[0]))  # Insert the value from the database
            else:
                entry = CTkEntry(scrollable_frame, placeholder_text=f"Enter {field.lower()}")
                entry.insert(0, str(cur.execute(f'''SELECT {db_value} FROM Postdata WHERE ID=1''').fetchone()[0]))  # Insert the value from the database
            entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            self.entries[var_name] = entry
            row += 1

        # Save Button
        save_button = CTkButton(scrollable_frame, width=100, text="Save Changes", command=self.save_changes)
        save_button.grid(row=row, column=0, padx=(10, 5), pady=20, sticky="ew")

        # Reset Button
        reset_button = CTkButton(scrollable_frame, width=100, text="Reset Data", command=self.reset_data)
        reset_button.grid(row=row, column=1, padx=(5, 10), pady=20)

        con.close()

    def save_changes(self):
        # Gather all values from entries
        values = {var_name: entry.get(1.0, "end-1c") if isinstance(entry, CTkTextbox) else entry.get() for var_name, entry in self.entries.items()}

        con = sqlite3.connect('postdb.db')
        cur = con.cursor()
        cur.execute('''
            UPDATE Postdata SET
                Website_name = ?,
                User_name = ?,
                App_pass = ?,
                Category_name = ?,
                Pixabay_api = ?,
                Blogspot_api = ?,
                Blogspot_id = ?,
                Title_prompt = ?,
                Intro_prompt = ?,
                Outline_prompt = ?,
                Content_prompt = ?,
                Faq_prompt = ?,
                Conclusion_prompt = ?
            WHERE ID = 1
        ''', (
            values["website_name_entry"],
            values["username_entry"],
            values["app_pass_entry"],
            values["category_name_entry"],
            values["pixabay_api_entry"],
            values["blogspot_api_entry"],
            values["blogspot_id_entry"],
            values["title_prompt_entry"],
            values["intro_prompt_entry"],
            values["outline_prompt_entry"],
            values["content_prompt_entry"],
            values["faq_prompt_entry"],
            values["conclusion_prompt_entry"]
        ))
        con.commit()
        con.close()
        print(f"Saved settings: {values}")

    def reset_data(self):
        con = sqlite3.connect('postdb.db')
        cur = con.cursor()
        cur.executef(f'''
                        UPDATE Postdata
                        SET
                            Website_name = '{self.defult_website_name}',
                            User_name = '{self.defult_userame_name}',
                            App_pass = '{self.defult_app_pass}',
                            Category_name = '{self.defult_category_name}', 
                            Pixabay_api = '{self.defult_pixabay_api}',
                            Blogspot_api = '{self.defult_blogspot_api}',
                            Blogspot_id =  '{self.defult_blogspot_id}',
                            Title_prompt = {self.defult_title_prompt},
                            Intro_prompt = {self.defult_intro_prompt}?,
                            Outline_prompt = {self.defult_outline_prompt},
                            Content_prompt = {self.defult_content_prompt},
                            Faq_prompt = {self.defult_faq_prompt},
                            Conclusion_prompt = {self.defult_coclusion_prompt}
                        WHERE ID = 1

                        ''')
