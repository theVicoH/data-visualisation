from flask import Flask, jsonify
from flasgger import Swagger, swag_from
from src.routes import passengers, holidays, holidays_and_passengers
from http import HTTPStatus
import csv
from collections import defaultdict

app = Flask(__name__)
swagger = Swagger(app)

app.register_blueprint(passengers.passengers_bp)
app.register_blueprint(holidays.holidays_bp)
app.register_blueprint(holidays_and_passengers.holidays_and_passengers_bp)

@app.route("/passengers/total-by-country")
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
                        "additionalProperties": {
                            "type": "number"
                        },
                        "example": {
                            "FRA": 1000000,
                            "USA": 2000000
                        }
                    }
                }
            }
        },
        500: {
            "description": "Erreur lors de la lecture du fichier"
        }
    }
})
def get_total_passengers_by_country():
    try:
        country_totals = defaultdict(float)
        
        with open('./data/monthly_passengers.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Total'] != 'NA':
                    country_totals[row['ISO3']] += float(row['Total']) * 1000
        
        return jsonify({
            "country_totals": dict(country_totals)
        }), HTTPStatus.OK
        
    except Exception as e:
        return jsonify({
            "error": "Erreur lors de la lecture du fichier",
            "details": str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

if __name__ == "__main__":
    app.run(debug=True)