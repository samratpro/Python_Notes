import openai
from random import choice
from PIL import Image
from PIL import ImageFile
import requests
import os
import json
from time import sleep
ImageFile.LOAD_TRUNCATED_IMAGES = True
from tkinter import END
import shutil
from pexels_api import API
from gologin import GoLogin
from playwright.sync_api import sync_playwright


def content_generator_loop(
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
                      ):
    with sync_playwright() as p:
        gl = GoLogin({
            "token": gologin_api_value,
            "profile_id": gologin_id_value,
        })

        debugger_address = gl.start()
        browser = p.chromium.connect_over_cdp("http://" + debugger_address)
        default_context = browser.contexts[0]
        page = default_context.pages[0]


        def feature_image(command):
            log.insert(END, f'Working Feature Image Section\n\n')
            if feature_img_status == "On":
                if not os.path.exists('img'):
                    os.makedirs('img')
                try:
                    api = API(pixabay_api)
                    api.search(command, page=1, results_per_page=1)
                    photos = api.get_entries()
                    photo_list = list()
                    for photo in photos:
                        photo = photo.original
                        photo_list.append(photo)
                    headers_fox = {
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
                    response = requests.get(photo_list[0], stream=True, headers=headers_fox)
                    print(response)
                    local_file = open('img/' + command + '.jpg', 'wb')
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, local_file)
                    im = Image.open('img/' + command + '.jpg')
                    resized_im = im.resize((round(im.size[0] * 0.5), round(im.size[1] * 0.5)))
                    resized_im.save('img/' + command + '.jpg')
                    media = {'file': open('img/' + command + '.jpg', 'rb')}
                    image = requests.post(json_url + '/media', headers=headers, files=media)
                    print(image)
                    post_id = str(json.loads(image.content.decode('utf-8'))['id'])
                    print(post_id)
                    return post_id
                except Exception as ops:
                    log.insert(END, f'error : {str(ops)}\n\n')
                    return 0
            else:
                return 0

        def create_category(cat_name):
            log.insert(END, 'Working in Category Section\n\n')
            id = 0
            if len(cat_name) > 0:
                data = {"name":cat_name}
                try:
                    cat = requests.post(json_url + '/categories', headers=headers, json=data)
                    id = str(json.loads(cat.content.decode('utf-8'))['id'])
                except:
                    try:
                        cat = requests.get(json_url + '/categories', headers=headers)
                        cat_id = json.loads(cat.content.decode('utf-8'))
                        for cat in cat_id:
                            if cat_name.lower() == cat['name'].lower():
                                id = str(cat['id'])
                    except:
                        pass
            return id




        def text_format(text):
            if len(text) > 0:
                rc1 = choice([3, 4])
                rc2 = choice([10, 11])
                rc3 = choice([16, 17])
                p_format = text.replace('?', '?---').replace('.', '.---').replace('!', '!---').strip().split(sep='---')
                p = '<p>' + ''.join(p_format[:rc1]) + '</p>' + '<p>' + ''.join(p_format[rc1:7]) + '</p>' + '<p>' + ''.join(p_format[7:rc2]) + '</p>' + '<p>' + ''.join(p_format[rc2:13]) + '</p>' + '<p>' + ''.join(p_format[13:rc3]) + '</p>' + '<p>' + ''.join(p_format[rc3:20]) + '</p>' + '<p>' + ''.join(p_format[20:]) + '</p>'
                text = p.replace('  ', ' ').replace('<p></p>', '').replace('<p><p>', '<p>').replace('</p></p>', '</p>').replace('<p> ', '<p>').replace('\n', '').replace('1.', '').replace('2.', '').replace('3.', '').replace('4.', '').replace('5.', '').replace('6.', '').replace('7.', '').replace('8.', '').replace('9.', '').replace('10.', '').replace('<p>  ','<p>').replace('<p> ','<p>').replace('.','. ').replace('.  ','. ').replace('!!','')
                return text
            else:
                return ''


        def title_render(keyword):
            log.insert(END, f'Working For Title \n\n')
            if engine_type.strip() == 'Automation':
                log.insert(END, f' Waiting Time : 5 second...\n\n')
                page.goto('https://chatgpt.com/', timeout=600000)
                page.wait_for_load_state("load")
                page.locator("//textarea[@id='prompt-textarea']").first.fill(title_command.replace('((keyword))', keyword))
                page.locator("//button[@data-testid='send-button']").click()
                sleep(6)
                replay = page.locator("//div[@data-message-author-role='assistant']").first.inner_text()
                return replay
            else:
                openai.api_key = openai_key
                response = openai.ChatCompletion.create(model=engine,
                                                        messages=[{"role": "system", "content": ''},
                                                        {"role": "user", "content": title_command.replace('((keyword))',keyword)}]
                                                        )
                result = ''
                for choice in response.choices:
                    result += choice.message.content
                return result


        def text_render(prompt, keyword):
            log.insert(END, f'Working For Text Generation, Intro / Conclusion\n\n')
            if engine_type.strip() == 'Automation':
                log.insert(END, f' Waiting Time : 10 second...\n\n')
                page.goto('https://chatgpt.com/', timeout=600000)
                page.wait_for_load_state("load")
                page.locator("//textarea[@id='prompt-textarea']").first.fill(prompt.replace('((keyword))', keyword))
                page.locator("//button[@data-testid='send-button']").click()
                sleep(10)
                replay = page.locator("//div[@data-message-author-role='assistant']").first.inner_text()
                return text_format(str(replay))
            else:
                openai.api_key = openai_key
                response = openai.ChatCompletion.create(model=engine,
                                                        messages=[{"role": "system", "content": ''},
                                                        {"role": "user", "content": prompt.replace('((keyword))',keyword)}]
                                                        )
                result = ''
                for choice in response.choices:
                    result += choice.message.content
                return text_format(result)


        def content_body(keyword):
            log.insert(END, f'Working in Content Body Section\n\n')

            if engine_type.strip() == 'Automation':
                log.insert(END, f' Waiting Time : 30 second...\n\n')
                page.goto('https://chatgpt.com/', timeout=600000)
                page.wait_for_load_state("load")
                page.locator("//textarea[@id='prompt-textarea']").first.fill(content_command.replace('((keyword))', keyword))
                page.locator("//button[@data-testid='send-button']").click()
                sleep(30)
                replay = str(page.locator("//div[@data-message-author-role='assistant']").first.inner_html())
                return replay
            else:
                openai.api_key = openai_key
                response = openai.ChatCompletion.create(model=engine,
                                                        messages=[{"role": "system", "content": ''},
                                                        {"role": "user", "content": content_command.replace('((keyword))',keyword)}]
                                                        )
                result = ''
                for choice in response.choices:
                    result += choice.message.content
                return post_body


        def faq_body(keyword):
            if faq_switch_status == 'On':
                log.insert(END, f'Working in FAQ Section\n\n')
                if engine_type.strip() == 'Automation':
                    log.insert(END, f' Waiting Time : 10 second...\n\n')
                    page.goto('https://chatgpt.com/', timeout=600000)
                    page.wait_for_load_state("load")
                    page.locator("//textarea[@id='prompt-textarea']").first.fill(faq_command.replace('((keyword))', keyword))
                    page.locator("//button[@data-testid='send-button']").click()
                    sleep(10)
                    replay = str(page.locator("//div[@data-message-author-role='assistant']").first.inner_html())
                    return "<h2> FAQ's </h2>" + replay
                else:
                    openai.api_key = openai_key
                    response = openai.ChatCompletion.create(model=engine,
                                                            messages=[{"role": "system", "content": ''},
                                                            {"role": "user", "content": faq_command.replace('((keyword))',keyword)}]
                                                            )
                    result = ''
                    for choice in response.choices:
                        result += choice.message.content
                    return result
            else:
                log.insert(END, f'FAQ Disable\n\n')
                return ''
        i=1
        for keyword in all_keywords:
            if len(keyword) > 0:
                print('Keyword : ', keyword)
                print(engine)
                print(engine_type)

                log.delete('0.0', END)
                log.insert(END, f'Running Keyword : {keyword}\n\n')
                log.insert(END, f'{engine}\n\n')
                log.insert(END, f'{engine_type}\n\n')
                title = title_render(keyword).replace('"', '').replace('<p>', '').replace('</p>', '').title()
                introduction = text_render(intro_command,keyword)
                post_body = introduction + content_body(keyword) + faq_body(keyword) +'<h2>Conclusion</h2>' +text_render(conclusion_command,keyword)
                if not os.path.exists('content_output'):
                    os.makedirs('content_output')
                with open(f'content_output/{keyword}.txt', 'w') as content_file:
                    content_file.write(title+'\n'+post_body)
                    content_file.close()
                if status_value == "blogspot":
                    API_KEY = blogspot_api_key
                    BLOG_ID = blogspot_id_key

                    # Define the URL for the Blogger API
                    BASE_URL = f'https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/'

                    # Define the post content
                    post_data = {
                        'kind': 'blogger#post',
                        'blog': {
                            'id': BLOG_ID
                        },
                        'title': title,
                        'content': post_body,
                        'labels': [category_name]
                    }

                    # Define the headers
                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {API_KEY}'
                    }

                    # Send POST request to create a new post
                    response = requests.post(BASE_URL, headers=headers, json=post_data)

                    # Check if the request was successful
                    if response.status_code == 201:
                        output.insert(END, f'{str(i)}. {keyword} (Done)..\n')
                        print('completed, kw:', keyword)
                        log.insert(END, f'completed, kw: {keyword}')
                    else:
                        output.insert(END, f'{str(i)}. {keyword} (Fail)..\n\n')
                        output.insert(END, str(f'{str(i)} . {keyword}, Blogspot Error, Status Code is : {response.status_code}\n\n'))
                        log.insert(END, str(f'{str(i)} . {keyword}, Blogspot Error, Status Code is : {response.status_code}\n\n'))
                else:
                    category_id = create_category(category_name)
                    slug = keyword.replace(' ', '-')
                    image_id = feature_image(keyword.strip())
                    print('Feature Image id ..........:', image_id)
                    log.insert(END, f'Feature Image id ..........:{image_id}\n')

                    # Post Data
                    if category_id == 0:
                        post = {'title': title, 'slug': slug, 'status': status_value, 'content': post_body,
                                'format': 'standard', 'featured_media': int(image_id)}
                    else:
                        post = {'title': title, 'slug': slug, 'status': status_value, 'content': post_body,
                                'categories': [category_id], 'format': 'standard', 'featured_media': int(image_id)}

                    # Posting Request
                    try:
                        response = requests.post(json_url + '/posts', headers=headers, json=post)
                    except:
                        response = requests.post(json_url + '/posts', headers=headers, json=post, verify=False)
                    if response.status_code == 201:
                        output.insert(END, f'{str(i)}. {keyword} (Done)..\n')
                        print('completed, kw:', keyword)
                        log.insert(END, f'completed, kw: {keyword}')
                    else:
                        output.insert(END, f'{str(i)}. {keyword} (Fail)..\n\n')
                        output.insert(END, str(f'{str(i)} . {keyword}, WP Error, Status Code is : {response.status_code}\n\n'))
                        log.insert(END, str(f'{str(i)} . {keyword}, WP Error, Status Code is : {response.status_code}\n\n'))
                    try:
                        shutil.rmtree('bulkimg')
                    except:
                        pass
            i += 1
    gl.stop()
