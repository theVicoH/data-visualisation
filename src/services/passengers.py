import os
from http import HTTPStatus
import pandas as pd
from flask import jsonify

class PassengersService:
    """
    Class service pour gérer les datas des passengers
    """

    def __init__(self):
        """
        Initialisation de la classe PassengerService
        """
        self.file_path = os.path.join('data', 'monthly_passengers.csv')

    def get_total_by_country(self):
        """
        Retourne le volume total de passagers par pays
        """
        try:
            df = pd.read_csv(self.file_path)
            totals = (df[df['Total'].notna()]['Total'] * 1000).groupby(df['ISO3']).sum()
            return jsonify({
                "country_totals": totals.to_dict()
            }), HTTPStatus.OK
        except ImportError as error:
            return jsonify({
                "error": "Erreur lors de la lecture du fichier",
                "details": str(error)
            }), HTTPStatus.INTERNAL_SERVER_ERROR

    def get_domestic_total(self):
        """
        Retourne le total des passagers domestiques par pays
        """
        try:
            df = pd.read_csv(self.file_path)
            totals = (df[df['Domestic'].notna()]['Domestic'] * 1000).groupby(df['ISO3']).sum()
            return jsonify({
                "domestic_totals": totals.to_dict()
            }), HTTPStatus.OK
        except ImportError as error:
            return jsonify({
                "error": "Erreur lors de la lecture du fichier",
                "details": str(error)
            }), HTTPStatus.INTERNAL_SERVER_ERROR

    def get_international_total(self):
        """
        Retourne le total des passagers internationaux par pays
        """
        try:
            df = pd.read_csv(self.file_path)
            totals = (
                df[df['International'].notna()]['International'] * 1000
            ).groupby(df['ISO3']).sum()
            return jsonify({
                "international_totals": totals.to_dict()
            }), HTTPStatus.OK
        except ImportError as error:
            return jsonify({
                "error": "Erreur lors de la lecture du fichier",
                "details": str(error)
            }), HTTPStatus.INTERNAL_SERVER_ERROR

    def get_country_totals(self, iso3):
        """
        Retourne le total des passagers domestiques et internationaux pour un pays
        """
        try:
            df = pd.read_csv(self.file_path)
            country_data = df[df['ISO3'] == iso3.upper()]

            if country_data.empty:
                return jsonify({
                    "error": "Pays non trouvé"
                }), HTTPStatus.NOT_FOUND

            domestic_total = (
                country_data[country_data['Domestic'].notna()]['Domestic'] * 1000
            ).sum()
            international_total = (
                country_data[country_data['International'].notna()]['International'] * 1000
            ).sum()

            return jsonify({
                "country": iso3.upper(),
                "domestic_total":domestic_total,
                "international_total": international_total
            }), HTTPStatus.OK

        except ImportError as error:
            return jsonify({
                "error": "Erreur lors de la lecture du fichier",
                "details": str(error)
            }), HTTPStatus.INTERNAL_SERVER_ERROR
