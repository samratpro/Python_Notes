from customtkinter import *
from playwright.sync_api import sync_playwright
import webbrowser, threading, os, json
import sqlite3
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from tkinter import END
from time import sleep
from openai import OpenAI
from random import choice
import re
import requests


class AmazonPage(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.base_path = os.path.join(os.getcwd(), "amazon_data")
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        self.template_path = os.path.join(self.base_path, "template")
        if not os.path.exists(self.template_path):
            os.makedirs(self.template_path)
        self.chrome_path = os.path.join(os.getcwd(), "chrome/chrome.exe")
        self.db_path = os.path.join(self.base_path, "database.db")
        self.keyword_path = 'no_path'

        ## checking number of logins and path
        self.json_files = [f for f in os.listdir(self.base_path) if f.endswith('.json')]
        self.cookie_path = os.path.join(os.getcwd(), f"{self.base_path}/cookie.json")

        # main labale
        self.label = CTkLabel(self, text="Amazon Writer Page", height=30, width=200, font=("Arial", 20))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        # main scroll frame
        self.scrollable_frame = CTkScrollableFrame(self, width=500, height=400, border_width=1)
        self.scrollable_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        # Configure row and column weights for resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # API Frame
        self.api_frame = CTkFrame(self.scrollable_frame)
        self.api_frame.grid(pady=10, padx=20)

        self.open_button = CTkButton(self.api_frame, text="Open Browser", width=200, fg_color=('#006262'),
                                     corner_radius=20, command=lambda: self.browser_open())
        self.open_button.grid(row=1, column=0, padx=10, pady=10)

        self.close_button = CTkButton(self.api_frame, text="Save Cookie", width=200, fg_color=('#006262'),
                                      corner_radius=20, command=lambda: self.browser_close())
        self.close_button.grid(row=1, column=1, padx=10, pady=10)


        self.cookie_status = CTkLabel(self.api_frame, width=300, text=f"Cookie Status: ",corner_radius=20,fg_color=('#9457EB'), text_color=('#E1E8FF'))
        if os.path.exists(self.cookie_path):
            self.cookie_status.configure(text="Cookie Status : True")
        else:
            self.cookie_status.configure(text="Cookie Status : False")
        self.cookie_status.grid(row=1, column=2, padx=10, pady=10)

        # Keyword frame
        def select_file():
            file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Text File", "*.txt")])
            self.keyword_path = os.path.join(os.getcwd(), file_path)
            if self.keyword_path:
                self.file_label.configure(text=self.keyword_path)

        self.keyword_frame = CTkFrame(self.scrollable_frame, border_width=1)
        self.keyword_frame.grid(pady=10, padx=10)
        self.keyword_label = CTkLabel(self.keyword_frame,
                                      text='Select Keyword File : ',
                                      anchor='w',
                                      width=60
                                      )
        self.keyword_label.grid(row=0, column=0, pady=10, padx=10)

        self.upload_button = CTkButton(self.keyword_frame,
                                       text="Select File",
                                       command=lambda: select_file(),
                                       anchor='center',
                                       width=30
                                       )
        self.upload_button.grid(row=0, column=1, pady=10, padx=10)

        self.file_label = CTkLabel(self.keyword_frame,
                                   text="No file selected",
                                   anchor='e',
                                   width=480
                                   )
        self.file_label.grid(row=0, column=2, pady=10, padx=10)

        # Command
        self.command_label = CTkFrame(self.scrollable_frame, fg_color=('#DBDBDB'))
        self.command_label.grid(pady=10, padx=20)
        self.start = CTkButton(self.command_label, text="▶️ Run", width=167, fg_color=('#006262'), corner_radius=20,
                               command=lambda: self.operation_start())
        self.start.grid(row=0, column=0, padx=5, pady=10, ipadx=5)
        self.stop = CTkButton(self.command_label, text="⏹️ Stop", width=167, fg_color=('#9457EB'), corner_radius=20,
                              command=lambda: self.operation_close())
        self.stop.grid(row=0, column=1, padx=5, pady=10, ipadx=5)

        # Log
        self.log = CTkTextbox(self.scrollable_frame, width=750, height=300, fg_color=('black', 'white'),
                              text_color=('white', 'black'))
        self.log.grid(row=11, column=0, padx=5, pady=(5, 10))

        self.copyright = CTkLabel(self.scrollable_frame, text="Need any help ?", width=700)
        self.copyright.grid(row=12, column=0, padx=5, pady=(5, 0))
        self.copy_button = CTkButton(self.scrollable_frame, text="Contact With Developer", fg_color=('#2374E1'),
                                     command=lambda: webbrowser.open_new('https://www.facebook.com/samratprodev/'))
        self.copy_button.grid(row=13, column=0, padx=5, pady=(5, 300))

        # login funcationality
        self.browser_close_event = threading.Event()
        self.args = [
            '--disable-blink-features=AutomationControlled',
            '--start-maximized',
            '--disable-infobars',
            '--no-sandbox',
            '--enable-gpu',
            '--use-gl=desktop',
            '--enable-webgl',
            '--enable-accelerated-2d-canvas',
            '--autoplay-policy=no-user-gesture-required',
            '--disable-dev-shm-usage',
            '--disable-extensions',
            '--remote-debugging-port=0',
            '--disable-web-security',
            '--enable-features=WebRTCPeerConnectionWithBlockIceAddresses',
            '--force-webrtc-ip-handling-policy=disable_non_proxied_udp',
            '--disable-third-party-cookies',  # Prevent third-party cookies from being blocked
        ]


    def is_storage_state_valid(self, file_path):
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    return bool(data)  # true false depend data exist
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                return False
        else:
            open(file_path, 'w').close()  # Create an empty file
            return False

    def cookie_save(self, log, close_event):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                executable_path=self.chrome_path,
                headless=False,
                args=self.args
            )
            # Create a new context and page
            context = browser.new_context(no_viewport=True)
            page = context.new_page()
            try:
                page.goto("https://amazon.com", timeout=120000)
            except Exception as e:
                log.insert(END, f"Error navigating to amazon: {e}\n")
                log.see(END)
                browser.close()
                return

            def check_close_event():
                if page.is_closed():
                    log.insert(END, "Browser closed or crashed. Exiting...\n")
                    log.see(END)
                    print("Browser closed or crashed. Exiting...")
                    return

                # Check if the close_event is set
                if not close_event.is_set():
                    sleep(5)  # Wait for 5 seconds
                    check_close_event()  # Recursive call
                else:
                    try:
                        context.storage_state(path=self.cookie_path)
                        self.cookie_status.configure(text=f"Cookie Status : True")
                        print("Login Data saved...")
                        log.insert(END, "Login Data saved...\n")
                        log.see(END)
                    except Exception as e:
                        log.insert(END, f"Error saving login data: {e}\n")
                        log.see(END)
                    finally:
                        if browser.is_connected():
                            browser.close()
                        log.insert(END, "Browser closed.\n")
                        log.see(END)
            check_close_event()

    def browser_open(self):
        thread = threading.Thread(target=self.browser_open_thread)
        thread.start()

    def browser_open_thread(self):
        # Clear the event if the browser is being opened
        self.browser_close_event.clear()
        self.cookie_save(self.log, close_event=self.browser_close_event)

    def browser_close(self):
        # Set the event to signal the browser should close
        self.browser_close_event.set()

    operation_close_event = threading.Event()

    def operation_start(self):
        if self.keyword_path != 'no_path':
            self.start.configure(text="⌛️ Running...")
            thread = threading.Thread(target=self.operation_start_thread)
            thread.start()
        else:
            print(f'Please select Keyword path..\n\n')
            self.log.insert(END, f'Please select Keyword path..\n\n')

    def operation_close(self):
        self.start.configure(text="▶️ Run")
        self.operation_close_event.set()

    def stop_check(self, event, log) -> bool:
        if event:
            print("⏹️ Stopped...")
            log.insert(END, f"⏹️ Stopped...\n\n")
            log.see(END)
            return True
        else:
            return False

    def operation_start_thread(self):
        keyword_path = self.keyword_path
        with open(keyword_path, 'r') as file:
            keyword_data = file.readlines()
            file.close()
        keywords_list = [x.strip() for x in keyword_data if len(x) > 0]

        self.operation_close_event.clear()

        print('keywords_list : ', keywords_list)

        self.posting_loop(keywords_list, self.log,
                          close_event=self.operation_close_event)

    # Seperate function

    # Main posting loop
    def posting_loop(self, keywords_list, log, close_event):
        print("Posting has started")


    def generate_content_body(self, prompt, deepseek_api, gemni_api, default_api, log, message):
        content_response = self.text_render(prompt, deepseek_api, gemni_api, default_api, log, message)
        if content_response != 'API-ERROR':
            # Split the content by <h2>, <h3>, and <p> tags
            content_split = re.split(r'(<h2>.*?</h2>|<h3>.*?</h3>|<p>.*?</p>)', content_response)
            # Remove HTML tags from each item and add to the list
            cleaned_content = [re.sub(r'<[^>]+>', '', x).strip() + '\n' for x in content_split if x.strip()]
            content_body = '\n'.join(cleaned_content)
            return content_body
        else:
            return "Content Body Text Generate error"

    def text_render(self, prompt, deepseek_key, gemni_key, default_key, log, message):
        log.insert("end", f"{message}\n")
        print(f"{message}\n")
        print("api key:", gemni_key)
        content = ''
        i = 1
        while i < 4:
            if default_key != "gemni":
                client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")
                try:
                    response = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=[
                            {"role": "system", "content": "You are content writing assistant"},
                            {"role": "user", "content": prompt},
                        ],
                        stream=False
                    )
                    content = response.choices[0].message.content
                    break
                except Exception as e:
                    log.insert("end", f"API-ERROR from Deepseek, trying ({i}) time\n")
                    print(f"API-ERROR from Deepseek, trying ({i}) time\n")
                    print("Error details:", str(e))
                    content = 'API-ERROR'
            else:
                try:
                    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemni_key}"
                    headers = {"Content-Type": "application/json"}
                    data = {"contents": [{"parts": [{"text": prompt}]}]}

                    response = requests.post(API_URL, json=data, headers=headers)
                    result = response.json()  # Convert response to JSON

                    # ✅ Handle errors in response
                    if response.status_code != 200:
                        log.insert("end", f"API-ERROR from Gemini ({i}) time\n")
                        print(f"API-ERROR from Gemini, trying ({i}) time\n")
                        print("Error Response:", result)
                        content = 'API-ERROR'
                    elif "candidates" not in result:
                        log.insert("end", f"API-ERROR: No candidates found, trying ({i}) time\n")
                        print(f"API-ERROR: No candidates found, trying ({i}) time\n")
                        print("Error Response:", result)
                        content = 'API-ERROR'
                    else:
                        content = result["candidates"][0]["content"]["parts"][0]["text"].replace("*", '')
                        break

                except Exception as e:
                    log.insert("end", f"API-ERROR from Gemini, trying ({i}) time\n")
                    print(f"API-ERROR from Gemini, trying ({i}) time\n")
                    print("Exception details:", str(e))
                    content = 'API-ERROR'
            i += 1
        return content

    def get_image_path(self, keyword, log):
        log.insert(END, f"Generating Image\n")
        template_dir = self.template_path  # Use the correct template directory path
        img_path = os.path.join(self.base_path, 'img')
        # Check if template directory exists
        if not os.path.exists(template_dir):
            log.insert(END, f"Template directory not found: {template_dir}\n")
            print(f"Template directory not found: {template_dir}\n")
            return 'img_error'
        # Create img directory if it doesn't exist
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        try:
            # Get all images from the template directory
            template_images = [f for f in os.listdir(template_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
        except FileNotFoundError:
            log.insert(END, f"Error: Template directory '{template_dir}' not found.\n")
            print(f"Error: Template directory '{template_dir}' not found.\n")
            return 'img_error'
        if not template_images:
            log.insert(END, f'No images found in the template directory.\n')
            return 'img_error'
        # Select a random image from the template directory
        random_image = choice(template_images)
        random_image_path = os.path.join(template_dir, random_image)
        try:
            im = Image.open(random_image_path)
            im = im.resize((800, 450), Image.Resampling.LANCZOS)
            darken_factor = 0.5
            im = im.point(lambda p: p * darken_factor)
            blur_radius = 2
            im = im.filter(ImageFilter.GaussianBlur(blur_radius))
            draw = ImageDraw.Draw(im)
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except IOError:
                font = ImageFont.load_default()
            words = keyword.title().split()
            max_words_per_line = 5
            wrapped_text = [" ".join(words[i:i + max_words_per_line]) for i in range(0, len(words), max_words_per_line)]
            line_height = font.getbbox('A')[3] - font.getbbox('A')[1]  # Height of one line
            total_text_height = len(wrapped_text) * line_height + (len(wrapped_text) - 1) * 20
            text_y = 450 - total_text_height - 50  # 50 pixels margin from the bottom
            text_color = choice(['yellow', '#F4CA16', 'white','#CCE4F7','#F0CF65'])
            for line in wrapped_text:
                text_bbox = draw.textbbox((0, 0), line, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_x = (800 - text_width) // 2
                border_thickness = 1
                for dx in range(-border_thickness, border_thickness + 1):
                    for dy in range(-border_thickness, border_thickness + 1):
                        if dx != 0 or dy != 0:  # Avoid overwriting the main text
                            draw.text((text_x + dx, text_y + dy), line, font=font, fill='#4A4A4A')
                draw.text((text_x, text_y), line, font=font, fill=text_color)
                text_y += line_height + 30
            # Save the modified image
            output_image_path = os.path.join(img_path, f'{keyword}.jpg')
            im.save(output_image_path)
            log.insert(END, f'Image Generate Done\n')
            return output_image_path

        except Exception as ops:
            log.insert(END, f'Error: {str(ops)}\n')
            print(f'Error: {str(ops)}\n')
            return 'img_error'

    def medium_posting_function(self, profile_path, title, img_path, content_body, log):
        log.insert(END, f"Start Posting\n")
        print(f"Start Posting\n")
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                executable_path=self.chrome_path,
                headless=False,
                args=self.args,
            )
            if self.is_storage_state_valid(profile_path):
                try:
                    context = browser.new_context(storage_state=profile_path, no_viewport=True)
                    page = context.new_page()
                    log.insert(END, f"Go to Post Page\n")
                    print(f"Go to Post Page\n")
                    for _ in range(4):
                        try:
                            page.goto('https://medium.com/new-story')
                            break
                        except:
                            print(f"Trying .. {str(_ + 2)} time..")
                            log.insert(END, f"Fail to load trying .. {str(_ + 2)} time..\n")
                            page.goto('https://medium.com/new-story')
                    page.wait_for_load_state("load")
                    # Image
                    if img_path != 'img_error':
                        page.click("//button[@title='Add an image, video, embed, or new part']")
                        with page.expect_file_chooser() as fc_info:
                            page.click("//button[@title='Add an image']")
                            sleep(2)
                        file_chooser = fc_info.value
                        file_chooser.set_files(img_path)
                        sleep(1)
                    else:
                        # log.insert(END, f"Error path error...\n")
                        print(f"Error path error...\n")
                        log.insert(END, f"Image generate error\n")
                        print(f"Image generate error\n")
                    sleep(1)
                    # Ttitle
                    page.locator("//h3[@data-testid='editorTitleParagraph']").fill(title)
                    sleep(1)
                    page.locator("//p[@data-testid='editorParagraphText']").click()
                    page.evaluate(
                        """
                        ({ elementSelector, value }) => {
                            const element = document.querySelector(elementSelector);
                            if (element) {
                                element.focus();
                                element.innerText = value;
                                const inputEvent = new Event('input', { bubbles: true });
                                element.dispatchEvent(inputEvent);
                                const changeEvent = new Event('change', { bubbles: true });
                                element.dispatchEvent(changeEvent);
                                element.blur();
                            }
                        }
                        """,
                        {"elementSelector": "p[data-testid='editorParagraphText']", "value": content_body}
                    )
                    sleep(1)
                    page.locator("//button[@data-action-source='post_edit_prepublish']").click()
                    sleep(1)
                    page.locator("text='Publish now'").click()
                    sleep(2)
                    browser.close()
                    log.insert(END, f"Posting Done\n")
                    print(f"Posting Done\n")
                except Exception as ops:
                    log.insert(END, f"Error Happen : {str(ops)}...\n")
                    print(f"Error Happen : {str(ops)}...\n")
            else:
                log.insert(END, "Login Not working...\n")
                print("Login Not working...\n")