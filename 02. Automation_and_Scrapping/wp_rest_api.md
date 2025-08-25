```py
# logging
from datetime import datetime
print(f'{datetime.now()} - Message...')
```
## 01. Simple Posting
```py
import requests
from requests.auth import HTTPBasicAuth

url = "https://your-wordpress-site.com/wp-json/wp/v2/posts"

username = "your-username"
password = "your-application-password"

category_ids = [5, 12]   # e.g., 5 = parent category, 12 = subcategory
tag_ids = [3, 8]         # tag IDs you got from wp-json/wp/v2/tags


post_data = {
    "title": "Text Post",
    "slug": "",
    "content": 'content',
    "excerpt": 'excerpt content',
    "status": "draft",  # 'publish' / 'schedule'
    "categories": category_ids,
    "tags": tag_ids,
    'featured_media': int(image_id)
}

response = requests.post(url, auth=HTTPBasicAuth(username, password), json=post_data)

if response.status_code == 201:
    print("Post created successfully!")
    print("Response:", response.json())  # The created post data
    print('link : ', response.json().get('guid').get('rendered'))
else:
    print(f"Failed to create post. Status code: {response.status_code}")
    print("Response:", response.json())  # Error details
```
## 02. Posting with header passing
```py
json_url = website_url + 'wp-json/wp/v2'
token = base64.standard_b64encode((Username + ':' + App_pass).encode('utf-8'))
headers = {'Authorization': 'Basic ' + token.decode('utf-8')}
post = {'title': 'title',
        'slug': 'slug',
        'status': 'draft/publish',
        'content': 'post_body',
        'format': 'standard',
        'featured_media': int(image_id)
}
r = requests.post(json_url + '/posts', headers=headers, json=post)
if r.status_code == 201:
    print("Post created successfully!")
    print("Response:", response.json())  # The created post data
else:
    print(f"Failed to create post. Status code: {response.status_code}")
    print("Response:", response.json())  # Error details
```
## 03. More stable way with httpx
```py
import httpx
import base64
credentials = f"{Username}:{App_pass}"
encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
headers = {"Authorization": f"Basic {encoded_credentials}",}
post_data = {'title': 'wp_h1',
        'slug': 'keyword',
        'status': 'publish',
        'content': 'wp_post_body',
        'format': 'standard',
        }
response = httpx.post(
    website + 'wp-json/wp/v2/posts',
    headers=headers,
    json=post_data,
    timeout=30
)
response.json()
```
## 03. Create Category
```py
def create_category(cat_name, json_url, username, password):
    id = 0
    if len(cat_name) > 0:
        data = {"name":cat_name}
        try:
            cat = requests.post(json_url + '/categories', auth=HTTPBasicAuth(username, password), json=data)
            id = str(json.loads(cat.content.decode('utf-8'))['id'])
        except KeyError:
            cat = requests.get(json_url + '/categories', headers=headers)
            cat_id = json.loads(cat.content.decode('utf-8'))
            for cat in cat_id:
                if cat_name.lower() == cat['name'].lower():
                    id = str(cat['id'])
    return id


def create_category(cat_name, website_url, username, password):
    if not cat_name:
        print("Category name is empty. Skipping.")
        return None
    id = None
    data = {"name": cat_name}
    try:
        # Attempt to create the category
        response = requests.post(f"{website_url}/wp-json/wp/v2/categories",auth=HTTPBasicAuth(username, password),json=data)
        if response.status_code == 201:  # Category created successfully
            id = str(response.json().get('id'))
            print(f"Created new category '{cat_name}' with ID {id}.")
        else:
            # If creation fails, check if the category already exists
            response = requests.get(f"{website_url}/wp-json/wp/v2/categories",auth=HTTPBasicAuth(username, password))
            if response.status_code == 200:  # Successfully fetched categories
                categories = response.json()
                for category in categories:
                    if cat_name.lower() == category['name'].lower():
                        id = str(category['id'])
                        print(f"Found existing category '{cat_name}' with ID {id}.")
                        break
            else:
                print(f"Failed to fetch categories. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error handling category '{cat_name}': {e}")
    return id


def create_category(cat_name, website_url, headers):
    """
    Create a category if it doesn't exist, or return its ID if it exists.
    """
    if not cat_name:
        print("Category name is empty. Skipping.")
        return None

    id = None
    data = {"name": cat_name}

    try:
        # Attempt to create the category
        response = requests.post(
            f"{website_url}/wp-json/wp/v2/categories",
            headers=headers,
            json=data
        )

        if response.status_code == 201:  # Category created successfully
            id = str(response.json().get('id'))
            print(f"Created new category '{cat_name}' with ID {id}.")
        else:
            # If creation fails, check if the category already exists
            response = requests.get(
                f"{website_url}/wp-json/wp/v2/categories",
                headers=headers
            )

            if response.status_code == 200:  # Successfully fetched categories
                categories = response.json()
                for category in categories:
                    if cat_name.lower() == category['name'].lower():
                        id = str(category['id'])
                        print(f"Found existing category '{cat_name}' with ID {id}.")
                        break
            else:
                print(f"Failed to fetch categories. Status code: {response.status_code}")

    except Exception as e:
        print(f"Error handling category '{cat_name}': {e}")

    return id
```
## 04. Create Image
```py

def create_img(file_path, website_url, username, password):
        media = {'file': open(file_path, 'rb')}
        json_url = f"{website_url}/wp-json/wp/v2/media"
        image = requests.post(json_url + '/media',  auth=HTTPBasicAuth(username, password), files=media)
        post_id = int(json.loads(image.content.decode('utf-8'))['id'])
        # image_title = keyword.replace('-', ' ').split('.')[0]
        # post_id = str(json.loads(image.content.decode('utf-8'))['id'])
        # source = json.loads(image.content.decode('utf-8'))['guid']['rendered']
        # image1 = '<!-- wp:image {"align":"center","id":' + post_id + ',"sizeSlug":"full","linkDestination":"none"} -->'
        # image2 = '<div class="wp-block-image"><figure class="aligncenter size-full"><img src="' + source + '" alt="' + image_title + '" title="' + image_title + '" class="wp-image-' + post_id + '"/></figure></div>'
        # image3 = '<!-- /wp:image -->'
        # image_wp = image1 + image2 + image3
        # f_img = [post_id, image_wp]
        # logger.info('Feature Img Done..')
        return post_id
```
## 05.  Create AI Image
```py
import openai
openai.api_key = "XXXXXXXXXXXXX"
def get_image_link(prompt, size="1024x1024"):
    """Generates an image using OpenAI's DALL·E API based on a text prompt."""
    print(f'{datetime.now()} - Working in get image link Section...')
    try:
      response = openai.Image.create(
          prompt=prompt,
          n=1,
          size=size
      )
      return response['data'][0]['url']
    except:
      return ''

def feature_image(keyword, headers, website_url):
    """Generates and post a feature image for a given prompt."""

    prompt = "Generate a blog post image for this keyword: <<keyword>>"
    prompt = prompt.replace('<<keyword>>', keyword)

    print(f'{datetime.now()} - Working in feature image Section...')

    img_url = get_image_link(prompt, size="1024x1024")
    if len(img_url) == 0:
        return 0

    if not os.path.exists(img_path):
        os.makedirs(img_path)
    try:
      headers_fox = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
      response = requests.get(img_url, stream=True, headers=headers_fox)
      local_file = open(f'{img_path}/' + keyword + '.jpg', 'wb')
      response.raw.decode_content = True
      shutil.copyfileobj(response.raw, local_file)
      im = Image.open(f'{img_path}/' + keyword + '.jpg')
      resized_im = im.resize((round(im.size[0] * 0.8), round(im.size[1] * 0.8)))
      resized_im.save(f'{img_path}/' + keyword + '.jpg')
      media = {'file': open(f'{img_path}/' + keyword + '.jpg', 'rb')}
      image = requests.post(website_url + '/wp-json/wp/v2/media', headers=headers, files=media)
      img_id = str(json.loads(image.content.decode('utf-8'))['id'])
      return img_id
    except Exception as ops:
        print(f'error : {str(ops)}\n\n')
        return 0
```
## 06. Auto Image Upload
```py
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse

username = "admin"
password = ""

# Cache for uploaded image URLs
uploaded_images = {}
def img_upload(img_link):
    if img_link in uploaded_images:
        print(f"[DEBUG] Using cached image URL: {img_link} -> {uploaded_images[img_link]}")
        return uploaded_images[img_link]
    try:
        img_response = requests.get(img_link, stream=True)
        if img_response.status_code == 200:
            filename = urlparse(img_link).path.split("/")[-1]
            content_type_map = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.bmp': 'image/bmp',
                '.webp': 'image/webp',
                '.svg': 'image/svg+xml',
                '.ico': 'image/x-icon'
            }
            extension = '.' + filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
            content_type = content_type_map.get(extension, img_response.headers.get("content-type", "image/jpeg"))
            headers = {
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": content_type
            }
            wp_media_url = "https://domain.org/wp-json/wp/v2/media"
            wp_response = requests.post(
                wp_media_url,
                auth=HTTPBasicAuth(username, password),
                headers=headers,
                data=img_response.content
            )
            if wp_response.status_code == 201:
                new_img_url = wp_response.json().get("source_url")
                uploaded_images[img_link] = new_img_url
                print(f"[DEBUG] Image uploaded successfully: {img_link} -> {new_img_url}")
                return new_img_url
            else:
                print(f"[DEBUG] Failed to upload image: {img_link}, Status: {wp_response.status_code}")
        else:
            print(f"[DEBUG] Failed to download image: {img_link}, Status: {img_response.status_code}")
    except Exception as e:
        print(f"[DEBUG] Error uploading image {img_link}: {str(e)}")
    return img_link
```
## 07. File Upload
```py
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse

username = "admin"
password = "Bpqs "

uploaded_files = {}  # cache to avoid duplicate uploads


def file_upload(file_url):
    if file_url in uploaded_files:
        print(f"[DEBUG] Using cached file URL: {file_url} -> {uploaded_files[file_url]}")
        return uploaded_files[file_url]

    try:
        response = requests.get(file_url, stream=True)
        if response.status_code == 200:
            filename = urlparse(file_url).path.split("/")[-1]
            extension = '.' + filename.split('.')[-1].lower() if '.' in filename else ''

            content_type_map = {
                # 📄 Documents
                ".pdf": "application/pdf",
                ".doc": "application/msword",
                ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                ".ppt": "application/vnd.ms-powerpoint",
                ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                ".xls": "application/vnd.ms-excel",
                ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ".zip": "application/zip",
                ".rar": "application/vnd.rar",
                ".txt": "text/plain",

                # 🖼️ Images (optional, for completeness)
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp",
                ".bmp": "image/bmp",
                ".svg": "image/svg+xml",

                # 🎵 Audio
                ".mp3": "audio/mpeg",
                ".ogg": "audio/ogg",
                ".wav": "audio/wav",

                # 🎥 Video
                ".mp4": "video/mp4",
                ".webm": "video/webm"
            }

            content_type = content_type_map.get(extension,
                                                response.headers.get("content-type", "application/octet-stream"))
            headers = {
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": content_type
            }

            wp_media_url = "https://domain.org/wp-json/wp/v2/media"
            wp_response = requests.post(
                wp_media_url,
                auth=HTTPBasicAuth(username, password),
                headers=headers,
                data=response.content
            )

            if wp_response.status_code == 201:
                new_url = wp_response.json().get("source_url")
                uploaded_files[file_url] = new_url
                print(f"[DEBUG] File uploaded successfully: {file_url} -> {new_url}")
                return new_url
            else:
                print(f"[DEBUG] Failed to upload file: {file_url}, Status: {wp_response.status_code}")
        else:
            print(f"[DEBUG] Failed to download file: {file_url}, Status: {response.status_code}")
    except Exception as e:
        print(f"[DEBUG] Error uploading file {file_url}: {str(e)}")

    return file_url
```
