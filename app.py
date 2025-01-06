from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    """
    Handles the root URL ("/") of the web application.

    Returns:
        str: An HTML string with a "Hello, World!" message.
    """
    return "<h1>Hello, World!</h1>"
