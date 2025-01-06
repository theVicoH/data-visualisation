from http import HTTPStatus
from flask import Blueprint, jsonify
from flasgger import swag_from

holidays_and_passengers_bp = Blueprint(
    'holidays_and_passengers_bp',
    __name__,
    url_prefix='/holidays_and_passengers'
)

@holidays_and_passengers_bp.route('/coucou', methods=['GET'])
@swag_from({
    "tags": ["Holidays & Passengers coucou"],
    "description": "Route coucou qui renvoi un message coucou holidays & passengers en JSON",
    "responses": {
        200: {
            "description": "Coucou holidays de bienvenue",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Coucou holidays & passengers !"
                    }
                }
            }
        }
    }
})
def holidays_and_passengers_coucou():
    """
    Fonction qui renvoi un message Coucou holidays & passengers ! en JSON
    """
    return jsonify({ 'message': 'Coucou holidays & passengers !' }), HTTPStatus.OK
