## 01. models.py
```py
from django.db import models

class NavigationItem(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name='children'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
```
## 02. admin.py
```py
from django.contrib import admin
from .models import NavigationItem

class NavigationItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'order', 'parent', 'is_active')
    list_filter = ('is_active', 'parent')
    ordering = ('order',)

admin.site.register(NavigationItem, NavigationItemAdmin)
```
## 03. context_processors.py
```py
from .models import NavigationItem

def navigation(request):
    nav_items = NavigationItem.objects.filter(is_active=True, parent=None).order_by('order')
    return {'nav_items': nav_items}
```
## 04. settings.py
```py
TEMPLATES = [
    {
        # Other template settings...
        'OPTIONS': {
            'context_processors': [
                # Other context processors...
                'your_app.context_processors.navigation',
            ],
        },
    },
]
```
## 05. base.html
```html
<nav>
    <ul>
        {% for item in nav_items %}
            <li>
                <a href="{{ item.url }}">{{ item.title }}</a>
                {% if item.children.all %}
                    <ul>
                        {% for child in item.children.all %}
                            <li><a href="{{ child.url }}">{{ child.title }}</a></li>
                        {% endfor %}
                    </ul>
                {% endif %}
            </li>
        {% endfor %}
    </ul>
</nav>
```
