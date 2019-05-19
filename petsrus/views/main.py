from petsrus.petsrus import app


@app.route("/")
def login():
    return "Login Page\n"
