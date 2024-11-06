# Important template tags
---
| Tags                 | Description                                                  | Example                                            |
|--------------------  |--------------------------------------------------------------|----------------------------------------------------|
| `{% load static %} ` | calling static method                                        | `place {% load static %} at top of html file`|
| `{% static 'style.css' %} ` | calling css/js file                                   | `calling css or js file`|
| `{% static 'logo.svg' %} ` | calling static image file                              | `must be in static folder`|
| `{% for %}`        | Loops over a sequence                                          | `{% for item in items %} {{ item }} {% endfor %}`|
| `{% loop counter %}` | To serial a list                                             |  `{% for item in items %} {{ forloop.counter }} {% endfor %}` |
| `{% if %}`         | Checks if a condition is true                                | `{% if user.is_authenticated %} Hello, {{ user.username }}! {% endif %}` |
| `{% else %}`       | Provides an alternative for the preceding `{% if %}`         | `{% if user.is_authenticated %} Hello, {{ user.username }}! {% else %} Please log in. {% endif %}` |
| `{% endif %}`      | Ends an `{% if %}` block                                     | `{% if user.is_authenticated %} Hello, {{ user.username }}! {% endif %}` |
| `{% include %}`    | Includes another template inside the current template        | `{% include 'header.html' %}`                      |
| `{% extends %}`    | Inherits from a base template                                 | `{% extends 'base.html' %}`                        |
| `{% block %}`      | Defines a block that can be overridden in child templates    | `{% block content %} {% endblock %}`               |
| `{% endblock %}`   | Ends a `{% block %}`                                         | `{% block content %} {% endblock %}`               |
| `{% load %}`       | Loads custom template tags or filters                        | `{% load my_tags %}`          
| `{% url %}`        | Generates a URL based on a view and optional parameters      | `{% url 'view_name' arg1 arg2 %}`                  |
| `{% csrf_token %}` | Adds a CSRF token to a form                                  | `<form method="post">{% csrf_token %}</form>`      |
| `{% with %}`       | Assigns a value to a variable within a specific block        | `{% with total=items|length %} {{ total }} {% endwith %}` |
| `{% endwith %}`    | Ends a `{% with %}` block                                    | `{% with total=items|length %} {{ total }} {% endwith %}` |                     |
| `{% comment %}`    | Comments out a block of code in a template                   | `{% comment %} This will not be rendered {% endcomment %}` |
| `{% endcomment %}` | Ends a `{% comment %}` block                                 | `{% comment %} This will not be rendered {% endcomment %}` |
| `{% spaceless %}`  | Removes whitespace between HTML tags within a block          | `{% spaceless %}<p> No space </p>{% endspaceless %}` |
| `{% endspaceless %}` | Ends a `{% spaceless %}` block                             | `{% spaceless %}<p> No space </p>{% endspaceless %}` |
| `{% now %}`        | Displays the current date or time using a format string      | `{% now "Y-m-d H:i" %}`                             |
| `{% verbatim %}`   | Disables template tag processing within a block              | `{% verbatim %} {{ some_var }} {% endverbatim %}`  |
| `{% endverbatim %}` | Ends a `{% verbatim %}` block                               | `{% verbatim %} {{ some_var }} {% endverbatim %}`  |
