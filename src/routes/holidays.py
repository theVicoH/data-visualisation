from flask import Blueprint
from flasgger import swag_from
from src.services.holidays import HolidaysService

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
        500: {"description": "Erreur lors de la lecture du fichier"}
    }
})
def get_holiday_repartition_by_type():
    """
    Fonction qui renvoi le nombre des jours
    fériés par type
    """
    return holidays_service.get_holidays_repartition_by_type()

@holidays_bp.get('/year')
@swag_from({
    "tags": ["Holidays"],
    "description": "Route qui renvoi le nombre des jours "
    "fériés par an",
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
        500: {"description": "Erreur lors de la lecture du fichier"}
    }
})
def get_holidays_by_year():
    """
    Fonction qui renvoi le nombre de jours
    fériés par an
    """
    return holidays_service.get_holidays_by_year()
