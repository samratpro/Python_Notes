from components import *
from customtkinter import *
import sqlite3
import base64
import threading
import webbrowser



con = sqlite3.connect('postdb.db')
cur = con.cursor()
cur.execute('''
            CREATE TABLE IF NOT EXISTS Postdata (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Website_name CHAR(200),
                User_name CHAR(200),
                App_pass CHAR(200),
                Category_name CHAR(200),
                Openai_api CHAR(200),
                pixabay_api CHAR(200),
                blogspot_api CHAR(200),
                blogspot_id CHAR(200),
                chatgpt_email CHAR(200),
                chatgpt_pass CHAR(200),
                gologin_api CHAR(200),
                gologin_id CHAR(200),
                Openai_model CHAR(200), 
                Content_generator TEXT,
                Intro_generator TEXT,
                faq_generator TEXT,
                conclusion_generator  TEXT,
                title_generator TEXT    
            )  
            ''')

data_check = cur.execute('''SELECT Website_name FROM Postdata WHERE ID=1''').fetchone()
print(data_check)

if data_check is None:
    cur.execute('''
        INSERT INTO Postdata(
            Website_name,
            User_name,
            App_pass,
            Category_name,
            Openai_api,
            Pixabay_api,
            blogspot_api,
            blogspot_id,
            chatgpt_email,
            chatgpt_pass,
            gologin_api,
            gologin_id,
            Openai_model,
            Content_generator,
            Intro_generator,
            faq_generator,
            conclusion_generator,
            title_generator
        ) VALUES (
            '',
            'wp username',
            'app pass token',
            'category name',
            'Openai Key',
            'pexels_api',
            'blogspot_api',
            'blogspot_id',
            'chatgpt_email',
            'chatgpt_pass',
            'gologin_api',
            'gologin_id',
            'gpt-3.5-turbo',
            "I Want You To Act As A Content Writer Very Proficient SEO Writer. Do it step by step. Bold the Heading of the Article using Markdown language. At least 10 headings and write a 1000+ words 100% Unique, SEO-optimized, Human-Written article. Write The article In Your Own Words Rather Than Copying And Pasting From Other Sources. Consider perplexity and burstiness when creating content, ensuring high levels of both without losing specificity or context. Use fully detailed paragraphs that engage the reader. Write In A Conversational Style As Written By A Human (Use An Informal Tone, Utilize Personal Pronouns, Keep It Simple, Engage The Reader, Use The Active Voice, Keep It Brief, Use Rhetorical Questions, and Incorporate Analogies And Metaphors). And please don\'t give me introduction, conclusion and faq, I want just content body. Now Write An Article On This Topic: ((keyword))",
            "Write a introduction on this keyword intro start with technical terms, not like are you and keyword must be include in output do not give me direct solution in intro section, intro last sentence must be interesting to read the full article, keyword: ((keyword))\nAnd length approx 100 words\n",
            "Write 5 FAQ with short answer within 1 sentence on this keyword: ((keyword))\nBold the Heading of using Markdown language. And please ignore here is your output or this type sentence. I want to just my targeted output",
            "keyword: ((keyword))\nWrite an web article bottom summary\nAnd length approx 60 words\n",
            "Write an SEO title on this keyword within 55 characters and the keyword must be directly included in the title\nkeyword: ((keyword))\n"
        )
    ''')

# TK part
window = CTk()
set_default_color_theme("green")
set_appearance_mode("light")
window.title("Shikhbo Academy - Multi Command")
window.geometry("1100x700")
window.wm_iconbitmap()

# Create a Frame + Content Frame with scrollbar
frame = CTkFrame(window)
frame.pack(fill=BOTH, expand=True)
canvas = CTkCanvas(frame)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
canvas.bind_all("<MouseWheel>", lambda event: on_mousewheel(event))  # Labda have to use when function is below
scrollbar = CTkScrollbar(frame, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
content_frame = CTkFrame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor=NW)

# website info widgets
webinfo_frame = CTkFrame(content_frame)
webinfo_frame.grid(pady=10, padx=20)

# label section
website_name = CTkLabel(webinfo_frame, text="Website Name")
website_name.grid(row=0, column=0, padx=10, pady=3)
website_entry = CTkEntry(webinfo_frame, width=180, border_width=1)
website_entry.insert(0,
                     str(cur.execute('''SELECT Website_name FROM Postdata WHERE ID=1''').fetchone()[0]))  # Default data
website_entry.grid(row=1, column=0, padx=10, pady=10)

user_name = CTkLabel(webinfo_frame, text="User Name")
user_name.grid(row=0, column=1, padx=10, pady=3)
username_entry = CTkEntry(webinfo_frame, width=90, border_width=1)
username_entry.insert(0, str(cur.execute('''SELECT User_name FROM Postdata WHERE ID=1''').fetchone()[0]))
username_entry.grid(row=1, column=1, padx=10, pady=10)

app_pass = CTkLabel(webinfo_frame, text="Application Password")
app_pass.grid(row=0, column=2, padx=10, pady=3)
app_pass_entry = CTkEntry(webinfo_frame, width=180, border_width=1)
app_pass_entry.insert(0, str(cur.execute('''SELECT App_pass FROM Postdata WHERE ID=1''').fetchone()[0]))
app_pass_entry.grid(row=1, column=2, padx=10, pady=10)

category_label = CTkLabel(webinfo_frame, text="Category")
category_label.grid(row=0, column=3, padx=10, pady=3)
category = CTkEntry(webinfo_frame, width=100, border_width=1)
category.insert(0, str(cur.execute('''SELECT Category_name FROM Postdata WHERE ID=1''').fetchone()[0]))
category.grid(row=1, column=3, pady=10, padx=10)

status = CTkLabel(webinfo_frame, text="Post Status")
status.grid(row=0, column=4, padx=10, pady=3)
status = CTkComboBox(webinfo_frame, width=80, border_width=1, values=['draft', 'publish','blogspot'], state='readonly')
status.set('draft')
status.grid(row=1, column=4, pady=10, padx=10)

blogspot_api_label = CTkLabel(webinfo_frame, text="blogspot api")
blogspot_api_label.grid(row=0, column=5, padx=10, pady=3)
blogspot_api = CTkEntry(webinfo_frame, width=110, border_width=1)
blogspot_api.insert(0, str(cur.execute('''SELECT blogspot_api FROM Postdata WHERE ID=1''').fetchone()[0]))
blogspot_api.grid(row=1, column=5, pady=11, padx=10)

blogspot_id_label = CTkLabel(webinfo_frame, text="blogspot id")
blogspot_id_label.grid(row=0, column=6, padx=10, pady=3)
blogspot_id = CTkEntry(webinfo_frame, width=110, border_width=1)
blogspot_id.insert(0, str(cur.execute('''SELECT blogspot_id FROM Postdata WHERE ID=1''').fetchone()[0]))
blogspot_id.grid(row=1, column=6, pady=10, padx=10)

# API info widgets
apiinfo_frame = CTkFrame(content_frame)
apiinfo_frame.grid(pady=10, padx=20)

# label section
openai_api_label = CTkLabel(apiinfo_frame, text="OpenAI API")
openai_api_label.grid(row=2, column=0, padx=5, pady=3)
openai_api = CTkEntry(apiinfo_frame, width=150, border_width=1)
openai_api.insert(0, str(cur.execute('''SELECT Openai_api FROM Postdata WHERE ID=1''').fetchone()[0]))
openai_api.grid(row=3, column=0, padx=5, pady=10)

api_model_label = CTkLabel(apiinfo_frame, text="API Model")
api_model_label.grid(row=2, column=1, padx=5, pady=3)
api_model = CTkEntry(apiinfo_frame, width=120, border_width=1)
api_model.insert(0, str(cur.execute('''SELECT Openai_model FROM Postdata WHERE ID=1''').fetchone()[0]))
api_model.grid(row=3, column=1, padx=5, pady=10)

model_type_label = CTkLabel(apiinfo_frame, text="Text Generate Mode")
model_type_label.grid(row=2, column=2, padx=5, pady=3)
model_type = CTkComboBox(apiinfo_frame, width=120, values=('Automation', 'API'), border_width=1, state='readonly')
model_type.set('Automation')
model_type.grid(row=3, column=2, padx=5, pady=10)

# browser_open_label = CTkLabel(apiinfo_frame, text="Browser Open")
# browser_open_label.grid(row=2, column=3, padx=5, pady=3)
# browser_open = CTkComboBox(apiinfo_frame, width=50, border_width=1, values=['Yes', 'No'], state='readonly')
# browser_open.set('No')
# browser_open.grid(row=3, column=3, pady=10, padx=5)

feature_img_switch_label = CTkLabel(apiinfo_frame, text="Feature Img")
feature_img_switch_label.grid(row=2, column=3, padx=5, pady=3)
feature_img_switch = CTkComboBox(apiinfo_frame, width=80, border_width=1, values=['On', 'Off'], state='readonly')
feature_img_switch.set('On')
feature_img_switch.grid(row=3, column=3, pady=10, padx=5)

faq_switch_label = CTkLabel(apiinfo_frame, text="FAQ")
faq_switch_label.grid(row=2, column=4, padx=5, pady=3)
faq_switch = CTkComboBox(apiinfo_frame, width=80, border_width=1, values=['On', 'Off'], state='readonly')
faq_switch.set('On')
faq_switch.grid(row=3, column=4, pady=10, padx=5)

# body_img_switch_label = CTkLabel(apiinfo_frame, text="Body IMG")
# body_img_switch_label.grid(row=2, column=5, padx=5, pady=3)
# body_img_switch = CTkComboBox(apiinfo_frame, width=80, border_width=1, values=['On', 'Off'], state='readonly')
# body_img_switch.set('On')
# body_img_switch.grid(row=3, column=5, pady=10, padx=5)


pixabay_api_key_label = CTkLabel(apiinfo_frame, text="Pixels")
pixabay_api_key_label.grid(row=2, column=6, padx=5, pady=3)
pixabay_api_key = CTkEntry(apiinfo_frame, width=120, border_width=1)
pixabay_api_key.insert(0, str(cur.execute('''SELECT Pixabay_api FROM Postdata WHERE ID=1''').fetchone()[0]))
pixabay_api_key.grid(row=3, column=6, pady=10, padx=5)


# chatgpt_email = CTkEntry(apiinfo_frame, width=160, border_width=1)
# chatgpt_email.insert(0, str(cur.execute('''SELECT chatgpt_email FROM Postdata WHERE ID=1''').fetchone()[0]))
# chatgpt_email.grid(row=4, column=0, pady=10, padx=5)
#
# chatgpt_pass = CTkEntry(apiinfo_frame, width=160, border_width=1)
# chatgpt_pass.insert(0, str(cur.execute('''SELECT chatgpt_pass FROM Postdata WHERE ID=1''').fetchone()[0]))
# chatgpt_pass.grid(row=4, column=1, pady=10, padx=5)


gologin_api = CTkEntry(apiinfo_frame, width=250, border_width=1)
gologin_api.insert(0, str(cur.execute('''SELECT gologin_api FROM Postdata WHERE ID=1''').fetchone()[0]))
gologin_api.grid(row=4, column=1, pady=10, padx=5)

gologin_id = CTkEntry(apiinfo_frame, width=200, border_width=1)
gologin_id.insert(0, str(cur.execute('''SELECT gologin_id FROM Postdata WHERE ID=1''').fetchone()[0]))
gologin_id.grid(row=4, column=2, pady=10, padx=5)

# text_generate_mode = CTkComboBox(apiinfo_frame, width=120, border_width=1, values=['TextMode', 'HTMLMode'], state='readonly')
# text_generate_mode.set('TextMode')
# text_generate_mode.grid(row=4, column=4, pady=10, padx=10)



# OpenAI Command Section
openai_section = CTkFrame(content_frame)
openai_section.grid(pady=10, padx=10)

title_generator_label = CTkLabel(openai_section, width=155, text="Title Generator : ")
title_generator_label.grid(row=5, column=0, pady=5, padx=10, sticky='w')
title_generator = CTkTextbox(openai_section, height=70, width=800, border_width=1)
title_generator.insert(1.0, str(cur.execute('''SELECT title_generator FROM Postdata WHERE ID=1''').fetchone()[0]))
title_generator.grid(row=5, column=1, pady=10, padx=10)

intro_generator_label = CTkLabel(openai_section, width=155, text="Intro Generator : ")
intro_generator_label.grid(row=6, column=0, pady=5, padx=10, sticky='w')
intro_generator = CTkTextbox(openai_section, height=80, width=800, border_width=1)
intro_generator.insert(1.0, str(cur.execute('''SELECT Intro_generator FROM Postdata WHERE ID=1''').fetchone()[0]))
intro_generator.grid(row=6, column=1, pady=5, padx=10)

content_generator_label = CTkLabel(openai_section, width=155, text="Content Generator : ")
content_generator_label.grid(row=7, column=0, pady=10, padx=10, sticky='w')
content_generator = CTkTextbox(openai_section, height=280, width=800, border_width=1)
content_generator.insert(1.0, str(cur.execute('''SELECT Content_generator FROM Postdata WHERE ID=1''').fetchone()[0]))
content_generator.grid(row=7, column=1, pady=5, padx=10)

faq_generator_label = CTkLabel(openai_section, width=155, text="FAQ Generator : ")
faq_generator_label.grid(row=8, column=0, pady=5, padx=10, sticky='w')
faq_generator = CTkTextbox(openai_section, height=150, width=800, border_width=1)
faq_generator.insert(1.0, str(cur.execute('''SELECT faq_generator FROM Postdata WHERE ID=1''').fetchone()[0]))
faq_generator.grid(row=8, column=1, pady=5, padx=10)

conclusion_generator_label = CTkLabel(openai_section, width=155, text="Conclusion Generator : ")
conclusion_generator_label.grid(row=9, column=0, pady=5, padx=10, sticky='w')
conclusion_generator = CTkTextbox(openai_section, height=90, width=800, border_width=1)
conclusion_generator.insert(1.0,
                            str(cur.execute('''SELECT conclusion_generator FROM Postdata WHERE ID=1''').fetchone()[0]))
conclusion_generator.grid(row=9, column=1, pady=5, padx=10)



# Terminal
terminal = CTkFrame(content_frame)
terminal.grid(row=11, column=0)

keyword_label = CTkLabel(terminal, text="Input Keywords")
keyword_label.grid(row=12, column=0, pady=5)
keyword_input = CTkTextbox(terminal, width=486, height=300)
keyword_input.insert('1.0', "Input keyword list here...")
keyword_input.grid(row=13, column=0, pady=0, ipadx=5)

output_label = CTkLabel(terminal, text="Output")
output_label.grid(row=12, column=1, pady=5)
output = CTkTextbox(terminal, fg_color=('black', 'white'), text_color=('white', 'black'), width=486, height=300)
output.grid(row=13, column=1, pady=0, ipadx=5)

# Command
command_label = CTkFrame(content_frame)
command_label.grid(row=14, column=0, padx=10, pady=(30, 30))

start = CTkButton(command_label, text=" ▶ Run", fg_color=('#2AA26F'),
                  command=lambda: operation_start())  # Labda have to use when function is below
start.grid(row=15, column=0, padx=20, pady=10, ipadx=20)

Update = CTkButton(command_label, text=' ✔ Save Update', fg_color=("#2AA26F"), command=lambda: db_save())
Update.grid(row=15, column=1, padx=20, pady=10, ipadx=20)

Reset = CTkButton(command_label, text=' ↻ Reset Commands', fg_color=("#EB4C42"), command=lambda: reset_data())
Reset.grid(row=15, column=2, padx=20, pady=10, ipadx=20)

# Log
log_label = CTkLabel(content_frame, text="Logs", font=('', 20), fg_color=("red"))
log_label.grid(row=16, column=0, pady=0, ipadx=20)

log = CTkTextbox(content_frame, fg_color=('black', 'white'), text_color=('white', 'black'), width=990, height=200)
log.grid(row=17, column=0, padx=5, pady=(5, 10))

copyright = CTkLabel(content_frame, text="Need any help ?")
copyright.grid(row=18, column=0, padx=5, pady=(5, 0))

copy_button = CTkButton(content_frame, text="Contact With Developer", fg_color=('#2374E1'),
                        command=lambda: webbrowser.open_new('https://www.facebook.com/samratprodev/'))
copy_button.grid(row=19, column=0, padx=5, pady=(5, 300))


def db_save():
    website_name = str(website_entry.get())
    username = str(username_entry.get())
    app_pass = str(app_pass_entry.get())
    category_name = str(category.get())
    openai_key = str(openai_api.get())
    pixabay_api = pixabay_api_key.get()
    blogspot_api_key = blogspot_api.get()
    blogspot_id_key = blogspot_id.get()
    chatgpt_email_value = 'chatgpt_email.get()'
    chatgpt_pass_value = 'chatgpt_pass.get()'
    gologin_api_value = gologin_api.get()
    gologin_id_value = gologin_id.get()
    model = str(api_model.get())
    content_command = str(content_generator.get('1.0', 'end-1c'))
    # content_command = str(content_generator.get('1.0', END))
    intro_command = str(intro_generator.get('1.0', 'end-1c'))
    faq_command = str(faq_generator.get('1.0', 'end-1c'))
    conclusion_command = str(conclusion_generator.get('1.0', 'end-1c'))

    title_command = str(title_generator.get('1.0', 'end-1c'))
    cur.execute('''
        UPDATE Postdata
        SET
            Website_name = ?,
            User_name = ?,
            App_pass = ?,
            Category_name = ?,
            Openai_api = ?,
            Pixabay_api = ?,
            blogspot_api = ?,
            blogspot_id = ?,
            chatgpt_email = ?,
            chatgpt_pass = ?,
            gologin_api = ?,
            gologin_id = ?,
            Openai_model = ?,
            Content_generator = ?,
            Intro_generator = ?,
            faq_generator = ?,
            conclusion_generator = ?,
            title_generator = ?
        WHERE ID = 1
    ''', (
    website_name, username, app_pass, category_name, openai_key, pixabay_api, blogspot_api_key, blogspot_id_key, chatgpt_email_value, chatgpt_pass_value, gologin_api_value, gologin_id_value, model, content_command, intro_command, faq_command,
    conclusion_command, title_command))


def reset_data():
    # Clear and Update default data
    website_entry.delete(0,END)
    website_entry.insert(0,'https://websitename.com/')
            
    username_entry.delete(0,END)
    username_entry.insert(0,'wp username')
            
    app_pass_entry.delete(0,END)
    app_pass_entry.insert(0,'app pass token')
            
    category.delete(0,END)
    category.insert(0,'category name')
            
    # Reset additional fields
    openai_api.delete(0, tk.END)
    openai_api.insert(0, 'Openai Key')

    pixabay_api_key.delete(0, tk.END)
    pixabay_api_key.insert(0, 'pexels_api')

    blogspot_api.delete(0, tk.END)
    blogspot_api.insert(0, 'blogspot_api')

    blogspot_id.delete(0, tk.END)
    blogspot_id.insert(0, 'blogspot_id')

    chatgpt_email.delete(0, tk.END)
    chatgpt_email.insert(0, 'chatgpt_email')

    chatgpt_pass.delete(0, tk.END)
    chatgpt_pass.insert(0, 'chatgpt_pass')

    gologin_api.delete(0, tk.END)
    gologin_api.insert(0, 'gologin_api')

    gologin_id.delete(0, tk.END)
    gologin_id.insert(0, 'gologin_id')

    # Handle the text widgets (if any)
    content_generator.delete("1.0", tk.END)
    content_generator.insert(tk.END, 'I Want You To Act As A Content Writer Very Proficient SEO Writer. Do it step by step. '
                                     'Bold the Heading of the Article using Markdown language. At least 10 headings and '
                                     'write a 1000+ words 100% Unique, SEO-optimized, Human-Written article. '
                                     'Write The article In Your Own Words Rather Than Copying And Pasting From Other Sources. '
                                     'Consider perplexity and burstiness when creating content, ensuring high levels of both '
                                     'without losing specificity or context. Use fully detailed paragraphs that engage the reader. '
                                     'Write In A Conversational Style As Written By A Human (Use An Informal Tone, Utilize Personal Pronouns, '
                                     'Keep It Simple, Engage The Reader, Use The Active Voice, Keep It Brief, Use Rhetorical Questions, '
                                     'and Incorporate Analogies And Metaphors). And please don\'t give me introduction, conclusion and faq, '
                                     'I want just content body. Now Write An Article On This Topic : ((keyword))')

    intro_generator.delete("1.0", tk.END)
    intro_generator.insert(tk.END, 'Write a introduction on this keyword intro start with technical terms, not like are you and keyword '
                                   'must be include in output do not give me direct solution in intro section, intro last sentence must '
                                   'be interesting to read the full article, keyword: ((keyword))\nAnd length approx 100 words\n')

    faq_generator.delete("1.0", tk.END)
    faq_generator.insert(tk.END, 'Write 5 FAQ with short answer within 1 sentence on this keyword : ((keyword)) '
                                 'Bold the Heading of using Markdown language. And please ignore here is your output or this type sentence. '
                                 'I want to just my targeted output')

    conclusion_generator.delete("1.0", tk.END)
    conclusion_generator.insert(tk.END, 'keyword: ((keyword))\nWrite an web article bottom summary\nAnd length approx 60 words\n')
    # Update database also
    cur.execute('''
                    UPDATE Postdata
                    SET
                        Website_name = 'https://websitename.com/',
                        User_name = 'wp username',
                        App_pass = 'app pass token',
                        Category_name = 'category name', 
                        Openai_api = 'Openai Key',
                        Pixabay_api = 'pexels_api',
                        blogspot_api = 'blogspot_api',
                        blogspot_id =  'blogspot_id',
                        chatgpt_email =  'chatgpt_email',
                        chatgpt_pass =  'chatgpt_pass',
                        gologin_api =  'gologin_api',
                        gologin_id =  'gologin_id',
                        chatgpt_pass =  'chatgpt_pass',
                        Openai_model = 'gpt-3.5-turbo',
                        Content_generator = 'I Want You To Act As A Content Writer Very Proficient SEO Writer. Do it step by step. 
Bold the Heading of the Article using Markdown language. At least 10 headings and write a 1000+ words 100% Unique, SEO-optimized, Human-Written article.
Write The article In Your Own Words Rather Than Copying And Pasting From Other Sources. Consider perplexity and burstiness when creating content, ensuring high levels of both without losing specificity or context. Use fully detailed paragraphs that engage the reader. Write In A Conversational Style As Written By A Human (Use An Informal Tone, Utilize Personal Pronouns, Keep It Simple, Engage The Reader, Use The Active Voice, Keep It Brief, Use Rhetorical Questions, and Incorporate Analogies And Metaphors).  
And please don't give me introduction, conclusion and faq, I want just content body.
Now Write An Article On This Topic : ((keyword))',
                        Intro_generator = 'Write a introduction on this keyword intro start with technical terms, not like are you and keyword must be include in output do not give me direct solution in intro section, intro last sentence must be interesting to read the full article, keyword: ((keyword))\nAnd length approx 100 words\n',
                        faq_generator =  'Write 5 FAQ with short answer within 1 sentence on this keyword : ((keyword))
Bold the Heading of using Markdown language.  And please ignore here is your output or this type sentence. I want to just my targeted output
',
                        conclusion_generator = 'keyword: ((keyword))\nWrite an web article bottom summary\nAnd length approx 60 words\n',                    
                        title_generator = 'write an SEO title on this keyword within 55 characters and the keyword must be directly included in the title \nkeyword : ((keyword))\n'
                    WHERE ID = 1

                    ''')
    # window.destroy()


def operation_start():
    thread = threading.Thread(target=operation_start_thread)
    thread.start()


def operation_start_thread():
    website_url = website_entry.get()
    Username = username_entry.get()
    App_pass = app_pass_entry.get()
    category_name = category.get()
    status_value = status.get()
    openai_key = openai_api.get()
    engine = api_model.get()
    engine_type = model_type.get()
    # operation = browser_open.get()
    feature_img_status = feature_img_switch.get()
    faq_switch_status = faq_switch.get()
    pixabay_api = pixabay_api_key.get()
    blogspot_api_key = blogspot_api.get()
    blogspot_id_key = blogspot_id.get()
    gologin_api_value = gologin_api.get()
    gologin_id_value = gologin_id.get()
    content_command = content_generator.get('1.0', 'end-1c')
    intro_command = intro_generator.get('1.0', 'end-1c')
    faq_command = faq_generator.get('1.0', 'end-1c')
    conclusion_command = conclusion_generator.get('1.0', 'end-1c')
    title_command = title_generator.get('1.0', 'end-1c')


    # Wordpress posting code-----------------
    json_url = website_url + 'wp-json/wp/v2'
    token = base64.standard_b64encode((Username + ':' + App_pass).encode('utf-8'))  # we have to encode the usr and pw
    headers = {'Authorization': 'Basic ' + token.decode('utf-8')}

    i = 1
    keyword_list = keyword_input.get('1.0', 'end-1c')
    all_keywords = keyword_list.splitlines()
    output.delete('0.0', END)
    output.insert('0.0', '>>> Start Working...\n')

    content_generator_loop(
            category_name,
            status_value,
            openai_key,
            engine,
            engine_type,
            feature_img_status,
            faq_switch_status,
            pixabay_api,
            blogspot_api_key,
            blogspot_id_key,
            gologin_api_value,
            gologin_id_value,
            content_command,
            intro_command,
            faq_command,
            conclusion_command,
            title_command,
            json_url,
            headers,
            all_keywords,
            log,
            output
    )



def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


if __name__ == '__main__':
    window.mainloop()

con.commit()
cur.close()
