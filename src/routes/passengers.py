from http import HTTPStatus
from flask import Blueprint, jsonify
from flasgger import swag_from

passengers_bp = Blueprint('passengers_bp', __name__, url_prefix='/passengers')

@passengers_bp.route('/coucou', methods=['GET'])
@swag_from({
    "tags": ["Passengers coucou"],
    "description": "Route coucou qui renvoi un message coucou passengers en JSON",
    "responses": {
        200: {
            "description": "Coucou passengers de bienvenue",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Coucou passengers !"
                    }
                }
            }
        }
    }
})
def passengers_coucou():
    """
    Fonction qui renvoi un message Coucou passengers ! en JSON
    """
    return jsonify({ "message": "Coucou passengers !" }), HTTPStatus.OK
