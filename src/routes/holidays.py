from http import HTTPStatus
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from src.services.holidays import HolidaysService, HOLIDAY_TYPES

holidays_bp = Blueprint('holidays_bp', __name__, url_prefix='/holidays')
holidays_service = HolidaysService()

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
        500: {"description": "Erreur lors du traitement des données de globals_holidays.csv "}
    }
})
def get_holidays_by_country():
    """
    Fonction qui renvoi le nombre de jours fériés par pays
    """

    try:
        holiday_type = request.args.get('holiday-type', None)

        if holiday_type and holiday_type not in HOLIDAY_TYPES:
            return jsonify(
                {
                    "error": "holiday-type non valide"
                }
            ), HTTPStatus.BAD_REQUEST

        result = holidays_service.get_holidays_by_country(holiday_type=holiday_type)

        return jsonify(result), HTTPStatus.OK

    except ImportError as error:
        return jsonify({
            "error": "Erreur lors du traitement des données de globals_holidays.csv ",
            "details": str(error)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

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
                        "example": "Erreur lors du traitement des données de globals_holidays.csv "
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
    try:
        holiday_type = request.args.get('holiday-type', None)

        if holiday_type and holiday_type not in HOLIDAY_TYPES:
            return jsonify(
                {
                    "error": "holiday-type non valide"
                }
            ), HTTPStatus.BAD_REQUEST

        result = holidays_service.get_holidays_for_one_country(
            iso3=iso3,
            holiday_type=holiday_type
        )

        if not result:
            return jsonify({
                "error": "iso3 non valide"
            }), HTTPStatus.BAD_REQUEST

        return jsonify(result), HTTPStatus.OK

    except ImportError as error:
        return jsonify({
            "error": "Erreur lors du traitement des données de globals_holidays.csv ",
            "details": str(error)
        }), HTTPStatus.INTERNAL_SERVER_ERROR


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
        500: {"description": "Erreur lors du traitement des données de globals_holidays.csv"}
    }
})
def get_holiday_min_max():
    """
    Fonction qui renvoi le pays avec le moins de jours fériés et
    le pays avec le plus de jours fériés
    """
    try:
        holiday_type = request.args.get('holiday-type', None)

        if holiday_type and holiday_type not in HOLIDAY_TYPES:
            return jsonify(
                {
                    "error": "holiday-type non valide"
                }
            ), HTTPStatus.BAD_REQUEST

        result = holidays_service.get_min_max_holidays(holiday_type=holiday_type)

        return jsonify(result), HTTPStatus.OK

    except ImportError as error:
        return jsonify({
            "error": "Erreur lors du traitement des données de globals_holidays.csv ",
            "details": str(error)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@holidays_bp.get('/repartition-by-type')
@swag_from({
    "tags": ["Holidays"],
    "description": "Route qui renvoi le nombre des jours "
    "fériés par type",
    "parameters": [
        {
            "name": "country",
            "in": "query",
            "type": "string",
            "required": False,
            "description": "Pays",
            "example": "Serbia"
        }
    ],
    "responses": {
        200: {
            "description": "Nombre de jours fériés par type",
            "schema": {
                "type": "object",
                "properties": {
                    "Local holiday": {
                        "type": "number",
                        "example": 2307
                    },
                    "Local observance": {
                        "type": "number",
                        "example": 358
                    },
                    "Observance": {
                        "type": "number",
                        "example": 10490
                    },
                    "Public holiday": {
                        "type": "number",
                        "example": 30669
                    },
                    "Special holiday": {
                        "type": "number",
                        "example": 274
                    },
                }
            }
        },
        400: {
            "description": "Erreur liée à la requête, comme un "
            "un pays non valide.",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "country non valide"
                    }
                }
            }
        },
        500: {"description": "Erreur lors du traitement des données de globals_holidays.csv"}
    }
})
def get_holiday_repartition_by_type():
    """
    Fonction qui renvoi le nombre des jours
    fériés par type
    """
    try:
        country = request.args.get('country', None)

        result = holidays_service.get_holidays_repartition_by_type(country=country)

        if result == {}:
            return jsonify({
                "error": "country non valide"
            }), HTTPStatus.BAD_REQUEST

        return jsonify(result), HTTPStatus.OK

    except ImportError as error:
        return jsonify({
            "error": "Erreur lors du traitement des données de globals_holidays.csv ",
            "details": str(error)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@holidays_bp.get('/year')
@swag_from({
    "tags": ["Holidays"],
    "description": "Route qui renvoi le nombre des jours "
    "fériés par an",
    "parameters": [
        {
            "name": "country",
            "in": "query",
            "type": "string",
            "required": False,
            "description": "Pays",
            "example": "Serbia"
        }
    ],
    "responses": {
        200: {
            "description": "Nombre de jours fériés par an",
            "schema": {
                "type": "object",
                "properties": {
                    "2010": {
                        "type": "number",
                        "example": 4296
                    },
                    "2011": {
                        "type": "number",
                        "example": 4355
                    }
                }
            }
        },
        500: {"description": "Erreur lors du traitement des données de globals_holidays.csv"}
    }
})
def get_holidays_by_year():
    """
    Fonction qui renvoi le nombre de jours
    fériés par an
    """
    try:
        country = request.args.get('country', None)

        result = holidays_service.get_holidays_by_year(country=country)

        if result == {}:
            return jsonify({
                "error": "country non valide"
            }), HTTPStatus.BAD_REQUEST

        return jsonify(result), HTTPStatus.OK

    except ImportError as error:
        return jsonify({
            "error": "Erreur lors du traitement des données de globals_holidays.csv",
            "details": str(error)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@holidays_bp.get('/month')
@swag_from({
    "tags": ["Holidays"],
    "description": "Route qui renvoi le nombre des jours "
    "fériés par mois",
    "parameters": [
        {
            "name": "country",
            "in": "query",
            "type": "string",
            "required": False,
            "description": "Pays",
            "example": "Serbia"
        }
    ],
    "responses": {
        200: {
            "description": "Nombre de jours fériés par mois",
            "schema": {
                "type": "object",
                "properties": {
                    "2010-01": {
                        "type": "number",
                        "example": 317
                    },
                    "2010-02": {
                        "type": "number",
                        "example": 2
                    }
                }
            }
        },
        500: {"description": "Erreur lors du traitement des données de globals_holidays.csv"}
    }
})
def get_holidays_by_month():
    """
    Fonction qui renvoi le nombre de jours
    fériés par mois
    """
    try:
        country = request.args.get('country', None)

        result = holidays_service.get_holidays_by_month(country=country)

        if result == {}:
            return jsonify({
                "error": "country non valide"
            }), HTTPStatus.BAD_REQUEST

        return jsonify(result), HTTPStatus.OK

    except ImportError as error:
        return jsonify({
            "error": "Erreur lors du traitement des données de globals_holidays.csv",
            "details": str(error)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@holidays_bp.get('/total')
@swag_from({
    "tags": ["Holidays"],
    "description": "Route qui renvoi le total de jours fériés dans le monde en JSON",
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
            "description": "Total de jours fériés dans le monde",
            "schema": {
                "type": "object",
                "properties": {
                    "total": {
                        "type": "number",
                        "example": 276
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
        500: {"description": "Erreur lors du traitement des données de globals_holidays.csv"}
    }
})
def get_total_holidays():
    """
    Fonction qui renvoi le total de jours fériés dans le monde
    """
    try:
        holiday_type = request.args.get('holiday-type', None)

        if holiday_type and holiday_type not in HOLIDAY_TYPES:
            return jsonify(
                {
                    "error": "holiday-type non valide"
                }
            ), HTTPStatus.BAD_REQUEST

        result = holidays_service.get_total_holidays(holiday_type=holiday_type)

        return jsonify(result), HTTPStatus.OK

    except ImportError as error:
        return jsonify({
            "error": "Erreur lors du traitement des données de globals_holidays.csv ",
            "details": str(error)
        }), HTTPStatus.INTERNAL_SERVER_ERROR
