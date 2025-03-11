### 01. How to start Python
- Installing Python: Python installation and setting up the environment.
- Understanding the Workspace: Explanation of Python project structure (scripts, modules, packages).
- Basic Commands: `python`, `python3`, `pip`, `pip install`, `python -m venv`.

### 02. Data Types and common variable rules
- Variable Declaration: Using `var` and constants, and understanding variable assignments.
- Zero Values: Default values of variables (None for uninitialized).
- Type Inference: Python’s dynamic typing and type hints.
- Type Casting: Implicit and explicit type casting (e.g., `int()`, `str()`).

### 03. Statement
- If-Else: Handling multiple conditions and nested if-else.
- Elif and else: Efficient conditional handling.
- Ternary Operator: Using conditional expressions for compact conditionals.
- Exception Handling: Using `try-except` for error handling.

### 04. Loop
- Basic `for` Loop: Looping over sequences such as lists, tuples, and strings.
- `while` Loop: Using while loops for condition-based iteration.
- Iterating with `enumerate`: Iterating over an index and value in loops.
- Break, Continue, and Else in loops: Controlling flow in loops.

### 05. Function
- Function Definition: Using `def` to define functions.
- Arguments and Parameters: Positional, keyword, and default arguments.
- Named Return Values: Returning multiple values from a function.
- Lambda Functions: Anonymous functions in Python.
- Recursive Functions: Functions calling themselves for problem-solving.
- Function as First-Class Citizens: Passing functions as arguments (callbacks).

### 06. Common Built-in Methods
- Time and Sleep:
  - Formatting and parsing time with `datetime` and `time`.
  - Using `time.sleep()` for delays.
- Type and Typecasting:
  - Checking types with `type()`.
  - Converting between data types (`int()`, `str()`, `list()`).
- List Operations:
  - `append`, `remove`, `pop`, `insert`, `extend`, `sort`, `reverse`.
- String Operations:
  - Concatenation, `split()`, `join()`, `strip()`.
- Collection Methods:
  - `len()`, `max()`, `min()`, `sum()`, `sorted()`.

### 07. Callback Methods
- Passing Functions as Arguments:
  - Defining and using callback functions.
  - Using closures for callback behavior.
- Asynchronous Callbacks:
  - Using `async` and `await` for asynchronous functions.
- Higher-order Functions:
  - Functions that return other functions.

### 08. String Manipulation
- String Operations:
  - Concatenation, splitting, trimming with `strip()`, and joining with `join()`.
  - Replacing, finding substrings, and formatting strings.
- String Formatting:
  - Using f-strings, `.format()`, and `%` formatting.
- Regular Expressions:
  - Using the `re` module for pattern matching and text manipulation.
- String Conversion:
  - Converting strings to other types (`int()`, `float()`, etc.).

### 09. List, Tuple, Dictionary, Set, Class (also project base usecase)
- List:
  - Creating and manipulating lists with methods like `append()`, `insert()`, and `pop()`.
  - List comprehensions for concise creation.
- Tuple:
  - Immutable sequences and unpacking.
  - Iterating over tuples and using them as function arguments.
- Dictionary:
  - Creating and manipulating key-value pairs.
  - Using methods like `get()`, `items()`, `keys()`, and `values()`.
- Set:
  - Creating and using sets for unique collections and set operations (union, intersection, etc.).
- Class:
  - Creating classes using `class` and instantiating objects.
  - Defining methods, class variables, and instance variables.

### 10. Strong OOP in Python (following Java)
- Classes and Objects:
  - Understanding `class`, `__init__`, and instance methods.
  - Object instantiation and method invocation.
  - Class attribute vs instance attribute
    ```py
    # class attribute can be update with class level
    # instance attribute can be update with instance level
    # class attribute can be instance attribute with self keyword
    # class
    class test:
        api = "xx"
    
        def __init__(self, x):
            self.x = x
        def check(self):
            print(self.api, '1')  # instance attribute
            print(test.api, '2')  # class attribute
    
    t = test('x')
    t.api = "Data"
    t.check()
    
    test.api = "Data 2"
    print(test.api)
    
    # Output:
    # Data 1
    # xx 2
    # Data 2
    ```
- Inheritance:
  - Subclassing classes and overriding methods.
- Polymorphism:
  - Dynamic method resolution and overriding methods in child classes.
- Encapsulation:
  - Using private and protected members.
  - Getter and Setter methods (`@property`, `@setter`).
- Design Patterns:
  - Common patterns like Singleton, Factory, and Observer in Python.

### 11. Threading, Basic Request, Data Scraping etc
- Threading:
  - Using the `threading` module for concurrency.
  - Managing threads with `Thread`, `Lock`, `Semaphore`.
- Requests:
  - Sending HTTP requests using the `requests` library.
  - Handling HTTP responses and status codes.
- Data Scraping:
  - Using `BeautifulSoup` or `Scrapy` for web scraping.
  - Parsing and extracting data from HTML/XML.
  - Automating browser actions with `Selenium`.

### 12. Error Handling (Try Except)
- Error Handling Idioms:
  - Using `try-except` blocks for synchronous error handling.
  - Handling multiple exception types using `except`.
- Custom Errors:
  - Defining custom exception classes.
  - Raising exceptions with `raise`.
- Handling Uncaught Exceptions:
  - Using `try-except-finally` for cleanup and resource management.

### 13. File Handling and IO
- File Operations:
  - Reading and writing files with built-in functions (`open()`, `read()`, `write()`).
  - Using `with open()` for automatic file closing.
- Buffering:
  - Reading and writing files in chunks for efficient IO.
- File Manipulation:
  - Renaming, deleting, and checking file existence using `os` and `shutil` modules.
