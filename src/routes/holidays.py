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
    "tags": ["Holidays"],
    "description": "Route qui renvoi le nombre de jours fériés par pays en JSON",
    "parameters": [
        {
            "name": "holiday-type",
            "in": "query",
            "type": "string",
            "required": False,
            "description": 
                "Type de jour férié à filtrer. Types valides : "
                "Public holiday, Observance, Local holiday, Local observance, Special holiday.",
            "example": "Public holiday"
        }
    ],
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

@holidays_bp.get("/holidays-by-country/<iso3>")
@swag_from({
    "tags": ["Holidays"],
    "description": 
        "Retourne le nombre de jours fériés pour un pays spécifique. "
        "Vous pouvez également filtrer les jours fériés par type "
        "(ex. : Public holiday, Observance, etc.).",
    "parameters": [
        {
            "name": "iso3",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "Code ISO3 du pays",
            "example": "FRA"
        },
        {
            "name": "holiday-type",
            "in": "query",
            "type": "string",
            "required": False,
            "description": 
                "Type de jour férié à filtrer. Types valides : "
                "Public holiday, Observance, Local holiday, Local observance, Special holiday.",
            "example": "Public holiday"
        }
    ],
    "responses": {
        200: {
            "description": "Nombre de jours fériés pour le pays (avec ou sans filtre).",
            "schema": {
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "example": "FRA"
                    },
                    "data": {
                        "type": "number",
                        "example": 190
                    }
                }
            }
        },
        400: {
            "description": "Erreur liée à la requête, comme un code ISO3 "
            "ou un type de jour férié non valide.",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "iso3 non valide"
                    }
                }
            }
        },
        500: {
            "description": "Erreur serveur lors de la lecture du fichier ou d'autres problèmes.",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Erreur lors de la lecture du fichier"
                    }
                }
            }
        }
    }
})
def get_holiday_for_one_country(iso3):
    """
    Retourne le nombre de jours fériés pour un pays spécifique
    """
    return holidays_service.get_holidays_for_one_country(iso3)

@holidays_bp.get('/min-max')
@swag_from({
    "tags": ["Holidays"],
    "description": "Route qui renvoi le pays avec le moins de jours fériés et "
    "le pays avec le plus de jours fériés en JSON",
    "parameters": [
        {
            "name": "holiday-type",
            "in": "query",
            "type": "string",
            "required": False,
            "description": 
                "Type de jour férié à filtrer. Types valides : "
                "Public holiday, Observance, Local holiday, Local observance, Special holiday.",
            "example": "Public holiday"
        }
    ],
    "responses": {
        200: {
            "description": "Pays avec les jours fériés minimum et maximum",
            "schema": {
                "type": "object",
                "properties": {
                    "max": {
                        "type": "object",
                        "properties": {
                            "country": {
                                "type": "string",
                                "example": "Us"
                            },
                            "data": {
                                "type": "number",
                                "example": 1079
                            }
                        }
                    },
                    "min": {
                        "type": "object",
                        "properties": {
                            "country": {
                                "type": "string",
                                "example": "Mayotte"
                            },
                            "data": {
                                "type": "number",
                                "example": 40
                            }
                        }
                    }
                }
            }
        },
        400: {
            "description": "Erreur liée à la requête, comme un "
            "un type de jour férié non valide.",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "holiday-type non valide"
                    }
                }
            }
        },
        500: {"description": "Erreur lors de la lecture du fichier"}
    }
})
def get_holiday_min_max():
    """
    Fonction qui renvoi le pays avec le moins de jours fériés et
    le pays avec le plus de jours fériés
    """
    return holidays_service.get_min_max_holidays()
