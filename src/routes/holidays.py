from http import HTTPStatus
from flask import Blueprint, jsonify
from flasgger import swag_from

holidays_bp = Blueprint('holidays_bp', __name__, url_prefix='/holidays')

@holidays_bp.route('/coucou', methods=['GET'])
@swag_from({
    "tags": ["Holidays coucou"],
    "description": "Route coucou qui renvoi un message coucou holidays en JSON",
    "responses": {
        200: {
            "description": "Coucou holidays de bienvenue",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Coucou holidays !"
                    }
                }
            }
        }
    }
})
def holidays_coucou():
    """
    Fonction qui renvoi un message Coucou holidays ! en JSON
    """
    return jsonify({ 'message': 'Coucou holidays !' }), HTTPStatus.OK
