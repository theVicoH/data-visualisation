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

    def coucou(self):
        """
        Fonction qui renvoi un message Coucou passengers ! en JSON
        """
        return jsonify({ "message": "Coucou passengers !" }), HTTPStatus.OK
