from http import HTTPStatus
from flask import Blueprint, jsonify
from flasgger import swag_from
from src.services.passengers import PassengersService

passengers_bp = Blueprint('passengers_bp', __name__, url_prefix='/passengers')
service = PassengersService()


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


@passengers_bp.get("/total-by-country")
@swag_from({
    "tags": ["Passengers"],
    "description": "Retourne le volume total de passagers par pays",
    "responses": {
        200: {
            "description": "Volume total de passagers par pays",
            "schema": {
                "type": "object",
                "properties": {
                    "country_totals": {
                        "type": "object",
                        "additionalProperties": {"type": "number"},
                        "example": {"FRA": 1000000, "USA": 2000000}
                    }
                }
            }
        },
        500: {"description": "Erreur lors de la lecture du fichier"}
    }
})
def get_total_passengers_by_country():
    """
    Fonction qui renvoi le total de passagers de tous les pays en JSON
    """
    return service.get_total_by_country()
