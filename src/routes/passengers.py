from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flasgger import swag_from
from src.services.passengers import PassengersService
from src.utils.date import DateUtils

passengers_bp = Blueprint('passengers_bp', __name__, url_prefix='/passengers')
passengers_service = PassengersService()
date_util = DateUtils()

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
        country_totals = passengers_service.get_totals_group_by_country('Total')
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
    try:
        domestic_totals = passengers_service.get_totals_group_by_country('Domestic')
        return jsonify({
            "domestic_totals": domestic_totals
        }), HTTPStatus.OK
    except ImportError as error:
        return jsonify({
            "error": "Erreur lors de la lecture du fichier",
            "details": str(error)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

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
    try:
        international_totals = passengers_service.get_totals_group_by_country('International')
        return jsonify({
            "international_totals": international_totals
        }), HTTPStatus.OK
    except ImportError as error:
        return jsonify({
            "error": "Erreur lors de la lecture du fichier",
            "details": str(error)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

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
    try:
        result = passengers_service.get_all_totals_by_country(iso3)

        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]

        return jsonify(result), HTTPStatus.OK

    except ImportError as error:
        return jsonify({
            "error": "Erreur lors du traitement des données",
            "details": str(error)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@passengers_bp.get("/date")
@swag_from({
    "tags": ["Passengers"],
    "description": 
      """
        Retourne le volume total de passagers domestiques
        et internationaux pour une année et optionnellement
        un mois spécifique
      """,
    "parameters": [
        {
            "name": "year",
            "in": "query",
            "type": "integer",
            "required": True,
            "description": "Année pour laquelle obtenir les statistiques",
            "example": 2019
        },
        {
            "name": "month",
            "in": "query",
            "type": "integer",
            "required": False,
            "description": "Mois pour lequel obtenir les statistiques (1-12)",
            "example": 6
        }
    ],
    "responses": {
        200: {
            "description": "Totaux des passagers pour la période",
            "schema": {
                "type": "object",
                "properties": {
                    "year": {
                        "type": "integer",
                        "example": 2019
                    },
                    "month": {
                        "type": "integer",
                        "example": 6,
                        "description": "Present uniquement si un mois est spécifié"
                    },
                    "domestic_total": {
                        "type": "number",
                        "example": 800000000
                    },
                    "international_total": {
                        "type": "number",
                        "example": 1500000000
                    },
                    "total": {
                        "type": "number",
                        "example": 2300000000
                    }
                }
            }
        },
        400: {"description": "Paramètres invalides"},
        404: {"description": "Données non trouvées pour la période spécifiée"},
        500: {"description": "Erreur lors de la lecture du fichier"}
    }
})
def get_totals_by_date():
    """
    Retourne les totaux de passagers domestiques et internationaux pour une année
    """
    try:
        year, error = date_util.validate_year(request.args.get('year'))
        if error:
            return jsonify(error[0]), error[1]

        month, error = date_util.validate_month(request.args.get('month'))
        if error:
            return jsonify(error[0]), error[1]

        result = passengers_service.get_totals_by_date(year, month)
        if result is None:
            return jsonify({
                "error": "Données non trouvées pour la période spécifiée"
            }), HTTPStatus.NOT_FOUND

        return jsonify(result), HTTPStatus.OK

    except ImportError as error:
        return jsonify({
            "error": "Erreur lors du traitement des données",
            "details": str(error)
        }), HTTPStatus.INTERNAL_SERVER_ERROR
