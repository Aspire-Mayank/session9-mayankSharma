import pytest
import random
import string
import os
import inspect
import re
import math
from datetime import datetime
from decimal import Decimal
import session9
from session9 import *


FUNCTIONS_TO_CHECK_FOR = [
    'htmlize',
    'html_set',
    'html_dict',
    'html_list',
    'html_int',
    'html_escape',
    'html_real',
    'dec_timeavg',
    'try_certificate_auth',
    'set_sign_on',
    'debugger',
    'odd_sec'
]

WORDS_TO_CHECK_FOR = [
    'global',
    'local',
    'nonlocal',
    'decorators',
    'singledispatch'
]

# ----------------------------------------------Default TEST CASE START--------------------------------------------------#
def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md file missing!"

def test_readme_contents():
    readme = open("README.md", "r")
    readme_words = readme.read().split()
    readme.close()
    assert len(readme_words) >= 500, "Make your README.md file interesting! Add atleast 500 words"

def test_readme_proper_description():
    READMELOOKSGOOD = True
    f = open("README.md", "r")
    content = f.read()
    f.close()
    for c in WORDS_TO_CHECK_FOR:
        if c not in content:
            READMELOOKSGOOD = False
            pass
    assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your README.md file"

def test_function_are_listed():
    READMELOOKSGOOD = True
    f = open("README.md", "r")
    content = f.read()
    f.close()
    AllFUNCTIONSDEFINED = True
    for c in FUNCTIONS_TO_CHECK_FOR:
        if c not in content:
            AllFUNCTIONSDEFINED = False
            pass
    assert AllFUNCTIONSDEFINED == True, "You have not defined all the required functions"

def test_readme_file_for_formatting():
    f = open("README.md", "r")
    content = f.read()
    f.close()
    assert content.count("#") >= 10

def test_indentations():
    ''' Returns pass if used four spaces for each level of syntactically \
    significant indenting.'''
    lines = inspect.getsource(session9)
    spaces = re.findall('\n +.', lines)
    for space in spaces:
        assert len(space) % 4 == 2, "Your script contains misplaced indentations"
        assert len(re.sub(r'[^ ]', '', space)) % 4 == 0, "Your code indentation does not follow PEP8 guidelines" 

def test_function_name_had_cap_letter():
    functions = inspect.getmembers(session9, inspect.isfunction)
    for function in functions:
        assert len(re.findall('([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"

# ----------------------------------------------Default TEST CASE END--------------------------------------------------#

# ----------------------------------------------CUSTOM TEST CASE START--------------------------------------------------#


def test_odd_it_even():
    time = datetime.utcnow()
    
    @odd_sec(time)
    def add(a: int, b: int) -> int:
        return a + b
    assert add(1, 2) == None


def test_odd_it_odd():
    time = datetime.utcnow()
    
    @odd_sec(time)
    def add(a: int, b: int) -> int:
        return a + b
    assert add(1, 2) == 3


@try_certificate_auth(current_pass=set_sign_on(), user_pass='login@123')
def add_1(a: int, b: int) -> int:
    return a+b


@try_certificate_auth(current_pass=set_sign_on(), user_pass='login@123')
def add_2(a: int, b: int) -> int:
    return a+b


def test_authenticate_correct_password():
    session9.get_password = lambda : 'login@123'
    assert add_1(1, 2) == 3, "Something wrong with authentication."


def test_authenticate_incorrect_password():
    session9.get_password = lambda : 'login@456'
    assert add_2(1, 2) == None, "Something wrong with authentication."


@Firewall("high")
def calc_sal_h(base, **kwargs):
    return sum([base]+list(kwargs.values()))

@Firewall("mid")
def calc_sal_m(base, **kwargs):
    return sum([base]+list(kwargs.values()))

@Firewall("low")
def calc_sal_l(base, **kwargs):
    return sum([base]+list(kwargs.values()))

@Firewall("no")
def calc_sal_n(base, **kwargs):
    return sum([base]+list(kwargs.values()))

@Firewall()
def calc_sal_(base, **kwargs):
    return sum([base]+list(kwargs.values()))

def test_privileges():
    _ = calc_sal_h(base=1000000, bonus1=200000, bonus2=100000, bonus3=50000)
    assert _ == 1350000, "Privilege failed!"
    _ = calc_sal_m(base=1000000, bonus1=200000, bonus2=100000, bonus3=50000)
    assert _ == 1300000, "Privilege failed!"
    _ = calc_sal_l(base=1000000, bonus1=200000, bonus2=100000, bonus3=50000)
    assert _ == 1200000, "Privilege failed!"
    _ = calc_sal_n(base=1000000, bonus1=200000, bonus2=100000, bonus3=50000)
    assert _ == 1000000, "Privilege failed!"
    _ = calc_sal_(base=1000000, bonus1=200000, bonus2=100000, bonus3=50000)
    assert _ == 1000000, "Privilege failed!"


def test_singledispatch():
    assert htmlize(106) == '106(<i>0x6a</i>)'

    assert htmlize({'a': 1, 'b': 2, 'c': 3}) == """<ul>
<li>a=1</li>
<li>b=2</li>
<li>c=3</li>
</ul>"""

    assert htmlize('245 < 255') == '245 &lt; 255'

    assert htmlize('Any random text\n') == 'Any random text<br/>\n'

    assert htmlize(1.1232112) == '(<i>1.12</i>)'
# ----------------------------------------------CUSTOM TEST CASE END--------------------------------------------------#