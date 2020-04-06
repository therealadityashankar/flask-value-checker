from flask import Flask, request
from helper import Invigilator
import io

app = Flask(__name__)
app.config["TESTING"] = True

invigilator = Invigilator()


@app.route("/popo", methods=["POST"])
@invigilator.check(
    ["POST"],
    """
    name : str/lenlim(0, 5)
    place : str/lenlim(0, 10)
    animal : str/lenlim(0, 15)
    thing : str/lenlim(0, 20)
    fav_number : int/lim(-10, 10)/optional
    fav_decimal : float/lim(-1, 1)/optional
    needed_file : file
    optional_file : file/optional
    """,
)
def popo():
    form = request.form
    file_text = request.files["needed_file"].read().decode()
    all_text = (
        f"hi {form['name']} of {form['place']}, who likes {form['animal']}s and {form['thing']}s "
        + f"needed_file contains {file_text}"
    )

    if request.files.get("optional_file"):
        optional_file_text = request.files["optional_file"].read().decode()
        all_text += f" optional file text {optional_file_text}"
    return all_text


def test_simple_flask():
    with app.test_client() as client:
        rv = client.post(
            "/popo",
            content_type="multipart/form-data",
            data={
                "name": "popo",
                "place": "some place",
                "animal": "panda",
                "thing": "block",
                "needed_file": (io.BytesIO(b"something"), "sample.txt"),
            },
        )

        assert rv.status_code == 200, rv.data
        assert rv.data == (
            b"hi popo of some place, who likes pandas and blocks "
            + b"needed_file contains something"
        )


def test_file_needed():
    err_txt = "file 'needed_file' is missing !"
    tests = [
        [b"asfasfasf", None],
        [b"fn392imewoi", None],
        [b"12F#@@!DC#$&", None],
        [None, err_txt],
        [b"", err_txt],  # edge case
    ]
    for test, exp_output in tests:
        data = {
            "name": "popo",
            "place": "some place",
            "animal": "panda",
            "thing": "block",
        }

        if test:
            data["needed_file"] = (io.BytesIO(test), "file.txt")

        with app.test_client() as client:
            rv = client.post("/popo", content_type="multipart/form-data", data=data,)

            if exp_output is None:
                assert rv.status_code == 200, (rv.data, f"test: {test}")
                assert rv.data == (
                    b"hi popo of some place, who likes pandas and blocks "
                    + "needed_file contains {0}".format(test.decode()).encode()
                )
            else:
                assert rv.status_code == 400, (rv.status_code, rv.data)
                assert rv.json["error"]["fields"]["needed_file"] == exp_output


def test_file_optional():
    err_txt = ""
    tests = [
        [b"asfasfasf", None],
        [b"fn392imewoi", None],
        [b"12F#@@!DC#$&", None],
        [None, None],
        [b"", None],  # edge case
    ]
    for test, exp_output in tests:
        data = {
            "name": "popo",
            "place": "some place",
            "animal": "panda",
            "thing": "block",
            "needed_file": (io.BytesIO(b"something"), "file.txt"),
        }

        if test:
            data["optional_file"] = (io.BytesIO(test), "file.txt")

        with app.test_client() as client:
            rv = client.post("/popo", content_type="multipart/form-data", data=data,)
            all_data = (
                b"hi popo of some place, who likes pandas and blocks "
                + b"needed_file contains something"
            )

            if test:
                all_data += " optional file text {0}".format(test.decode()).encode()

            assert rv.status_code == 200, (rv.data, f"test: {test}")
            assert rv.data == all_data
