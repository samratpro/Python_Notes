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

