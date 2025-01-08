from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flasgger import swag_from
from src.services.passengers import PassengersService
from src.utils.date import DateUtils

passengers_bp = Blueprint('passengers_bp', __name__, url_prefix='/passengers')
passengers_service = PassengersService()
date_util = DateUtils()

@passengers_bp.get("/totals/total/country")
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

@passengers_bp.get("/totals/domestic/country")
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

@passengers_bp.get("/totals/international/country")
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

@passengers_bp.get("/totals/country/<iso3>")
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
                    },
                    "total": {
                        "type": "number",
                        "example": 2300000
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

@passengers_bp.get("/totals/world")
@swag_from({
    "tags": ["Passengers"],
    "description": "Retourne le volume total mondial de passagers",
    "responses": {
        200: {
            "description": "Totaux mondiaux",
            "schema": {
                "type": "object",
                "properties": {
                    "domestic_total": {"type": "number", "example": 800000000},
                    "international_total": {"type": "number", "example": 1500000000},
                    "total": {"type": "number", "example": 2300000000},
                    "countries": {"type": "integer", "example": 192}
                }
            }
        },
        500: {"description": "Erreur lors de la lecture du fichier"}
    }
})
def get_world_total():
    """
    Retourne les totaux de passagers mondiaux
    """
    try:
        result = passengers_service.get_world_totals()
        return jsonify(result), HTTPStatus.OK
    except ImportError as error:
        return jsonify({
            "error": "Erreur lors du traitement des données",
            "details": str(error)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@passengers_bp.get("/date/totals")
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

@passengers_bp.get("/date/range/totals")
@swag_from({
    "tags": ["Passengers"],
    "description": "Retourne les totaux de passagers sur une période donnée",
    "parameters": [
        {
            "name": "start_year",
            "in": "query",
            "type": "integer",
            "required": True,
            "description": "Année de début",
            "example": 2019
        },
        {
            "name": "start_month",
            "in": "query",
            "type": "integer",
            "required": True,
            "description": "Mois de début (1-12)",
            "example": 1
        },
        {
            "name": "end_year",
            "in": "query",
            "type": "integer",
            "required": True,
            "description": "Année de fin",
            "example": 2019
        },
        {
            "name": "end_month",
            "in": "query",
            "type": "integer",
            "required": True,
            "description": "Mois de fin (1-12)",
            "example": 12
        }
    ],
    "responses": {
        200: {
            "description": "Totaux des passagers pour la période",
            "schema": {
                "type": "object",
                "properties": {
                    "period": {
                        "type": "object",
                        "properties": {
                            "start": {
                                "type": "object",
                                "properties": {
                                    "year": {"type": "integer", "example": 2019},
                                    "month": {"type": "integer", "example": 1}
                                }
                            },
                            "end": {
                                "type": "object",
                                "properties": {
                                    "year": {"type": "integer", "example": 2019},
                                    "month": {"type": "integer", "example": 12}
                                }
                            }
                        }
                    },
                    "domestic_total": {"type": "number", "example": 800000000},
                    "international_total": {"type": "number", "example": 1500000000},
                    "total": {"type": "number", "example": 2300000000},
                    "countries": {"type": "integer", "example": 192}
                }
            }
        },
        400: {"description": "Paramètres invalides"},
        404: {"description": "Données non trouvées pour la période spécifiée"},
        500: {"description": "Erreur lors de la lecture du fichier"}
    }
})
def get_totals_by_date_range():
    """
    Retourne les totaux de passagers sur une période donnée
    """
    try:
        response = None
        status = HTTPStatus.OK

        params = {
            'start_year': date_util.validate_year(request.args.get('start_year')),
            'start_month': date_util.validate_month(request.args.get('start_month')),
            'end_year': date_util.validate_year(request.args.get('end_year')),
            'end_month': date_util.validate_month(request.args.get('end_month'))
        }

        for param_result in params.values():
            if param_result[1]:
                response = param_result[1][0]
                status = param_result[1][1]
                break

        if not response:
            start_year, start_month = params['start_year'][0], params['start_month'][0]
            end_year, end_month = params['end_year'][0], params['end_month'][0]

            if (start_year > end_year) or (start_year == end_year and start_month > end_month):
                response = {"error": "La date de début doit être antérieure à la date de fin"}
                status = HTTPStatus.BAD_REQUEST
            else:
                result = passengers_service.get_totals_by_date_range(
                    start_year, start_month, end_year, end_month
                )

                if result is None:
                    response = {"error": "Données non trouvées pour la période spécifiée"}
                    status = HTTPStatus.NOT_FOUND
                else:
                    response = result

    except ImportError as error:
        response = {
            "error": "Erreur lors du traitement des données",
            "details": str(error)
        }
        status = HTTPStatus.INTERNAL_SERVER_ERROR

    return jsonify(response), status

@passengers_bp.get("/country/<iso3>")
@swag_from({
    "tags": ["Passengers"],
    "description": "Retourne les données mensuelles pour un pays spécifique",
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
            "description": "Données mensuelles du pays",
            "schema": {
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "example": "FRA"
                    },
                    "monthly_data": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "year": {"type": "integer", "example": 2019},
                                "month": {"type": "integer", "example": 1},
                                "domestic": {"type": "number", "example": 800000},
                                "international": {"type": "number", "example": 1500000},
                                "total": {"type": "number", "example": 2300000}
                            }
                        }
                    }
                }
            }
        },
        400: {"description": "Code pays invalide"},
        500: {"description": "Erreur lors du traitement des données"}
    }
})
def get_country_monthly_data(iso3):
    """
    Retourne les données mensuelles pour un pays spécifique
    """
    try:
        monthly_data = passengers_service.get_monthly_data_by_country(iso3)

        if monthly_data is None:
            return jsonify({
                "error": "Code pays invalide"
            }), HTTPStatus.BAD_REQUEST

        return jsonify({
            "country": iso3.upper(),
            "monthly_data": monthly_data
        }), HTTPStatus.OK

    except ImportError as error:
        return jsonify({
            "error": "Erreur lors du traitement des données",
            "details": str(error)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@passengers_bp.get("/date/country")
@swag_from({
    "tags": ["Passengers"],
    "description": "Retourne les totaux par pays pour une date donnée",
    "parameters": [
        {
            "name": "year",
            "in": "query",
            "type": "integer",
            "required": True,
            "description": "Année",
            "example": 2019
        },
        {
            "name": "month",
            "in": "query",
            "type": "integer",
            "required": False,
            "description": "Mois (1-12)",
            "example": 6
        }
    ],
    "responses": {
        200: {
            "description": "Totaux par pays pour la période",
            "schema": {
                "type": "object",
                "properties": {
                    "year": {"type": "integer", "example": 2019},
                    "month": {"type": "integer", "example": 6},
                    "countries": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "country": {"type": "string", "example": "FRA"},
                                "domestic": {"type": "number", "example": 800000},
                                "international": {"type": "number", "example": 1500000},
                                "total": {"type": "number", "example": 2300000}
                            }
                        }
                    }
                }
            }
        },
        400: {"description": "Paramètres invalides"},
        404: {"description": "Données non trouvées"},
        500: {"description": "Erreur lors du traitement"}
    }
})
def get_totals_by_date_country():
    """
    Retourne les totaux par pays pour une date donnée
    """
    try:
        year, error = date_util.validate_year(request.args.get('year'))
        if error:
            return jsonify(error[0]), error[1]

        month, error = date_util.validate_month(request.args.get('month'))
        if error:
            return jsonify(error[0]), error[1]

        result = passengers_service.get_totals_by_date_country(year, month)
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

@passengers_bp.get('/date')
@swag_from({
    "tags": ["Passengers"],
    "description": "Route qui renvoi le nombre de passagers par années et mois en JSON",
    "responses": {
        200: {
            "description": "Nombre de passagers par années et mois",
            "schema": {
                "type": "object",
                "properties": {
                    "2010-01": {
                        "type": "number",
                        "example": 28902
                    },
                    "2010-07": {
                        "type": "number",
                        "example": 102
                    }
                }
            }
        },
        500: {"description": "Erreur lors du traitement des données"}
    }
})
def get_monthly_data_by_country():
    """
    Fonction qui renvoi un dictionnaire avec en clé
    le mois et l'année et en valeur le nombre de passangers
    """

    try:
        result = passengers_service.get_passengers_by_date()

        return jsonify(result), HTTPStatus.OK

    except ImportError as error:
        return jsonify({
            "error": "Erreur lors du traitement des données",
            "details": str(error)
        }), HTTPStatus.INTERNAL_SERVER_ERROR
