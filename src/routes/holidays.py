from http import HTTPStatus
from flask import Blueprint, jsonify
from flasgger import swag_from
from src.services.holidays import HolidaysService

holidays_bp = Blueprint('holidays_bp', __name__, url_prefix='/holidays')
holidays_service = HolidaysService()

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

@holidays_bp.get('/holidays-by-country')
@swag_from({
    "tags": ["Holidays by country"],
    "description": "Route coucou qui renvoi le nombre de jours fériés par pays en JSON",
    "responses": {
        200: {
            "description": "Nombre de jours fériés par pays",
            "schema": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "additionalProperties": {"type": "number"},
                        "example": {"France": 190, "Estonia": 120}
                    }
                }
            }
        },
        500: {"description": "Erreur lors de la lecture du fichier"}
    }
})
def get_holidays_by_country():
    """
    Fonction qui renvoi le nombre de jours fériés par pays en JSON
    """
    return holidays_service.get_holidays_by_country()
