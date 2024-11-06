# Using logger instead of print function, cause live server can't show data like VS Code or Pycharm terminal

import logging
# Get an instance of a logger
logger = logging.getLogger("django")

def your_view_function(request):
    name = 'Samrat'
    age = 25
    logger.info('Appname.filename.py >>> This is bulk info posting page, testing for Python logger')
    logger.info(f'Appname.filename.py >>> This message in from logger, name: {name} and  age :{str(age)}')
    # Logger can take one argument not like print() function
    return render(request, template, context=context)
