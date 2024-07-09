import pytest
import random
import session6
import os
import inspect
import re
from session6 import checker
from session6 import fibonacci_closure
from session6 import function_counter_with_one_dict,func_count
from session6 import function_counter_multi_dict

README_CONTENT_CHECK_FOR = [
    'checker',
    'docstring',
    'function',
    'TypeError',
     'count',
     'dict'
]

def test_session6_readme_exists():
    """ 
        This test checks whether a README.md file exists in the current project
    """
    assert os.path.isfile("README.md"), "README.md file missing!"


def test_session6_readme_500_words():
    """ 
        This test checks whether the readme file contains atleast 500 words
    """
    readme = open("README.md", "r")
    readme_words = readme.read().split()
    readme.close()
    assert len(readme_words) >= 500, "Make your README.md file interesting! Add atleast 500 words"

def test_session6_readme_proper_description():
    """ 
        This test cheecks whether the readme file contains good description of the assignment and
        checks if it has expected keywords. The keywords are defined globally in this file.
    """
    READMELOOKSGOOD = True
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    for c in README_CONTENT_CHECK_FOR:
        if c not in content:
            READMELOOKSGOOD = False
            pass
    assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your README.md file"

def test_session6_readme_file_for_more_than_10_hashes():
    """ 
        This code checks for formatting for readme file exisits. 
        It checks if there are hashes in the file which indicates
        usage of heading and comments in the readme file.There must 
        be atleast 10 hashes for function test to pass. 
    """
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    assert content.count("#") >= 10

def test_session6_indentations():
    """ 
        Returns pass if used four spaces for each level of syntactically \
        significant indenting (spaces%4 == 2 and spaces%4 ==0).
    """
    lines = inspect.getsource(session6)
    spaces = re.findall('\n +.', lines)
    for space in spaces:
        assert len(space) % 4 == 2, "Your script contains misplaced indentations"
        assert len(re.sub(r'[^ ]', '', space)) % 4 == 0, "Your code indentation does not follow PEP8 guidelines"


def test_session6_function_name_had_cap_letter():
    """
        This test checks whether the functions defined in the assignment
        file contains captial letters. As per the standard functions must
        not be defined in capital letters.
    """
    functions = inspect.getmembers(session6, inspect.isfunction)
    for function in functions:
        assert len(re.findall('([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"



##############################Validations for Docstring Checker Closure###########################

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

######################## Validations for Next Fibbonacci Number Closure#################################

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
    This function checks if fibbonacci series is generated correctly
    for given number of calls.
    '''
    x=[]
    next_fibbonacci=fibonacci_closure()
    for _ in range(10):
        x.append(next_fibbonacci())
    assert x==[0, 1, 1, 2, 3, 5, 8, 13, 21, 34], 'Fibbonacci series is not working as expected'


######################## Validations for function counter with one dictionary ####################
@function_counter_with_one_dict
def add_1(a: int, b: int = 10) -> int:
    """
    This function adds two numbers of any type and returns the sum.
    """
    return a + b

@function_counter_with_one_dict
def mul_1(a:int, b:int) -> int:
    """
    This function return product of two given numbers a and b.
    """
    return a*b

@function_counter_with_one_dict
def div_1(a:int, b:int) -> int:
    """
    This function return division of two given numbers a and b.
    """
    if b != 0:
        return a / b
    else:
        raise ValueError("Cannot divide by zero")

def test_argument_type():
    """Test cases for counter object type passed"""

    # Test 1: Non-function object should raise TypeError
    with pytest.raises(TypeError, match=r"The passed argument is not a function"):
        function_counter_with_one_dict("not_a_function")
    
    # Test 2: counter keeps track for function type and not Class type
    
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
        add_1(random.randint(1,10),random.randint(1,10))
        mul_1(random.randint(1,10), random.randint(1,10))
        div_1(random.randint(1,10), random.randint(1,10))
    
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
        add_1(random.randint(1,10),random.randint(1,10))
        mul_1(random.randint(1,10), random.randint(1,10))
        div_1(random.randint(1,10), random.randint(1,10))
    
    # Expected dictionary
    expected = {'add_1': 5, 'mul_1': 5, 'div_1': 5}
    
    # Assert that the func_count dictionary matches the expected dictionary
    assert func_count == expected, f"Expected {expected}, but got {func_count}"

######################## Validations for function counter with multiple dictionaries ####################

dict1={}
@function_counter_multi_dict(dict1)
def add_2(a: int, b: int = 10) -> int:
    """
    This function adds two numbers of any type and returns the sum.
    """
    return a + b

dict2={}
@function_counter_multi_dict(dict2)
def mul_2(a:int, b:int) -> int:
    """
    This function return product of two given numbers a and b.
    """
    return a*b

@function_counter_multi_dict(dict2)
def div_2(a:int, b:int) -> int:
    """
    This function return division of two given numbers a and b.
    """
    if b != 0:
        return a / b
    else:
        raise ValueError("Cannot divide by zero")


def test_argument_type_multi_dict():
    """Test cases for counter object type passed"""
    d1={}
    t1=function_counter_multi_dict(d1)
    # Test 1: Non-function object should raise TypeError
    with pytest.raises(TypeError, match=r"The passed argument is not a function"):
        t1("not_a_function")
    
    # Test 2: Counter keeps track for function type and not Class type
    
    with pytest.raises(TypeError, match=r"The passed argument is a class type"):
        d1={}
        @function_counter_multi_dict(d1)
        class ExampleClass:
            pass   

def test_argument_given_multi_dict():  
    #Test 3: No argument should raise TypeError for dictionary
    with pytest.raises(TypeError, match=r"missing 1 required positional argument: 'counter_dict'"):
        function_counter_multi_dict()

    # Test 4: No argument to decorator must raise exception
    with pytest.raises(TypeError, match=r"missing 1 required positional argument: 'fn'"):
        d1={}
        t1=function_counter_multi_dict(d1)
        t1()

#Test 5: Check if count is working properly
def test_function_call_counts_multi_dict():
    """
    This checks if counter dictionary is updating the values correctly for n number
    of times the functions are called to correct dictionaries called during function declarat
    """
    # Call each function 5 times
    for _ in range(5):
        add_2(random.randint(1,10),random.randint(1,10))
        mul_2(random.randint(1,10), random.randint(1,10))
        div_2(random.randint(1,10), random.randint(1,10))
    
    # Expected dictionary
    expected1 = {'add_2': 5}
    expected2 = {'mul_2': 5, 'div_2': 5}
    
    # Assert that the dictionary matches the expected dictionary respectively
    assert dict1 == expected1 and dict2==expected2 , f"Count is not updated to correct dictionaries"

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
        add_2(random.randint(1,10),random.randint(1,10))
        mul_2(random.randint(1,10), random.randint(1,10))
        div_2(random.randint(1,10), random.randint(1,10))
    
    # Expected dictionary
    expected1 = {'add_2': 10}
    expected2 = {'mul_2': 10, 'div_2': 10}
    
    # Assert that the dictionary matches the expected dictionary respectively
    assert dict1 == expected1 and dict2==expected2 , f"Count is not updated to correct dictionaries after resetting counter"
