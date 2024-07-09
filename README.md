# Assignment 6: Closures and Decorators in Python

This assignment focuses on understanding and implementing closures and decorators in Python.

## Functions

### Docstring Checker closure `checken(fn)`

A closure that checks if a function has a docstring of sufficient length before executing it.

- **Args**: `fn` (function): The function to be checked and potentially executed.
- **Raises**:
  - `TypeError`: If the passed argument is not a function or is a class type.
  - `ValueError`: If the function's docstring is missing or shorter than 50 characters.
- **Returns**: The inner function that enforces the docstring length check before calling the original function.

```python
@checker
def example_function():
    """This is an example function with a sufficiently long docstring."""
    return "Function executed"

print(example_function())  # Output: The function example_function has a description of more than 50 characters.
```

#### Tests for `checker(fn)`

```python
def test_closure_arguments():
    """Test cases for checker object type passed"""

    # Test 1: Non-function object should raise TypeError
    with pytest.raises(TypeError, match=r"The passed argument is not a function"):
        checker("not_a_function")
    
    # Test 2: Checker must check docstring only for function type and not Class type
    
    with pytest.raises(TypeError, match=r"The passed argument is a class type"):
        @checker
        class ExampleClass:
            """This is an example class with a docstring."""
            pass    

    #Test 3: No argument should raise TypeError
    with pytest.raises(TypeError, match=r"missing 1 required positional argument: 'fn'"):
        checker()

    # Test 4: Incorrect usage should raise TypeError
    with pytest.raises(TypeError, match=r"missing 1 required positional argument: 'fn'"):
        @checker()
        def some_function():
            pass
        some_function()

def test_closure_no_docstring():
    '''
    Test 5: Raises ValueError if no docstring is written for a function
    '''
    with pytest.raises(ValueError,match=r"The passed function has no docstring"):
        @checker
        def no_docstring_function():
            return "No docstring"
        no_docstring_function()

def test_closure_less_characters_docstring():
    '''
    Test 6: Function must raise Exception with relevant message if there are less than
    50 characters
    '''
    with pytest.raises(ValueError,match=r"requires a docstring longer than 50 characters"):
        @checker
        def short_docstring_function():
            """Short doc"""
            return "Short docstring"
        short_docstring_function()

def closure_function_run_test():
    '''
    Test 7: This function checks if a function with a sufficient docstring and passes
    without error.
    '''
    @checker
    def add(a: int, b: int = 10) -> int:
        """
        This function adds two numbers of any type and returns the sum.
        """
        return a + b

    assert add(10, 20) == 30
```

## Fibonacci Closure Function

### `fibonacci_closure()`

Returns a closure that generates the next Fibonacci number each time it is called.

This closure initializes with two initial values, `a` and `b`. Each time the
`next_fibonacci_number` function is called, it calculates the next Fibonacci
number based on the previous two numbers stored in `a` and `b`. The sequence
starts from 0.

### Returns

- **function**: A closure that returns the next Fibonacci number when called.

### Example

```python
fib = fibonacci_closure()
print(fib())  # Output: 0
print(fib())  # Output: 1
print(fib())  # Output: 1
print(fib())  # Output: 2
print(fib())  # Output: 3
```

### `next_fibonacci_number()`

Calculates the next Fibonacci number based on the previous two values.

This function does not accept any arguments. It raises a ValueError if
any arguments are passed.

### Raises

- **ValueError**: If any arguments are passed to the function.

### Returns

- **int**: The next Fibonacci number in the sequence.

```python
def fibonacci_closure():
    """
    Returns a closure that generates the next Fibonacci number each time it is called.

    This closure initializes with two initial values, `a` and `b`. Each time the
    `next_fibonacci_number` function is called, it calculates the next Fibonacci
    number based on the previous two numbers stored in `a` and `b`. The sequence
    starts from 0.

    Returns:
        function: A closure that returns the next Fibonacci number when called.

    Example:
        fib = fibonacci_closure()
        print(fib())  # Output: 0
        print(fib())  # Output: 1
        print(fib())  # Output: 1
        print(fib())  # Output: 2
        print(fib())  # Output: 3
    """
    a, b = 0, 1

    def next_fibonacci_number(*args, **kwargs):
        """
        Calculates the next Fibonacci number based on the previous two values.

        This function does not accept any arguments. It raises a ValueError if
        any arguments are passed.

        Raises:
            ValueError: If any arguments are passed to the function.

        Returns:
            int: The next Fibonacci number in the sequence.
        """
        if args or kwargs:
            raise ValueError("No arguments should be passed to this function.")

        nonlocal a, b
        next_val = a
        a, b = b, a + b
        return next_val

    return next_fibonacci_number

def test_fibonacci_no_arguments():
    '''
    This function runs some test to check for arguments passed to next_fibonacci closure
    '''
    next_fibonacci = fibonacci_closure()
    
    # Check that passing an argument raises a ValueError
    with pytest.raises(ValueError, match="No arguments should be passed to this function."):
        next_fibonacci(1)
    
    # Check that passing a keyword argument raises a ValueError
    with pytest.raises(ValueError, match="No arguments should be passed to this function."):
        next_fibonacci(arg=1)

def test_fibonacci_series_generated():
    '''
    This function checks if Fibonacci series is generated correctly
    for a given number of calls.
    '''
    x=[]
    next_fibonacci = fibonacci_closure()
    for _ in range(10):
        x.append(next_fibonacci())
    assert x == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34], 'Fibonacci series is not working as expected'
```

# Function Counter with One Dictionary

### `function_counter_with_one_dict(fn)`

A decorator that counts how many times a function is called and updates a global dictionary (`func_count`) with the counts.

### Args

- **fn (function)**: The function to be decorated and counted.

### Raises

- **TypeError**: If the passed argument is not a function or if it is a class type.

### Returns

- **function**: The inner function that wraps the original function and keeps track of the call count.

### Example

```python
@function_counter_with_one_dict
def add(a, b):
    return a + b

print(add(1, 2))  # Output: add has been called 1 times
print(add(3, 4))  # Output: add has been called 2 times
print(func_count)  # Output: {'add': 2}
```

### `inner()`

The inner function that wraps the original function and keeps track of the call count.

### Resets

- **reset_counter()**: Resets the call count (`cnt`) to zero.

```python
func_count = {}

def function_counter_with_one_dict(fn):
    """
    A decorator that counts how many times a function is called and updates a global dictionary with the counts.

    Args:
        fn (function): The function to be decorated and counted.

    Raises:
        TypeError: If the passed argument is not a function or if it is a class type.

    Returns:
        function: The inner function that wraps the original function and keeps track of the call count.

    Example:
        @counter_with_one_dict
        def add(a, b):
            return a + b

        print(add(1, 2))  # Output: add has been called 1 times
        print(add(3, 4))  # Output: add has been called 2 times
        print(func_count)  # Output: {'add': 2}
    """
    if not callable(fn):
        raise TypeError("The passed argument is not a function")
    if isinstance(fn, type):
        raise TypeError("The passed argument is a class type. Please use this closure only for functions")

    cnt = 0  # initially fn has been run zero times

    def inner(*args, **kwargs):
        nonlocal cnt
        global func_count
        inner.__name__ = fn.__name__
        inner.__doc__ = fn.__doc__
        cnt += 1
        func_count[fn.__name__] = cnt
        print('{0} has been called {1} times'.format(fn.__name__, cnt))
        return fn(*args, **kwargs)

    def reset_counter():
        nonlocal cnt
        cnt = 0

    inner.reset_counter = reset_counter

    return inner

def test_argument_type():
    """Test cases for counter object type passed"""

    # Test 1: Non-function object should raise TypeError
    with pytest.raises(TypeError, match=r"The passed argument is not a function"):
        function_counter_with_one_dict("not_a_function")
    
    # Test 2: Class type should raise TypeError
    with pytest.raises(TypeError, match=r"The passed argument is a class type"):
        @function_counter_with_one_dict
        class ExampleClass:
            pass    

def test_argument_given():      
    #Test 3: No argument should raise TypeError
    with pytest.raises(TypeError, match=r"missing 1 required positional argument: 'fn'"):
        function_counter_with_one_dict()

    # Test 4: Incorrect usage should raise TypeError
    with pytest.raises(TypeError, match=r"missing 1 required positional argument: 'fn'"):
        @function_counter_with_one_dict()
        def some_function():
            pass
        some_function()

#Test 5: Check if count is working properly
def test_function_call_counts():
    """
    This checks if counter dictionary is updating the values correctly for n number
    of times the functions are called.
    """
    # Call each function 5 times
    for _ in range(5):
        add_1(1, 2)
        mul_1(2, 3)
        div_1(4, 2)
    
    # Expected dictionary
    expected = {'add_1': 5, 'mul_1': 5, 'div_1': 5}
    
    # Assert that the func_count dictionary matches the expected dictionary
    assert func_count == expected, f"Expected {expected}, but got {func_count}"

#Test 6 : Check if docstrings of functions are not overwritten
def test_docstring_modification():
    '''
    This function checks if the docstrings of each function passed to counter is remained intact 
    even after calling decorator on top of function.
    '''
    assert ' This function adds two numbers of any type and returns the sum.' in add_1.__doc__, 'The docstring of function add is modified by decorator'

    assert 'This function return product of two given numbers a and b.' in mul_1.__doc__, 'The docstring of function mul is modified by decorator'

    assert 'This function return division of two given numbers a and b.' in div_1.__doc__, 'The docstring of function div is modified by decorator'


#Test 7: Check if functions are running as expected
def test_function_output():
    assert add_1(1, 2)==3, "Addition function is not working as expected"
    assert mul_1(2, 3)==6, "Multiplication function is not working as expected"
    assert div_1(4, 2)==2, "Division function is not working as expected"

#Test 8: Check if reset of global dictionary is working

def test_function_call_counts_after_reset():
    add_1.reset_counter()
    mul_1.reset_counter()
    div_1.reset_counter()
    # Call each function 5 times
    for _ in range(5):
        add_1(1, 2)
        mul_1(2, 3)
        div_1(4, 2)
    
    # Expected dictionary
    expected = {'add_1': 5, 'mul_1': 5, 'div_1': 5}
    
    # Assert that the func_count dictionary matches the expected dictionary
    assert func_count == expected, f"Expected {expected}, but got {func_count}"
```


## Function Counter with Multiple Dictionaries

### `function_counter_multi_dict(counter_dict)`

A decorator factory that counts how many times a function is called and updates a specified dictionary with the counts.

### Args

- **counter_dict (dict)**: The dictionary to be updated with the function call counts.

### Raises

- **TypeError**: If the passed `counter_dict` argument is not a dictionary.
- **TypeError**: If the passed argument is not a function or if it is a class type.

### Returns

- **function**: A decorator that wraps the original function and keeps track of the call count.

### Example

```python
dict1 = {}
@function_counter_multi_dict(dict1)
def add(a, b):
    return a + b

print(add(1, 2))  # Output: add has been called 1 times
print(add(3, 4))  # Output: add has been called 2 times
print(dict1)  # Output: {'add': 2}
```

## `inner()`

The inner function that wraps the original function and keeps track of the call count.

### Resets

- **reset_counter()**: Resets the call count (`cnt`) to zero.

```python
func_count = {}

def function_counter_multi_dict(counter_dict):
    """
    A decorator factory that counts how many times a function is called and updates a specified dictionary with the counts.

    Args:
        counter_dict (dict): The dictionary to be updated with the function call counts.

    Raises:
        TypeError: If the passed argument is not a function or if it is a class type.

    Returns:
        function: A decorator that wraps the original function and keeps track of the call count.

    Example:
        func_count = {}
        @function_counter_multi_dict(func_count)
        def add(a, b):
            return a + b

        print(add(1, 2))  # Output: add has been called 1 times
        print(add(3, 4))  # Output: add has been called 2 times
        print(func_count)  # Output: {'add': 2}
    """
    if not isinstance(counter_dict, dict):
        raise TypeError("The counter_dict argument must be a dictionary")

    def decorator(fn):
        if not callable(fn):
            raise TypeError("The passed argument is not a function")
        if isinstance(fn, type):
            raise TypeError("The passed argument is a class type. Please use this decorator only for functions")

        cnt = 0  # initially fn has been run zero times

        def inner(*args, **kwargs):
            nonlocal cnt
            inner.__name__ = fn.__name__
            inner.__doc__ = fn.__doc__
            cnt += 1
            counter_dict[fn.__name__] = cnt
            print('{0} has been called {1} times'.format(fn.__name__, cnt))
            return fn(*args, **kwargs)

        def reset_counter():
            nonlocal cnt
            cnt = 0

        inner.reset_counter = reset_counter

        return inner

    return decorator

def test_argument_type_multi_dict():
    """Test cases for counter object type passed"""

    # Test 1: Non-function object should raise TypeError
    with pytest.raises(TypeError, match=r"The passed argument is not a function"):
        function_counter_multi_dict("not_a_function")
    
    # Test 2: Class type should raise TypeError
    with pytest.raises(TypeError, match=r"The passed argument is a class type"):
        @function_counter_multi_dict({})
        class ExampleClass:
            pass   

def test_argument_given_multi_dict():  
    #Test 3: No argument should raise TypeError for dictionary
    with pytest.raises(TypeError, match=r"missing 1 required positional argument: 'counter_dict'"):
        function_counter_multi_dict()

    # Test 4: No argument to decorator must raise exception
    with pytest.raises(TypeError, match=r"missing 1 required positional argument: 'fn'"):
        t1 = function_counter_multi_dict({})
        t1()

#Test 5: Check if count is working properly
def test_function_call_counts_multi_dict():
    """
    This checks if counter dictionary is updating the values correctly for n number
    of times the functions are called to correct dictionaries called during function declarat
    """
    dict1 = {}
    dict2 = {}

    # Call each function 5 times
    for _ in range(5):
        add_2(1, 2)
        mul_2(2, 3)
        div_2(4, 2)
    
    # Expected dictionaries
    expected1 = {'add_2': 5}
    expected2 = {'mul_2': 5, 'div_2': 5}
    
    # Assert that the dictionaries match the expected dictionaries respectively
    assert dict1 == expected1 and dict2 == expected2, f"Count is not updated to correct dictionaries"

#Test 6 : Check if docstrings of functions are not overwritten
def test_docstring_modification_multi_dict():
    '''
    This function checks if the docstrings of each function passed to counter is remained intact 
    even after calling decorator on top of function.
    '''
    assert ' This function adds two numbers of any type and returns the sum.' in add_2.__doc__, 'The docstring of function add is modified by decorator'

    assert 'This function return product of two given numbers a and b.' in mul_2.__doc__, 'The docstring of function mul is modified by decorator'

    assert 'This function return division of two given numbers a and b.' in div_2.__doc__, 'The docstring of function div is modified by decorator'


#Test 7: Check if functions are running as expected
def test_function_output_multi_dict():
    assert add_2(1, 2)==3, "Addition function is not working as expected"
    assert mul_2(2, 3)==6, "Multiplication function is not working as expected"
    assert div_2(4, 2)==2, "Division function is not working as expected"

#Test 8: Check if reset of global dictionary is working

def test_function_call_counts_after_reset_multi_dict():
    add_2.reset_counter()
    mul_2.reset_counter()
    div_2.reset_counter()
    # Call each function 10 times
    for _ in range(10):
        add_2(1, 2)
        mul_2(2, 3)
        div_2(4, 2)
    
    # Expected dictionaries
    expected1 = {'add_2': 10}
    expected2 = {'mul_2': 10, 'div_2': 10}
    
    # Assert that the dictionaries match the expected dictionaries respectively
    assert dict1 == expected1 and dict
```