## Assingment Decorators

> A **decorator** in **Python** is any callable **Python** object that is used to modify a function or a class. This assignment is about implementing various simple decorators to accomplish tiny features in our functions.

### Allows a function to run only on odd seconds

> A simple decorator to make the function return the output only if the current time has seconds numeric as an odd digit.

```python
def odd_sec(fn) -> "Function":
    """
    This is a closure function
        # Param:
            fn : This function takes in function as a parameter
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        """
            This function checks if the seconds is odd, then it will run the function
            else will return a message
        """
        CURR_TIME = datetime.now()
        print(CURR_TIME)
        if CURR_TIME.second % 2 != 0:
            return fn(*args, **kwargs)
    return inner
```

### Debugger :

> A decorator to print the logs of a function, the start time of execution, end time, running time. Also, whether the function returns something, it's docs. The decorator adds these functionality for us.

```python
def debugger(func) -> "Function":
    """
    This is a decorator which adds logging to an exisitng function
    """
    @wraps(func)
    def inner(*args, **kwargs):
        run_dt = datetime.now(timezone.utc)
        start_time = perf_counter()
        output = fn(*args, **kwargs)
        end_time = perf_counter()

        print(f'{run_dt}: called {fn.__name__} function')
        print(f'{fn.__name__} description: {fn.__doc__}')
        print(f'{fn.__name__} took {end_time -start_time} seconds to complete')
        return output
    return inner
```

### Authenticate

> Decorator to implement simple authentication functionality and give that to any function of our choice. The user can make use of a closure to provide the current password. It has to match with the default user password provided beforehand.

```python
def set_sign_on() -> "Function":
    """
    This is a decorator which adds authentication using a stored password
    """
    auth = ''
    def inner():
        nonlocal auth
        if auth == '':
            auth = get_password()
        return auth
    return inner


def try_certificate_auth(current_pass: str, user_pass: str):
    """
    Wrapper used to authenticate the function before executing the function.
    current_pass: `set_password` closure to get password from user.
    :param user_pass: pre-defined password compared with the `curr_password`.
    """ 

    def decor(fn: "Function"):
        @wraps(fn)
        def inner(*args, **kwargs):
            if user_pass == current_pass():
                print("You are authenticated")
                return fn(*args, **kwargs)
            else:
                print("Wrong Password!!!")

        return inner

    return decor
```

### Average time

> A decorator factory, that takes in an integer, defining the number of iteration of which a function's runtime has to be calculated and average is calculated. It returns a decorator.

```python
def dec_timeavg(reps:int):
    '''
    This is a function takes integer as an input and runs the functions of reps number of time.
    '''
    def dec(fn):
        '''
        This is a decorator which can run a function n times
        and returns the avg run time ( n times )
        '''
        @wraps(fn)
        def inner(*args, **kwargs):
            total_elapsed = 0

            for i in range(reps):
                start = perf_counter()
                result = fn(*args, **kwargs)
                end = perf_counter()
                total_elapsed += (end - start)
            avg_run_time = total_elapsed / reps

            print('Avg Run time: {0:.6f}s ({1} reps)'.format(avg_run_time, reps))
            
            return result
        return inner
    return avgtime

```

### Privilege

> Decorator that provides privilege access. A function can have four parameters and based on the privileges (high, mid, low, no), access is given to all 4, 3, 2 or 1 parameters.

```python
class Firewall:
    """
    This decorator class  wraps any function with certain privileges which
    limits the arguments passed to the function. Based on privileges (high, mid, low, no),
    it provides access to all 4, 3, 2 or 1 parameters.
    """

    def __init__(self, privilege="no"):
        if privilege and privilege in ("high", "mid", "low", "no"):
            self.privilege = privilege
        else:
            self.privilege = "no"

    def __call__(self, fn):

        @wraps(fn)
        def inner(base, **kwargs):
            params = list(kwargs.items())
            cnt = {"high": 3, "mid": 2, "low": 1, "no":0}
            if len(params) < cnt[self.privilege] :
                raise ValueError("Invalid number of keyword arguments!")

            if self.privilege == "high":
                return fn(base, **dict(params[:3]))

            elif self.privilege == "mid":
                return fn(base, **dict(params[:2]))

            elif self.privilege == "low":
                return fn(base, **dict(params[:1]))

            elif self.privilege == "no":
                return fn(base)
        return inner
```

### Single dispatch

> Writing HTMLize code using `singledispatch`, available as a built-in decorator in `functools` module. Also the idea is to add functionality using monkey patching and not make every thing hard coded.

```python
@singledispatch
def htmlize(arg):
    if isinstance(arg, int):
        '''
        function to htmlize the input based on the type of input.
        this is a default initializer.
        '''
        return html_int(arg)

    elif isinstance(arg, float) or isinstance(arg, Decimal):
        """
        Convert real number to Decimal function
        """
        return html_real(arg)

    elif isinstance(arg, str):
        return html_str(arg)

    elif isinstance(arg, list) or isinstance(arg, tuple):
        return html_list(arg)

    elif isinstance(arg, dict):
        return html_dict(arg)

    elif isinstance(arg, set):
        return html_set(arg)

    else:
        return html_escape(arg)
```

```
def html_escape(arg):
    return escape(str(arg))

def html_int(a):
    return f'{a}(<i>{str(hex(a))}</i>)'

def html_real(a):
    return f'{round(a, 2)}'

def html_str(s):
    return html_escape(s).replace('\n', '<br/>\n')

def html_list(l):
    items = (f'<li>{html_escape(item)}</li>' for item in l)
    return '<ul>\n' + '\n'.join(items) + '\n</ul>'

def html_dict(d):
    items = (f'<li>{k}={v}</li>' for k, v in d.items())
    return '<ul>\n' + '\n'.join(items) + '\n</ul>'

def html_set(arg):
    return html_list(arg)
```
After this, functions to handle other types are added one by one, available in the code.

## Test Case Performance

![](result.png)