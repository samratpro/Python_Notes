## 01. template.html
```html
<!-- Post Method -->
<form action="" method="post">
                                 <!-- Warning .............. form="usrform" We can't use like this type in our HTML element -->
{% csrf_token %}                 <!-- ...................... {% csrf_token %} is mendatory for post method -->
    <input name="Name">          <!-- ...................... name="value" will pass as a veriable -->
    <input name="Phone">
    <input name="Email">
    <select name="type" >                               <!-- .. We can pass optional value -->
        <option value="service"> Service </option>       
        <option value="query"> General Query </option>
    </select>
    <textarea name="comment"> Massage </textarea>
    <button type="submit"> Send Message </button>      <!-- ... type="submit" is mendatory and as last node of form -->
</form>


<!-- Get Method -->

<form action="" method="get">
    <input name="Name">          <!-- ................................................ name="value" will pass as a veriable -->
    <input name="Phone">
    <input name="Email">
    <select name="type" >                               <!-- ......................... We can pass optional value -->
        <option value="service"> Service </option>       
        <option value="query"> General Query </option>
    </select>
    <textarea name="comment"> Massage </textarea>
    <button type="submit"> Send Message </button>      <!-- .......................... type="submit" is mendatory -->
</form>


<!-- Two Form Submit Button -->
<form action="" class="mb-5" method="post">
    {% csrf_token %}
    <!-- Other form fields -->
    <button type="submit" name="action" value="send" id="sendBtn" class="btn brand-bg ms-3 mt-2 mb-5 px-5 py-2 fs-5">Send to Website</button>
    <button type="submit" name="action" value="update" id="updateBtn" class="btn brand-bg ms-3 mt-2 mb-5 px-5 py-2 fs-5">Update</button>
</form>



<!-- Current URL condition -->
class="{% if request.resolver_match.url_name == "urlname" %} actv {% endif %}"    <!-- ......  "urlname" is URL's Function name and "actv" is HTML class --> 


<!-- For Loop list -->
https://fedingo.com/how-to-loop-through-list-in-django-template/
```
## 02. views.py
```py
# Warning:---------- Complete first App's urls mapping and view.py

# Views File Output-------------------------------
from django.http import HttpResponse # Only for Python Function Output...
from django.shortcuts import render


# Function Operation
def function_name(arg):
  operation = arg
  return operation


# Template Rendering Function..............
def home(request):
    template = 'NewApp/home.html'
    
    if request.method == 'GET' and 'city_search' in request.GET:        # Get alternative is POST...
        input_data = request.GET.get('city_search')                     # city_search form name of HTML input...
        result = function_name(input_data)                              # function_name is a function...   
        contex = {'result':result}
    else:
        contex = {}
        
    return render(request, template, contex) # Return for Templates


# Template Rendering Function............
def contact(request):
    template = 'NewApp/home.html'
    
    if request.method == 'POST' and 'city_search' in request.POST:        # POST alternative is GET...
        input_data = request.POST.get('city_search')                     # city_search form name of HTML input...
        result = function_name(input_data)                              # function_name is a function...   
        contex = {'result':result}
    else:
        contex = {}
        
    return render(request, template, contex) # Return for Templates



# Two Form Submit Button .................
def complete_generated_single_view(request, id):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'send':
            # Logic for sending the news to the website
            pass
        elif action == 'update':
            # Logic for updating the news
            pass
        else:
            # Handle invalid action

    # Remain code in template.html
```
