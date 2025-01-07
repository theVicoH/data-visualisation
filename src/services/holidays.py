import os
from http import HTTPStatus
import pandas as pd
from flask import jsonify

class HolidaysService:
    """
    Class service pour gérer les datas des jours fériés
    """

    def __init__(self):
        """
        Initialisation de la classe HolidaysService
        """
        self.file_path = os.path.join('data', 'global_holidays.csv')

    def get_holidays_by_country(self):
        """
        Retourne le nombre de jours fériés par pays
        """
        try:
            df = pd.read_csv(self.file_path)
            holidays_count = df.groupby('ADM_name').size()
            return jsonify({"data": holidays_count.to_dict()}), HTTPStatus.OK

        except ImportError as error:
            return jsonify({"error": error}), HTTPStatus.INTERNAL_SERVER_ERROR

    def get_holidays_for_one_country(self, iso3):
        """
        Retourne le nombre de jours fériés ppur un seul pays

        :param iso3: iso3 du pays dont vous voulez savoir les jours fériés
        :type iso3: str
        """
        try:
            df = pd.read_csv(self.file_path)
            filtered_df = df[df['ISO3'] == iso3.upper()]

            if filtered_df.empty:
                return jsonify({
                    "error": "iso3 non valide"
                }), HTTPStatus.BAD_REQUEST

            holiday_count = len(filtered_df)

            return jsonify({
                "country": iso3,
                "data": holiday_count
            }), HTTPStatus.OK

        except ImportError as error:
            return jsonify({"error": error}), HTTPStatus.INTERNAL_SERVER_ERROR
