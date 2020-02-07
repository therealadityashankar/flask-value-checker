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

### Writing parameters:

- different parameters are separated by a newline
- the parameter and its rules are separated by an `:`
- rule conditions are separated by an `/`
- the first condition should be the type of the required value, `str`, `int` or `float`
- condition arguments are put in brackets `()`

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
