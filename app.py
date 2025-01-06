from flask import Flask, jsonify
from flasgger import Swagger, swag_from
from http import HTTPStatus

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/")
@swag_from({
    "tags": ["Hello World"],
    "description": "Route racine qui renvoie un message Hello World en JSON",
    "responses": {
        200: {
            "description": "Message de bienvenue",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Hello, World!"
                    }
                }
            }
        }
    }
})
def hello_world():
    """
    Handles the root URL ("/") of the web application.

    Returns:
        json: A JSON object containing a welcome message and status code
    """
    return jsonify({
        "message": "Hello, World!"
    }), HTTPStatus.OK

if __name__ == "__main__":
    app.run(debug=True)