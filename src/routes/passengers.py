from http import HTTPStatus
from flask import Blueprint, jsonify
from flasgger import swag_from
from src.services.passengers import PassengersService

passengers_bp = Blueprint('passengers_bp', __name__, url_prefix='/passengers')
service = PassengersService()

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
def get_total_number_of_passengers_by_country():
    """
    Fonction qui renvoi le total de passagers de tous les pays en JSON
    """
    try:
        country_totals = service.get_total_by_country()
        return jsonify({
            "country_totals": country_totals
        }), HTTPStatus.OK
    except ImportError as error:
        return jsonify({
            "error": "Erreur lors de la lecture du fichier",
            "details": str(error)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@passengers_bp.get("/domestic-total")
@swag_from({
    "tags": ["Passengers"],
    "description": "Retourne le volume total de passagers domestiques par pays",
    "responses": {
        200: {
            "description": "Volume total de passagers domestiques par pays",
            "schema": {
                "type": "object",
                "properties": {
                    "domestic_totals": {
                        "type": "object",
                        "additionalProperties": {"type": "number"},
                        "example": {"FRA": 800000, "USA": 1500000}
                    }
                }
            }
        },
        500: {"description": "Erreur lors de la lecture du fichier"}
    }
})
def get_total_number_of_domestic_passengers_by_country():
    """
    Fonction qui renvoi le total de passagers domestiques par pays en JSON
    """
    return service.get_domestic_total()

@passengers_bp.get("/international-total")
@swag_from({
    "tags": ["Passengers"],
    "description": "Retourne le volume total de passagers internationaux par pays",
    "responses": {
        200: {
            "description": "Volume total de passagers internationaux par pays",
            "schema": {
                "type": "object",
                "properties": {
                    "international_totals": {
                        "type": "object",
                        "additionalProperties": {"type": "number"},
                        "example": {"FRA": 800000, "USA": 1500000}
                    }
                }
            }
        },
        500: {"description": "Erreur lors de la lecture du fichier"}
    }
})
def get_total_number_of_international_passengers_by_country():
    """
    Fonction qui renvoi le total de passagers internationaux par pays en JSON
    """
    return service.get_international_total()

@passengers_bp.get("/country/<iso3>")
@swag_from({
    "tags": ["Passengers"],
    "description": 
      "Retourne le total de passagers domestiques et internationaux pour un pays spécifique",
    "parameters": [
        {
            "name": "iso3",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "Code ISO3 du pays",
            "example": "FRA"
        }
    ],
    "responses": {
        200: {
            "description": "Totaux des passagers pour le pays",
            "schema": {
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "example": "FRA"
                    },
                    "domestic_total": {
                        "type": "number",
                        "example": 800000
                    },
                    "international_total": {
                        "type": "number",
                        "example": 1500000
                    }
                }
            }
        },
        400: {"description": "Entrez un iso3 valide"},
        500: {"description": "Erreur lors de la lecture du fichier"}
    }
})
def get_all_totals_passenger_by_country(iso3):
    """
    Retourne les totaux de passagers pour un pays spécifique
    """
    return service.get_totals_by_country(iso3)
