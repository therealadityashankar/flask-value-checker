@app.route("/abc")
@check_values_exist(
    "POST",
    """
    firstName : str/lenlim(1, 15)
    middleName : str/optional
    lastName : str/optional
    email : str
    password : str/lenlim(8, 15)
    phone : str/lenlim(8, 15)
    age : int/lim(18, 99)
    wannaPlay : bool
    """,
)
def abc():
    some_content


@app.route("/access_resource/details")
@check_values_exist(
    "POST",
    """
    resourceName : str/lenlim(0, 20)
    """,
)
def abc():
    some_content
