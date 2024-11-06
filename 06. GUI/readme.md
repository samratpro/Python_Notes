# Content
```
Databse Handle with SQLAlchemy ORM (sync) - CRUD
Databse Handle with Tortoise ORM (async) - CRUD with Example
Databe handle without any ORM - CRUD
```

### i. Databse Handle with SQLAlchemy ORM
```bash
pip install sqlalchemy
pip install sqlalchemy alembic   # for db migrations
```
DB Migrations
```bash
alembic init alembic       # This will create a new alembic folder with configuration files and a migration script folder
# Open the generated alembic.ini   sqlalchemy.url = sqlite:///websites.db
# Next, modify the env.py
```
```py
# env.p
from app.models import Base  # Import your Base (declarative_base) from models
target_metadata = Base.metadata
```
```bash
alembic revision --autogenerate -m "Initial migration"  # create your first migration  ` initial migrations is comment `
alembic upgrade head                                    # Apply the Migration                       
```
#### 01. Define the Database Models SQLAlchemy ORM (Create)
```py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Set up SQLite database and base
Base = declarative_base()

# Website Model
class Website(Base):
    __tablename__ = 'websites'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)

    # Relationship to connect website with its pages
    pages = relationship('Page', back_populates='website', cascade='all, delete-orphan')

# Page Model
class Page(Base):
    __tablename__ = 'pages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    content = Column(String, nullable=False)
    
    # Foreign key linking to Website
    website_id = Column(Integer, ForeignKey('websites.id'))
    
    # Relationship to access website from page
    website = relationship('Website', back_populates='pages')

# Create SQLite engine and session
engine = create_engine('sqlite:///websites.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(engine)
```
#### 02. Insering Data SQLAlchemy ORM (Write)
```py
# Add a website and its pages
new_website = Website(name="Example", url="https://example.com")
new_website.pages = [
    Page(url="https://example.com/page1", content="Content of Page 1"),
    Page(url="https://example.com/page2", content="Content of Page 2")
]

session.add(new_website)
session.commit()

# Add another website and its pages
another_website = Website(name="Another Website", url="https://anotherwebsite.com")
another_website.pages = [
    Page(url="https://anotherwebsite.com/page1", content="Content of Another Website Page 1"),
    Page(url="https://anotherwebsite.com/page2", content="Content of Another Website Page 2")
]

session.add(another_website)
session.commit()
```
#### 03. Querying & Filter Data SQLAlchemy ORM (Read)
```py
# Fetch all pages of a specific website
website = session.query(Website).filter_by(name="Example").first()

# Access all pages related to this website
for page in website.pages:
    print(f"Page URL: {page.url}, Content: {page.content}")
```
```py
website_id = website.id
pages = session.query(Page).filter_by(website_id=website_id).all()

for page in pages:
    print(f"Page URL: {page.url}, Content: {page.content}")
```
#### 04. Update data SQLAlchemy ORM (Update)
```py
# Update example function
def update_website(website_id, new_name=None, new_url=None):
    # Fetch the website record by id
    website = session.query(Website).filter(Website.id == website_id).first()
    
    if website:
        if new_name:
            website.name = new_name
        if new_url:
            website.url = new_url
        
        session.commit()  # Save changes to the database
        print(f"Updated website: {website.name}, {website.url}")
    else:
        print("Website not found.")

# Example usage
update_website(1, new_name="Updated Example", new_url="https://updatedexample.com")
```
#### 05. Delete Data
delete a page
```py
# Delete a page by its ID
def delete_page(page_id):
    page = session.query(Page).filter(Page.id == page_id).first()
    if page:
        session.delete(page)  # Remove the page from the session
        session.commit()       # Commit the changes
        print(f"Deleted page with ID: {page_id}")
    else:
        print("Page not found.")

# Example usage
delete_page(1)
```
To delete a website (and all related pages due to the cascade option set by the relationship)
```py
# Delete a website by its ID
def delete_website(website_id):
    website = session.query(Website).filter(Website.id == website_id).first()
    if website:
        session.delete(website)  # This will also delete related pages
        session.commit()
        print(f"Deleted website with ID: {website_id}")
    else:
        print("Website not found.")

# Example usage
delete_website(1)
```
Delete All data
```py
def delete_all_pages():
    session.query(Page).delete()  # This will delete all records from the pages table
    session.commit()               # Commit the changes
    print("All pages deleted.")
# Example usage
delete_all_pages()

def delete_all_websites():
    session.query(Website).delete()  # This will delete all records from the websites table
    session.commit()                  # Commit the changes
    print("All websites deleted.")
# Example usage
delete_all_websites()

def delete_all_data():
    session.query(Page).delete()  # Delete all pages first
    session.query(Website).delete()  # Then delete all websites
    session.commit()                  # Commit the changes
    print("All websites and pages deleted.")
# Example usage
delete_all_data()
```





### ii. Databse Handle with Tortoise ORM
```bash
pip install tortoise-orm aiosqlite
pip install tortoise-orm aerich        # DB Migrations
```
DB Migrations
```bash
aerich init -t app.models   # `app.models` refers to your Tortoise settings module
aerich init-db              # Create the First Migration
aerich migrate              # Run More Migrations:
aerich upgrade              # Apply the Migrations
```
#### 01. Define Models in Tortoise ORM (initial)
```
app        : Folder Name
models     : models.py db file name
aerich.models  : for DB migrations
```
config.json
```json
{
    "connections": {
        "default": "sqlite://websites.db"
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default"
        }
    }
}

```
```py
from tortoise import Tortoise, fields
from tortoise.models import Model


# Define Website model
class Website(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    url = fields.CharField(max_length=255)

    # Reverse relation to the Page model
    pages: fields.ReverseRelation['Page']


# Define Page model
class Page(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=255)
    content = fields.TextField()

    # ForeignKeyField to link Page to Website
    website = fields.ForeignKeyField('models.Website', related_name='pages')


# Initialize the Tortoise ORM
async def init():
    await Tortoise.init(
        db_url='sqlite://websites.db',
        modules={'models': ['__main__']}
    )
    await Tortoise.generate_schemas()

# Call the init function to initialize the database schema
import asyncio
asyncio.run(init())
```
#### 02. Insert Data into the Database in Tortoise ORM (Create)
```py
async def add_website_with_pages():
    # Create a new website
    website = await Website.create(name="Example", url="https://example.com")

    # Add multiple pages for the website
    await Page.create(url="https://example.com/page1", content="Page 1 content", website=website)
    await Page.create(url="https://example.com/page2", content="Page 2 content", website=website)

    # Add another website with pages
    another_website = await Website.create(name="Another Website", url="https://anotherwebsite.com")
    await Page.create(url="https://anotherwebsite.com/page1", content="Another Website Page 1 content", website=another_website)

# Run the async function to add data
asyncio.run(add_website_with_pages())
```
#### 03. Querying & Filtering Data in Tortoise ORM (Read)
```py
async def filter_pages_by_website():
    # Fetch all pages for the website with id=1
    pages = await Page.filter(website_id=1)

    for page in pages:
        print(f"Page URL: {page.url}, Content: {page.content}")

# Run the filter function
asyncio.run(filter_pages_by_website())
```
#### 04. Data Update in Tortoise ORM (Update)
```py
async def update_website(website_id, new_name=None, new_url=None):
    # Fetch the website record by id
    website = await Website.get(id=website_id)
    
    if website:
        if new_name:
            website.name = new_name
        if new_url:
            website.url = new_url
        
        await website.save()  # Save changes to the database
        print(f"Updated website: {website.name}, {website.url}")
    else:
        print("Website not found.")

# Example usage
async def main():
    await init()  # Initialize Tortoise ORM
    await update_website(1, new_name="Updated Example", new_url="https://updatedexample.com")

run_async(main())
```
#### 05: Delete Operation in Tortoise ORM (Delete)
delete a page
```py
# Delete a page by its ID
async def delete_page(page_id):
    page = await Page.get(id=page_id)
    await page.delete()  # Delete the page
    print(f"Deleted page with ID: {page_id}")

# Example usage
async def main():
    await init()  # Initialize Tortoise ORM
    await delete_page(1)

run_async(main())
```
delete a website (and all related pages automatically due to the foreign key constraint):
```py
# Delete a website by its ID
async def delete_website(website_id):
    website = await Website.get(id=website_id)
    await website.delete()  # This will also delete related pages
    print(f"Deleted website with ID: {website_id}")

# Example usage
async def main():
    await init()  # Initialize Tortoise ORM
    await delete_website(1)

run_async(main())
```
Delete All Pages
```py
async def delete_all_pages():
    await Page.all().delete()  # Delete all pages
    print("All pages deleted.")

# Example usage
async def main():
    await init()  # Initialize Tortoise ORM
    await delete_all_pages()

run_async(main())
```
Delete All Websites
```py
async def delete_all_websites():
    await Website.all().delete()  # Delete all websites
    print("All websites deleted.")

# Example usage
async def main():
    await init()  # Initialize Tortoise ORM
    await delete_all_websites()

run_async(main())
```
Delete All Page & Websites
```py
async def delete_all_data():
    await Page.all().delete()      # Delete all pages first
    await Website.all().delete()   # Then delete all websites
    print("All websites and pages deleted.")

# Example usage
async def main():
    await init()  # Initialize Tortoise ORM
    await delete_all_data()

run_async(main())
```

#### 06. Example Add Web Crawling in Tortoise ORM
```py
import aiohttp
import asyncio
from tortoise import Tortoise, fields, run_async
from tortoise.models import Model

# Define your models
class Website(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    url = fields.CharField(max_length=255)
    pages: fields.ReverseRelation['Page']

class Page(Model):
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=255)
    content = fields.TextField()
    website = fields.ForeignKeyField('models.Website', related_name='pages')

# Tortoise ORM initialization
async def init():
    await Tortoise.init(config="config.json")
    await Tortoise.generate_schemas()

async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

async def crawl_websites(websites):
    async with aiohttp.ClientSession() as session:
        for website in websites:
            main_page_content = await fetch_page(session, website['url'])
            website['pages'] = [{'url': website['url'], 'content': main_page_content}]

async def save_crawled_data(crawled_data):
    for site in crawled_data:
        website, _ = await Website.get_or_create(name=site['name'], url=site['url'])
        for page_data in site['pages']:
            await Page.create(url=page_data['url'], content=page_data['content'], website=website)

async def main():
    await init()  # Initialize Tortoise ORM
    crawled_data = [
        {"name": "Example", "url": "https://example.com"},
        {"name": "Another Website", "url": "https://anotherwebsite.com"},
    ]
    await crawl_websites(crawled_data)  # Step 1: Crawl the websites
    await save_crawled_data(crawled_data)  # Step 3: Save crawled data to DB

run_async(main())
```




### iii. Databse Handle without ORM
#### 01: Create the Database and Tables (initial)
```py
import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect('websites.db')
cursor = connection.cursor()

# Create a table for websites
cursor.execute('''
CREATE TABLE IF NOT EXISTS websites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    content TEXT
)
''')

# Create a table for pages with a foreign key referencing websites
cursor.execute('''
CREATE TABLE IF NOT EXISTS pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    content TEXT,
    FOREIGN KEY (website_id) REFERENCES websites(id) ON DELETE CASCADE
)
''')

# Commit changes and close the connection
connection.commit()
connection.close()
```
#### 02. Insert Data in Without ORM (Create)
```py
def create_website_with_pages(name, url, content, pages):
    connection = sqlite3.connect('websites.db')
    cursor = connection.cursor()
    
    # Insert the website first
    cursor.execute('''
    INSERT INTO websites (name, url, content) VALUES (?, ?, ?)
    ''', (name, url, content))
    
    website_id = cursor.lastrowid  # Get the ID of the newly inserted website
    
    # Insert pages for the website
    for page in pages:
        cursor.execute('''
        INSERT INTO pages (website_id, title, url, content) VALUES (?, ?, ?, ?)
        ''', (website_id, page['title'], page['url'], page['content']))
    
    connection.commit()
    connection.close()
    print(f"Website '{name}' with pages added.")

# Example usage
pages_data = [
    {'title': 'Home', 'url': 'https://example.com/home', 'content': 'Homepage content.'},
    {'title': 'About', 'url': 'https://example.com/about', 'content': 'About us content.'}
]
create_website_with_pages('Example', 'https://example.com', 'Example website content.', pages_data)
```
#### 03. Read Data in Without ORM (Read)
```py
def read_websites_with_pages():
    connection = sqlite3.connect('websites.db')
    cursor = connection.cursor()
    
    # Fetch all websites
    cursor.execute('SELECT * FROM websites')
    websites = cursor.fetchall()
    
    for website in websites:
        print(f"Website ID: {website[0]}, Name: {website[1]}, URL: {website[2]}")
        
        # Fetch pages for each website
        cursor.execute('SELECT * FROM pages WHERE website_id = ?', (website[0],))
        pages = cursor.fetchall()
        
        for page in pages:
            print(f"    Page ID: {page[0]}, Title: {page[2]}, URL: {page[3]}")
    
    connection.close()

# Example usage
read_websites_with_pages()
```
#### 04. Update data in Without ORM (Update)
```py
def update_page(page_id, new_title=None, new_url=None, new_content=None):
    connection = sqlite3.connect('websites.db')
    cursor = connection.cursor()
    
    if new_title:
        cursor.execute('UPDATE pages SET title = ? WHERE id = ?', (new_title, page_id))
    if new_url:
        cursor.execute('UPDATE pages SET url = ? WHERE id = ?', (new_url, page_id))
    if new_content:
        cursor.execute('UPDATE pages SET content = ? WHERE id = ?', (new_content, page_id))
    
    connection.commit()
    connection.close()
    print(f"Page with ID {page_id} updated.")

# Example usage
update_page(1, new_title='Updated Home')
```
#### 05. Delete Data in Without ORM (Delete)
Delete Pages
```py
def delete_page(page_id):
    connection = sqlite3.connect('websites.db')
    cursor = connection.cursor()
    
    cursor.execute('DELETE FROM pages WHERE id = ?', (page_id,))
    
    connection.commit()
    connection.close()
    print(f"Page with ID {page_id} deleted.")

# Example usage
delete_page(1)
```
Delete All Pages
```py
def delete_all_pages():
    cursor.execute('DELETE FROM pages')  # Delete all records from the pages table
    connection.commit()                   # Commit the changes
    print("All pages deleted.")

# Example usage
delete_all_pages()
```
Delete All Websites
```py
def delete_all_websites():
    cursor.execute('DELETE FROM websites')  # Delete all records from the websites table
    connection.commit()                      # Commit the changes
    print("All websites deleted.")

# Example usage
delete_all_websites()
```
Delete All Data from Both Tables
```py
def delete_all_data():
    cursor.execute('DELETE FROM pages')     # Delete all pages first
    cursor.execute('DELETE FROM websites')   # Then delete all websites
    connection.commit()                      # Commit the changes
    print("All websites and pages deleted.")

# Example usage
delete_all_data()
```



