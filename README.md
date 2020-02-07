# Flask-value-checker :mag_right:
Imaging web form checking, but now imagine that it was easy and comfy

## Installation
Install simply using pip:

```
pip install flask-value-checker
```


## Example usage
```python
from flask_value_checker import Invigilator
from flask import Flask, request

app = Flask(__name__)
invigilator = Invigilator()

@app.route('/abc', methods=['POST'])
@invigilator.check(
   'POST',
   '''
   username : str/lenlim(5, 15)
   password : str/lenlim(8, inf)
   stayLoggedIn : str/accept(['on'])/optional
   '''
)
def abc():
    stay_logged_in = request.form.get('stayLoggedIn', 'off')
    return f'hi {request.form['username']}, stay logged in: {stay_logged_in}'

app.run()
```

#### example default error
Note: this error can [be customized](#custom-error-showing)

```javascript
{
    "error": {
        "code": "MALFORMED_OR_MISSING_PARAMETERS",
        "message": "one or more fields we're either missing or malformed",
        "fields": {
            "email" : "missing parameter, parameter is required",
            "firstName" : "string length must be between 5 and inf",
            "age" : "parameter has to be of type 'int'"
            ...
        }
    }
}
```
---
## Navigation
- [Function docs](#function-docs)
- [Field name attribute docs](#field-name-attribute-docs)
- [Guide](#guide)

---
<a name="function-docs"></a>
## Function docs :notebook_with_decorative_cover: :notebook: :closed_book: :blue_book:
<a name="custom-error-showing"></a>
### Invigilator(err_function=None)
- **Type** : `function` or `None`
- **Description** : the function that displays the final error to the webpage, must be written the the way a standard flask function is written, (although you may wanna check out [Flask.Response](https://flask.palletsprojects.com/en/1.1.x/api/?highlight=response#flask.Response), and return that instead of a tuple like `(error, 400)`)
- **Example**
```python
def custom_error_shower(errors):
    return Response(
        json.dumps({"errors": errors,}), status=400, mimetype="application/json"
    )
```

### Invigilator.check(http_methods, checker_str)
#### http_methods:
- **Type** : `str` or `list of strs`
- **Description** : HTTP methods to check for,

 **NOTE**: if the http method to check for is not present in methods, the decorated function will be called normally and no checks will be performed
- **Example** : `'GET'`, `'POST'`, `['GET', 'POST']`

#### checker_str
- **Type** : `str`
- **Description** : the form attributes and their restrictions written in the prescribed format, [See Here](#writing-parameters)

---
<a name="field-name-attribute-docs"></a>
## Field name attribute docs :notebook_with_decorative_cover: :notebook: :closed_book: :blue_book:
all top attributes (str, int, float) should not have any parameters,

**Note**: top attributes should be placed first, then its sub attributes
should be placed
### str
#### lenlim(min, max)
the minimum and maximum length the fields string can be
- **min** : `int` or the value `inf`, the minimum accepted string length
- **max** : `int` or the value `inf` (see [example-usage](#example-usage)), the maximum accepted string length

#### optional
is the attribute optional ?

#### accept(accepted_vals)
values that can be accepted when using the field name
- **accepted_vals**: `list of strings`, the acceptable values for the parameter

### int and float
**int** specifies that the number must be an integer,

**float** specifies that it can be decimal,

both attributes have the same sub-attributes
#### lim(min, max)
the limits that the numeric values can range between
- **min** : `float` or the value `inf`, the minimum accepted numeric value
- **max** : `float` or the value `inf` (see [bigger-full-example](#bigger-full-example)), the maximum accepted numeric value

#### optional
is the attribute optional ?

---
<a name="guide"></a>
## Guide :metal:

ok, so you wanna write parameters, but in a fun way, cool, you've come to the right place !

**Note**:
  - ensure <u>**[flask-value-checker](#install)**</u> and <u>**requests**</u> have been install via `pip install <library>`
  before starting with the tutorial

### Hello invigilated world

lets start off with a really simple example

- create a file `hello_invigilation.py` in a suitable directory
- add the below contents to the file, then save the file

```python
from flask_value_checker import Invigilator
from flask import Flask, request

app = Flask(__name__)
invigilator = Invigilator()

@app.route('/abc', methods=['POST'])
@invigilator.check(
   'POST',
   '''
   name : str
   '''
)
def abc():
    return f"hi {request.form['name']}"

app.run(port=5000, debug=True)
```
the code in the `invigilator.check` decorator here ensures that there is a name present


- if you're running **linux**, run the file via writing `python3 hello_invigilation.py` in a terminal instance
- if you're running **windows**, run the file via double clicking the icon
- let this file run in the background
- now create another file `check_invigilation.py`, in the same directory
- add the following contents to the file

```python
import requests

site = "http://localhost:5000/abc"
vals = {'name':'bob'}

val = requests.post(site,data=vals)
print(val.text)
```

- now save the file, and run the file similarly as before
- you should see the following output

```
hi bob
```

- now open `check_invigilation.py` again, and change the contents to the following

```python
import requests

site = "http://localhost:5000/abc"
vals = {}

val = requests.post(site,data=vals)
print(val.text)
```
- save the contents and run the file again, you should see the following message

```js
{"error": {"code": "MALFORMED_OR_MISSING_PARAMETERS", "message": "one or more fields we're either missing or malformed", "fields": {"name": "value is required"}}}
```

I'm gonna rewrite this json below better for more clarity
```js
{
  "error": {
    "code": "MALFORMED_OR_MISSING_PARAMETERS",
    "message": "one or more fields we're either missing or malformed",
    "fields": {"name": "value is required"}
  }
}
```

cool, we did it !, we've put restrictions on our first parameter !

we've ensured that any user using the code will have to put their name here !

now lets add an additional restrictions to the parameter,

it'll be difficult to represent a name if its too long, so lets restrict the name to between 5 and 18 characters

- open `hello_invigilation.py` and rewrite the file to the following content

```python
from flask_value_checker import Invigilator
from flask import Flask, request

app = Flask(__name__)
invigilator = Invigilator()

@app.route('/abc', methods=['POST'])
@invigilator.check(
   'POST',
   '''
   name : str/lenlim(5, 18)
   '''
)
def abc():
    return f"hi {request.form['name']}"

app.run(port=5000, debug=True)
```
- notice the changed text after `name : str`, we've added `lenlim(5, 18)` here, this ensures that the length of the string is between 5 and 18 characters, the `/` simply divides the attributes
- save the file, and the running process should automatically update its contents (thanks to how app.run(debug=True) in flask works)
- now lets rewrite `check_invigilation.py` to its original contents

```python
import requests

site = "http://localhost:5000/abc"
vals = {'name':'bob'}

val = requests.post(site,data=vals)
print(val.text)
```

- now lets run `check_invigilation.py`, you should see the message

```javascript
{"error": {"code": "MALFORMED_OR_MISSING_PARAMETERS", "message": "one or more fields we're either missing or malformed", "fields": {"name": "string length must be between 5 and 18"}}}
```

prettyfied, this is

```javascript
{
  "error": {
    "code": "MALFORMED_OR_MISSING_PARAMETERS",
    "message": "one or more fields we're either missing or malformed",
    "fields": {
      "name": "string length must be between 5 and 18"
    }
  }
}
```

this is telling us the name we've written is too short !, lets rewrite `check_invigilation.py` to fix this !

- here are the new contents of `check_invigilation.py`

```python
import requests

site = "http://localhost:5000/abc"
vals = {'name':'bobmus'}

val = requests.post(site,data=vals)
print(val.text)
```
- run the file and you should see

`hi bobmus`

COOL :smiley:

our condition here ensures that the name has to be between 5 and 18 characters

here are some additional `invigilator.check` examples you can try out for yourself

- this forces a name that is greater than 3 characters and an age that is an integer
```
'''
name : str/lenlim(3, inf)
age : int
'''
```

- this is the same as above, but forces the age to be between 18 and 99
```
'''
name : str/lenlim(3, inf)
age : int/lim(18, 99)
'''
```

- this, along side the above, adds an additional, optional, email option
```
'''
name : str/lenlim(3, inf)
age : int/lim(18, 99)
email : str/optional
'''
```

- this, adds a team option, that only supports the keywords "blue", "green", or "orange", hence letting the user choose an appropriate team, it'll raise an error if a value outside these values is used
```
'''
name : str/lenlim(3, inf)
age : int/lim(18, 99)
email : str/optional
team : str/accept(['blue', 'green', 'red'])
'''
```

- lastly, this adds an additional 'sendNewsletter' optional value, that only accepts the value "on", and is optional, (in complaince with how form checkboxes work)
```
'''
name : str/lenlim(3, inf)
age : int/lim(18, 99)
email : str/optional
team : str/accept(['blue', 'green', 'red'])
sendNewsletter : str/accept(['on'])/optional
'''
```

#### basic guide to writing restrictions:

- different restrictions are separated by a newline
- the restriction and its rules are separated by an `:`
- rule conditions (attributes) are separated by an `/`
- the first condition should be the type of the required value, `str`, `int` or `float`
- attribute parameters are put in brackets `()`

###### example:
`score : float/lim(0, 11.5)/optional`

### bigger full example
```python
@app.route('/abc')
@invigilator.check(
   'POST',
   '''
    firstName : str/lenlim(1, 15)
    middleName : str/optional
    lastName : str/optional
    stayLoggedIn : str/accept(['on'])/optional
    team : str/accept(['blue', 'green', 'yellow'])
    email : str
    password : str/lenlim(8, inf)
    phone : str/lenlim(8, 15)
    # number will have to be an Int,
    # but it'll have to be greater than
    # 18, not including 18
    age : int/lim(18.9, inf)
    score : float/lim(0, 10) # can be a decimal value
    '''
)
def abc():
    some_content
```

## Dev-docs
- codestyle : black
- documentation style : numpydoc
- HTTP-Returns extra to Numpydoc, that is similar to Return, but is represented as follows

```python
'''
HTTP-Returns
------------
400
    on failure, the response will be similar to,

    {
        "error": {
            "code": "MALFORMED_OR_MISSING_PARAMETERS",
            "message": "one or more fields we're either missing or malformed",
            "fields": {
                "email" : "missing parameter, parameter is required",
                "firstName" : "name has to be under 15 characters",
                "age" : "parameter has to be of type 'int'"
                ...
            }
        }
    }

*
    or whatever the original function returns

    *
'''
```

i.e.

```
<return code>
    <details>
    <return message>
```
