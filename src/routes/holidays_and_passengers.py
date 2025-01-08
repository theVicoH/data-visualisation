from http import HTTPStatus
from datetime import datetime
from collections import defaultdict
from flask import Blueprint, jsonify
from flasgger import swag_from
from src.services import holidays, passengers

holidays_and_passengers_bp = Blueprint(
    'holidays_and_passengers_bp',
    __name__,
    url_prefix='/holidays_and_passengers'
)

holidays_service = holidays.HolidaysService()
passengers_service = passengers.PassengersService()

@holidays_and_passengers_bp.get('/holidays-type-by-passengers')
@swag_from({
    "tags": ["Holidays & Passengers"],
    "description": "Route qui renvoi le nombre de passagers par type de jours fériés en JSON",
    "responses": {
        200: {
            "description": "Nombre de passagers par type de jours fériés",
            "schema": {
                "type": "object",
                "properties": {
                    "Half-day holiday": {
                        "type": "number",
                        "example": 2730
                    },
                    "Local holiday": {
                        "type": "number",
                        "example": 9
                    },
                }
            }
        },
        500: {
            "description": "Erreur lors du traitement des données de global_holidays.csv "
            "ou monthly_passenger.csv",
        }
    }
})
def passengers_by_holiday_type():
    """
    Fonction qui renvoi le nombre de passangers
    par type de jours fériés
    """
    try:
        holidays_and_holiday_type = holidays_service.get_holiday_and_holiday_type()
        passengers_by_month = passengers_service.get_passengers_by_date()

        holiday_passenger_count = defaultdict(float)

        for holiday, holiday_type in holidays_and_holiday_type.items():
            holiday_date = datetime.strptime(holiday, '%Y-%m-%d')
            month_str = holiday_date.strftime('%Y-%m')

            if month_str in passengers_by_month:
                holiday_passenger_count[holiday_type] += passengers_by_month[month_str]

        return jsonify(holiday_passenger_count), HTTPStatus.OK

    except ImportError as error:
        return jsonify({
            "error": "Erreur lors du traitement des données de global_holidays.csv "
            "ou monthly_passenger.csv",
            "details": str(error)
        }), HTTPStatus.INTERNAL_SERVER_ERROR
