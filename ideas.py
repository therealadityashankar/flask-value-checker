#!/usr/bin/env python3
"""
developmental future ideas, for fun
"""
from flask_value_checker import Invigilator
from flask import Flask, request, Response, g

import json

app = Flask(__name__)


def custom_error_shower(errors):
    return Response(
        json.dumps({"errors": errors,}), status=400, mimetype="application/json"
    )


invigilator = Invigilator(custom_error_shower)


@app.route("/", methods=["POST"])
@invigilator.check(
    "POST",
    """
    firstName : str/lenlim(1, 15)
    middleName : str/optional
    lastName : str/optional
    email : str/optional
    password : str/lenlim(8, 15)/optional
    phone : str/lenlim(8, 15)/optional
    age : int/lim(18, 99)/optional
    preferedState : str/optional/accept(['TamilNadu', 'Kerela'])
    stayLoggedIn : str/accept(['on'])/optional
    """,
)
def abc():
    print(g.value_checker)
    form = request.form
    stay_logged_in = form.get("stayLoggedIn", "off")
    return f'hi! {form["firstName"]}, stay logged in : {stay_logged_in}'


if __name__ == "__main__":
    app.run(debug=True)
