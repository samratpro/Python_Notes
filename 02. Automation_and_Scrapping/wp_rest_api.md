## 01. Simple Posting
```py
import requests
from requests.auth import HTTPBasicAuth

url = "https://your-wordpress-site.com/wp-json/wp/v2/posts"

username = "your-username"
password = "your-application-password"

post_data = {
    "title": "Text Post",
    "content": "Test Content From App",
    "status": "draft"  # 'publish' / 'schedule'
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
```
## 04. Create Image
```py

def create_img(file_path, username, password):
        media = {'file': open(file_path), 'rb')}
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
