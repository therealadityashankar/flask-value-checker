# Flask-value-checker

## Example usage
```python
@app.route('/abc')
@check_values_exist(
   'POST', '''
    firstName : str/lenlim(1, 15)
    middleName : str/optional
    lastName : str/optional
    email : str
    password : str/lenlim(8, 15)
    phone : str/lenlim(8, 15)
    age : int/lim(18, 99)
    wannaPlay : bool
    '''
)
def abc():
    some_content
```

## format of the decorator
argument 1 : decorator method,
argument 2 : parameters required,
             checks form in case of "POST" or "PUT" request,
             querystring otherwise for "GET"

### Rules:
- different parameters are separated by a newline
- the parameter and its rules are separated by an `:`
- rule conditions are separated by an `/`
- the first condition should be the type of the required value, `str` or `int`

## Dev-docs
- codestyle : Numpydoc
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
